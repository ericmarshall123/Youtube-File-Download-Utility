import os
import json
from yt_dlp import YoutubeDL

NODE_PATH = "/usr/local/bin/node"

def build_opts(extra=None):
    if extra is None:
        extra = {}
    base = {
        "quiet": False,
        "noplaylist": True,
        "postprocessor_args": {
            "default": ["--js-runtime", f"node:{NODE_PATH}"]
        }
    }
    base.update(extra)
    return base


def fetch_metadata(url: str):
    ydl_opts = build_opts({"skip_download": True})
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
    return metadata, info


def fetch_transcript(url: str, save_dir: str):
    metadata, info = fetch_metadata(url)
    subtitles = info.get("subtitles") or {}
    transcript_text = "No transcript available"

    if subtitles:
        lang = "en" if "en" in subtitles else list(subtitles.keys())[0]
        ydl_opts = build_opts({
            "skip_download": True,
            "writesubtitles": True,
            "subtitleslangs": [lang],
            "subtitlesformat": "vtt",
            "outtmpl": os.path.join(save_dir, "%(id)s.%(ext)s")
        })
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        vtt_file = os.path.join(save_dir, f"{info['id']}.vtt")
        if os.path.exists(vtt_file):
            with open(vtt_file, "r", encoding="utf-8") as f:
                transcript_text = f.read()

    return metadata, transcript_text


def download_audio(url: str, save_dir: str, filename: str = "audio.mp3"):
    output_path = os.path.join(save_dir, filename)
    ydl_opts = build_opts({
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    })
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_path
