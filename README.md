# yt-batchdl

Let’s be real: those "Online Video Converter" sites are a nightmare. They’re slow, they’re covered in sketchy ads, and if you have 20 videos to download, you’re basically signing up for a part-time job of copy-pasting.

**yt-batchdl** exists because I got tired of that. It’s a dead-simple, local tool that lets you dump a massive pile of links into a box, pick your format, and walk away while it does the heavy lifting.

---

## The Problem
Manually downloading a playlist/list of links is a soul-crushing experience.

Most "bulk" downloaders are bloated, expensive, or require a PhD to configure.

I just wanted my MP3s (or MP4s) in a folder. Fast.

## The Solution
- **Bulk Input**: Paste 1 link or 100. It doesn't care.
- **Format Toggle**: One click for High-Quality MP3s or Full HD MP4s.
- **Real-time Progress**: Satisfying progress bars so you know exactly how long until your flight/commute is saved.
- **Local Power**: It uses `yt-dlp` (the GOAT of download engines) right on your own machine. No server limits, no ads, no nonsense.

---

## Features
- **Bulk Downloads**: Paste dozens of links and let them rip.
- **Audio & Video**: One-click toggle between High-Quality MP3 (192kbps) and MP4.
- **Real-Time Progress**: Watch every download progress bar move in real-time via Server-Sent Events (SSE).
- **Smart Folders**: Organize your downloads on the fly by specifying a subfolder.
- **Proxy Support**: Bypass regional restrictions with built-in proxy settings.
- **Playlist Control**: Automatically ignores playlists to focus only on the videos you actually asked for.
- **Local First**: Your data, your files, your bandwidth. No sketchy third-party servers.

## Technical Stack
- **Backend**: Python 3.10+ with [FastAPI](https://fastapi.tiangolo.com/).
- **Engine**: [yt-dlp](https://github.com/yt-dlp/yt-dlp) (The gold standard for media extraction).
- **Multimedia**: [FFmpeg](https://ffmpeg.org/) (Required for MP3 conversion).
- **Frontend**: Vanilla HTML5, JavaScript (ES6), and [Tailwind CSS](https://tailwindcss.com/).

## Getting Started

### 1. Prerequisites
Ensure you have Python 3.10+ and FFmpeg installed.

```bash
# MacOS (Homebrew)
brew install ffmpeg

# Linux (Debian/Ubuntu)
sudo apt update && sudo apt install ffmpeg
```

### 2. Installation
Clone this repository and install the Python dependencies.

```bash
pip install -r requirements.txt
```

### 3. Run the App
Start the local server.

```bash
python main.py
```

Open your browser and navigate to `http://localhost:8000`.

## Project Structure
- `main.py`: FastAPI server handling download logic and SSE streaming.
- `index.html`: Modern, dark-themed UI.
- `downloads/`: Default directory where your media is saved.
- `requirements.txt`: Python package dependencies.

---

> [!NOTE]
> This tool is intended for personal use and downloading content you have the rights to. Please respect the terms of service of the content providers.
