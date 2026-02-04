# YouTube Metadata & Audio Extractor

A lightweight Python utility for extracting metadata, transcripts, and high‑quality MP3 audio from YouTube videos using **yt‑dlp**. This tool is designed for researchers, content analysts, and developers who need structured video information or offline audio access.

## What This Tool Does

### 1. Fetches YouTube Metadata
The function **`fetch_metadata_and_transcript`** retrieves detailed information about a YouTube video without downloading the video itself. It collects:

- **Video ID**
- **Title**
- **Uploader / Channel**
- **View count**
- **Like count**
- **Duration**
- **Upload date**
- **Description**
- **Tags**
- **Categories**
- **Original URL**

All metadata is saved to **`metadata.json`**.

### 2. Attempts to Download a Transcript
If subtitles are available:

- English is selected when possible; otherwise, the first available language is used
- Subtitles are downloaded in **VTT format**
- The `.vtt` file is read and converted into plain text
- If no subtitles exist or retrieval fails, a fallback message is used

The transcript is saved as **`transcript.txt`**.

### 3. Downloads Audio as MP3
The **`download_audio`** function:

- Downloads the best available audio stream
- Converts it to MP3 using FFmpeg via yt‑dlp
- Saves the final file as **`audio.mp3`** in the chosen directory

### 4. User Interaction (main function)
The script guides the user through:

- Entering a YouTube URL
- Choosing a directory to save files
- Automatically creating the directory if needed
- Fetching metadata and transcript
- Saving both to disk
- Downloading audio
- Displaying progress messages

## Features

- Extracts detailed YouTube metadata
- Downloads subtitles/transcripts when available
- Saves transcripts as readable text files
- Converts audio to MP3 with high quality
- Simple command‑line interface
- No video download required

## Tech Stack

- **Python 3**
- **yt‑dlp**
- **FFmpeg**

## Use Cases

- Archiving lectures, podcasts, or interviews
- Preparing datasets for NLP or machine learning
- Content analysis and research workflows
- Offline listening
