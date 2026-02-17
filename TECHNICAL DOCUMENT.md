Technical Specification: Bulk Media Downloader (Lite)
1. Project Overview
A lightweight, local-first web application that allows users to paste multiple YouTube/Video URLs and download them in bulk as either Video (MP4) or Audio (MP3). The app must provide real-time progress updates for each individual link.

2. Technical Stack
Backend: Python 3.10+ with FastAPI.

Engine: yt-dlp (Library for media extraction).

Multimedia Processor: ffmpeg (Required for MP3 conversion).

Frontend: Vanilla HTML5, JavaScript (ES6), and Tailwind CSS (via CDN).

Communication: Server-Sent Events (SSE) for real-time progress streaming.

3. System Architecture & Logic Flow
A. Backend Requirements (main.py)
Endpoint POST /download:

Accepts a JSON object: { "urls": [], "format": "mp3" | "video" }.

Initializes a yt-dlp process for each URL.

Real-time Progress Hook:

Use the progress_hooks feature in yt-dlp.

Extract: status, downloaded_bytes, total_bytes, speed, and eta.

Format these as a JSON string and stream them to the frontend via an SSE EventSource.

File Storage:

Downloads should be saved to a local folder named /downloads.

Files should be named using the template: %(title)s.%(ext)s.

Audio Conversion:

If "MP3" is selected, use yt-dlp post-processors to convert the file using ffmpeg.

B. Frontend Requirements (index.html)
Input UI:

A textarea for bulk URL pasting.

A toggle switch or radio buttons for MP4 vs MP3.

A "Start Download" button.

Progress Tracking UI:

A dynamic list container (#progress-container).

When a download starts, inject a "Card" for that URL containing:

The video title (once fetched).

A visual progress bar (0–100%).

Status text (e.g., "Downloading...", "Converting...", "Finished").

JavaScript Logic:

Split the textarea content by newlines and filter out empty strings.

Use fetch to trigger the backend.

Listen to the SSE stream to update the specific progress bar associated with each URL.

4. Key yt-dlp Configuration (Instruction for AI)
The AI should use the following options for the YoutubeDL object:

For MP3:

Python
'format': 'bestaudio/best',
'postprocessors': [{
    'key': 'FFmpegExtractAudio',
    'preferredcodec': 'mp3',
    'preferredquality': '192',
}]
For Video:

Python
'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
5. Directory Structure
Plaintext
/project-root
├── main.py            # FastAPI server and logic
├── index.html         # Single-page UI
├── downloads/         # Local folder for finished files
└── requirements.txt   # fastapi, uvicorn, yt-dlp
6. Constraints & Error Handling
Validation: Frontend must validate that inputs are valid URLs before sending to backend.

Concurrency: To prevent CPU/Bandwidth choking, the backend should process downloads sequentially or in small batches (max 3 at a time).

Clean-up: Provide a "Clear Finished" button on the UI to remove completed progress cards.