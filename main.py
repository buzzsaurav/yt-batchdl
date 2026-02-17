import os
import json
import asyncio
from typing import List, Dict
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DOWNLOAD_DIR = "downloads"
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Global state to store progress
progress_state: Dict[str, dict] = {}

def progress_hook(d, url_id):
    if not url_id:
        return

    if d['status'] == 'downloading':
        progress = d.get('_percent_str', '0%').replace('%', '').strip()
        progress_state[url_id] = {
            'url_id': url_id,
            'status': 'Downloading',
            'progress': progress,
            'speed': d.get('_speed_str', 'N/A'),
            'eta': d.get('_eta_str', 'N/A'),
            'title': d.get('info_dict', {}).get('title', 'Unknown')
        }
    elif d['status'] == 'finished':
        progress_state[url_id] = {
            'url_id': url_id,
            'status': 'Finished',
            'progress': '100',
            'speed': '0',
            'eta': '0',
            'title': d.get('info_dict', {}).get('title', 'Unknown')
        }

def run_download(url, format_type, folder, proxy):
    def hook_wrapper(d):
        progress_hook(d, url)

    # Sanitize and prepare path
    target_dir = DOWNLOAD_DIR
    if folder:
        target_dir = os.path.join(DOWNLOAD_DIR, folder.strip().strip('/'))
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)

    ydl_opts = {
        'outtmpl': f'{target_dir}/%(title)s.%(ext)s',
        'progress_hooks': [hook_wrapper],
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
    }

    if proxy:
        ydl_opts['proxy'] = proxy

    if format_type == 'mp3':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        ydl_opts.update({
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        progress_state[url] = {
            'url_id': url,
            'status': f'Error: {str(e)}',
            'progress': '0',
            'title': 'Error'
        }

@app.post("/download")
async def start_download(request: Request, background_tasks: BackgroundTasks):
    data = await request.json()
    urls = [u.strip() for u in data.get("urls", []) if u.strip()]
    format_type = data.get("format", "mp3")
    folder = data.get("folder", "")
    proxy = data.get("proxy", None)
    
    for url in urls:
        progress_state[url] = {
            'url_id': url,
            'status': 'Queued',
            'progress': '0',
            'title': 'Waiting...'
        }
        background_tasks.add_task(run_download, url, format_type, folder, proxy)
    
    return {"status": "started", "count": len(urls)}

@app.get("/events")
async def event_stream(request: Request):
    async def event_generator():
        last_sent = {}
        while True:
            if await request.is_disconnected():
                break
            
            # Send updates only if state changed
            for url_id, state in list(progress_state.items()):
                state_json = json.dumps(state)
                if last_sent.get(url_id) != state_json:
                    yield f"data: {state_json}\n\n"
                    last_sent[url_id] = state_json
            
            await asyncio.sleep(0.5)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open("index.html", "r") as f:
        return f.read()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

