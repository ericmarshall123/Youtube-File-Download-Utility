# YouTube Metadata, Transcript & Audio Extractor (GUI Edition)

A desktop application for extracting metadata, transcripts, and high‑quality MP3 audio from YouTube videos. The tool uses **PySide6** for the graphical interface, **yt‑dlp** for extraction, and a threaded backend to ensure a responsive user experience.

This application is designed for researchers, analysts, archivists, and anyone who need structured YouTube data or offline audio access.

## Features

YouTube Metadata, Transcript & Audio Extractor (GUI Edition)
A desktop application for extracting metadata, transcripts, and high‑quality MP3 audio from YouTube videos. The tool uses PySide6 for the graphical interface, yt‑dlp for extraction, and a threaded backend to ensure a responsive user experience.

This application is designed for researchers, analysts, archivists, and anyone who needs structured YouTube data or offline audio access.

Features
Modern PySide6 Desktop Interface
Clean, responsive Qt‑based GUI

URL input field

Directory picker

Buttons for metadata, transcript, and audio extraction

Real‑time progress bar

Scrollable log output

Error popups and status messages

Threaded yt‑dlp Backend
All downloads run in background threads

GUI remains responsive

Progress updates via yt‑dlp hooks

Centralized worker class for clean architecture

Metadata Extraction
Retrieves detailed information without downloading the video:

- Video ID

- Title

- Uploader / Channel

- View count

- Like count

- Duration

- Upload date

- Description

- Tags

- Categories

- Original URL

Saved as metadata.json.

Transcript Extraction
If subtitles are available:

- English is preferred when available

- Falls back to the first available language

- Downloads .vtt subtitle file

- Converts it to plain text

- Gracefully handles missing transcripts

- Saved as transcript.txt.

# YouTube Metadata, Transcript & Audio Extractor (GUI Edition)

A desktop application for extracting metadata, transcripts, and high‑quality MP3 audio from YouTube videos. The tool uses **PySide6** for the graphical interface, **yt‑dlp** for extraction, and a threaded backend to ensure a responsive user experience.

This application is designed for researchers, analysts, archivists, and anyone who need structured YouTube data or offline audio access.

High‑Quality MP3 Audio Download
Downloads the best available audio stream

Converts to MP3 using FFmpeg

Saves as audio.mp3 in the selected directory

Clean Project Architecture
The application is organized into three main components:

yt_gui.py — PySide6 GUI

yt_backend.py — metadata, transcript, and audio logic

yt_worker.py — threaded yt‑dlp worker with progress hooks

This structure keeps the project modular and easy to extend.

Tech Stack
Python 3.11+

PySide6 (Qt6)

yt‑dlp

FFmpeg

Node.js (required for YouTube’s JavaScript‑based extraction)

How to Use the Application
1. Enter a YouTube URL
Paste any valid YouTube video link into the URL field.

2. Choose a Save Directory
Select where metadata, transcript, and audio files will be stored.

3. Choose an Action
Download Metadata

Download Transcript

Download Audio (MP3)

4. Monitor Progress
The progress bar updates in real time as yt‑dlp downloads and processes the video.

5. Review Logs
All status messages and yt‑dlp output appear in the log window.

Use Cases
Academic research

Podcast or lecture archiving

NLP dataset creation

Content analysis

Offline listening

Media organization workflows

Project Structure

### Modern PySide6 Desktop Interface
- Clean, responsive Qt‑based GUI
- URL input field
- Directory picker
- Buttons for metadata, transcript, and audio extraction
- Real‑time progress bar
- Scrollable log output
- Error popups and status messages

### Threaded yt‑dlp Backend
- All downloads run in background threads
- GUI remains responsive
- Progress updates via yt‑dlp hooks
- Centralized worker class for clean architecture

### Metadata Extraction
Retrieves detailed information without downloading the video:
- Video ID
- Title
- Uploader / Channel
- View count
- Like count
- Duration
- Upload date
- Description
- Tags
- Categories
- Original URL

Saved as **metadata.json**.

### Transcript Extraction
If subtitles are available:
- English is preferred when available
- Falls back to the first available language
- Downloads `.vtt` subtitle file
- Converts it to plain text
- Gracefully handles missing transcripts

Saved as **transcript.txt**.

### High‑Quality MP3 Audio Download
- Downloads the best available audio stream
- Converts to MP3 using FFmpeg
- Saves as **audio.mp3** in the selected directory

### Clean Project Architecture
The application is organized into three main components:
- **yt_gui.py** — PySide6 GUI
- **yt_backend.py** — metadata, transcript, and audio logic
- **yt_worker.py** — threaded yt‑dlp worker with progress hooks

This structure keeps the project modular and easy to extend.

## Tech Stack
- Python 3.11+
- PySide6 (Qt6)
- yt‑dlp
- FFmpeg
- Node.js (required for YouTube’s JavaScript‑based extraction)

## How to Use the Application

### 1. Enter a YouTube URL
Paste any valid YouTube video link into the URL field.

### 2. Choose a Save Directory
Select where metadata, transcript, and audio files will be stored.

### 3. Choose an Action
- Download Metadata
- Download Transcript
- Download Audio (MP3)

### 4. Monitor Progress
The progress bar updates in real time as yt‑dlp downloads and processes the video.

### 5. Review Logs
All status messages and yt‑dlp output appear in the log window.

## Use Cases
- Academic research
- Podcast or lecture archiving
- NLP dataset creation
- Content analysis
- Offline listening
- Media organization workflows

## Project Structure

### Code

youtubeutility/
│
├── yt_gui.py          # PySide6 GUI application
├── yt_backend.py      # Metadata, transcript, and audio logic
├── yt_worker.py       # Threaded yt-dlp worker with progress hooks
└── README.md          # Project documentation


Planned Enhancements
Playlist controls (first video only, full playlist, or range selection)

Batch mode (multiple URLs or file import)

Filename sanitizing and custom output templates

Configurable settings file

macOS .app packaging

Windows/Linux builds

Dark mode UI
=======

## Planned Enhancements
- Playlist controls (first video only, full playlist, or range selection)
- Batch mode (multiple URLs or file import)
- Filename sanitizing and custom output templates
- Configurable settings file
- macOS .app packaging
- Windows/Linux builds
- Dark mode UI

