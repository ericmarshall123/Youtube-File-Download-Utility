import os
import json
from yt_dlp import YoutubeDL

# ---------------------------------------------------------
# Environment Setup
# ---------------------------------------------------------

# Force Node to the front of PATH so yt-dlp can see it
NODE_PATH = "/usr/local/bin/node"
os.environ["PATH"] = f"/usr/local/bin:{os.environ['PATH']}"

print(">>> RUNNING UPDATED SCRIPT <<<")
print("PATH =", os.environ["PATH"])
print("Using Node at:", NODE_PATH)

# Shared yt-dlp JS runtime args
JS_RUNTIME_ARGS = ["--js-runtime", f"node:{NODE_PATH}"]


# ---------------------------------------------------------
# Shared yt-dlp configuration builder
# ---------------------------------------------------------

def build_opts(**overrides):
    """Return a yt-dlp options dict with JS runtime forced."""
    base = {
        "quiet": False,
        "postprocessor_args": {
            "default": JS_RUNTIME_ARGS
        }
    }
    base.update(overrides)
    return base


# ---------------------------------------------------------
# Metadata + Transcript
# ---------------------------------------------------------

def fetch_metadata_and_transcript(url: str, save_dir: str):
    """Fetch metadata and transcript if available."""
    
    # Metadata extraction
    ydl_opts = build_opts(skip_download=True)
    print("Metadata ydl_opts:", ydl_opts)

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    metadata = {
        "id": info.get("id"),
        "title": info.get("title"),
        "uploader": info.get("uploader"),
        "channel": info.get("channel"),
        "view_count": info.get("view_count"),
        "like_count": info.get("like_count"),
        "duration": info.get("duration"),
        "upload_date": info.get("upload_date"),
        "description": info.get("description"),
        "tags": info.get("tags"),
        "categories": info.get("categories"),
        "url": url
    }

    # Transcript extraction
    transcript_text = "No transcript available"
    subtitles = info.get("subtitles") or {}

    if subtitles:
        lang = "en" if "en" in subtitles else list(subtitles.keys())[0]

        ydl_sub_opts = build_opts(
            skip_download=True,
            writesubtitles=True,
            subtitleslangs=[lang],
            subtitlesformat="vtt",
            outtmpl=os.path.join(save_dir, "%(id)s.%(ext)s")
        )
        print("Subtitle ydl_sub_opts:", ydl_sub_opts)

        with YoutubeDL(ydl_sub_opts) as ydl:
            ydl.download([url])

        vtt_file = os.path.join(save_dir, f"{info['id']}.vtt")
        if os.path.exists(vtt_file):
            with open(vtt_file, "r", encoding="utf-8") as f:
                transcript_text = f.read()

    return metadata, transcript_text


# ---------------------------------------------------------
# Audio Download
# ---------------------------------------------------------

def download_audio(url: str, save_dir: str, output_file: str = "audio.mp3"):
    """Download audio as MP3."""
    output_path = os.path.join(save_dir, output_file)

    ydl_opts = build_opts(
        format="bestaudio/best",
        outtmpl=output_path,
        postprocessors=[{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    )
    print("Audio ydl_opts:", ydl_opts)

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():
    url = input("Enter the YouTube URL: ").strip()
    save_dir = input("Enter the directory to save files: ").strip()

    os.makedirs(save_dir, exist_ok=True)

    metadata, transcript = fetch_metadata_and_transcript(url, save_dir)

    # Save metadata
    metadata_file = os.path.join(save_dir, "metadata.json")
    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)
    print(f"Metadata saved to {metadata_file}")

    # Save transcript
    transcript_file = os.path.join(save_dir, "transcript.txt")
    with open(transcript_file, "w", encoding="utf-8") as f:
        f.write(transcript)
    print(f"Transcript saved to {transcript_file}")

    # Save audio
    download_audio(url, save_dir, "audio.mp3")
    print(f"Audio saved to {os.path.join(save_dir, 'audio.mp3')}")


if __name__ == "__main__":
    main()
