import os
import json
import re
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError, ExtractorError

# ---------------------------
# Custom Exceptions
# ---------------------------

class InvalidURLError(Exception):
    pass

class MetadataError(Exception):
    pass

class TranscriptError(Exception):
    pass

class AudioDownloadError(Exception):
    pass


# ---------------------------
# Helpers
# ---------------------------

def sanitize_filename(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "", name)


def ensure_unique_path(path: str) -> str:
    """Avoid overwriting by adding (1), (2), etc."""
    if not os.path.exists(path):
        return path

    base, ext = os.path.splitext(path)
    counter = 1
    new_path = f"{base} ({counter}){ext}"

    while os.path.exists(new_path):
        counter += 1
        new_path = f"{base} ({counter}){ext}"

    return new_path


def validate_url(url: str):
    if not isinstance(url, str) or ("youtube.com" not in url and "youtu.be" not in url):
        raise InvalidURLError("This is not a valid YouTube URL.")


def build_opts(extra=None):
    base = {
        "quiet": False,
        "noplaylist": True,
    }
    if extra:
        base.update(extra)
    return base


# ---------------------------
# Metadata
# ---------------------------

def fetch_metadata(url: str):
    validate_url(url)

    try:
        ydl_opts = build_opts({"skip_download": True})
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

    except (ExtractorError, DownloadError) as e:
        raise MetadataError(f"Failed to extract metadata: {e}")

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


# ---------------------------
# Transcript
# ---------------------------

def fetch_transcript(url: str, save_dir: str, title: str, info: dict):
    subtitles = info.get("subtitles") or {}
    transcript_text = "No transcript available"

    if not subtitles:
        return transcript_text

    try:
        lang = "en" if "en" in subtitles else list(subtitles.keys())[0]

        ydl_opts = build_opts({
            "skip_download": True,
            "writesubtitles": True,
            "subtitleslangs": [lang],
            "subtitlesformat": "vtt",
            "outtmpl": os.path.join(save_dir, f"{title}.%(ext)s")
        })

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        vtt_file = os.path.join(save_dir, f"{title}.vtt")
        txt_file = ensure_unique_path(os.path.join(save_dir, f"{title}.txt"))

        if os.path.exists(vtt_file):
            with open(vtt_file, "r", encoding="utf-8") as f:
                transcript_text = f.read()

            with open(txt_file, "w", encoding="utf-8") as f:
                f.write(transcript_text)

    except Exception as e:
        raise TranscriptError(f"Transcript download failed: {e}")

    return transcript_text


# ---------------------------
# Audio Download
# ---------------------------

def download_audio(url: str, save_dir: str, title: str, uploader: str):
    try:
        output_template = os.path.join(save_dir, f"{title}.%(ext)s")

        # Inject metadata directly into the info dict
        # yt-dlp will pass this to FFmpegMetadata automatically
        def add_metadata_hook(d):
            if d.get("info_dict"):
                d["info_dict"]["artist"] = uploader
                d["info_dict"]["title"] = title

        ydl_opts = build_opts({
            "format": "bestaudio/best",
            "outtmpl": output_template,
            "progress_hooks": [add_metadata_hook],
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                },
                {
                    "key": "FFmpegMetadata",
                    "add_metadata": True,
                    "add_chapters": False,
                    "add_infojson": False
                }
            ]
        })

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        final_path = os.path.join(save_dir, f"{title}.mp3")
        final_path = ensure_unique_path(final_path)

        return final_path

    except Exception as e:
        raise AudioDownloadError(f"Audio download failed: {e}")
    

# ---------------------------
# JSON Save
# ---------------------------

def save_metadata_json(metadata: dict, save_dir: str, title: str):
    try:
        json_path = ensure_unique_path(os.path.join(save_dir, f"{title}.json"))
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4)
        return json_path

    except Exception as e:
        raise MetadataError(f"Failed to save metadata JSON: {e}")
