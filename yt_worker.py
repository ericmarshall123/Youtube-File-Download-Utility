from PySide6.QtCore import QObject, Signal, Slot
from yt_dlp import YoutubeDL
import traceback
import signal
import os

class YTWorker(QObject):
    progress = Signal(float)
    log = Signal(str)
    finished = Signal()
    error = Signal(str)

    def __init__(self, url, opts):
        super().__init__()
        self.url = url
        self.opts = opts
        self._stop_requested = False

    @Slot()
    def run(self):
        try:
            # Allow Ctrl+C to interrupt subprocesses
            signal.signal(signal.SIGINT, signal.SIG_DFL)

            # Inject progress hook
            self.opts["progress_hooks"] = [self._hook]

            with YoutubeDL(self.opts) as ydl:
                ydl.download([self.url])

            self._cleanup()
            self.finished.emit()

        except Exception as e:
            tb = traceback.format_exc()
            self.error.emit(str(e) + "\n" + tb)
            self._cleanup()

    def _hook(self, d):
        if self._stop_requested:
            raise KeyboardInterrupt("Download cancelled")

        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 1
            downloaded = d.get("downloaded_bytes", 0)
            percent = (downloaded / total) * 100
            self.progress.emit(percent)

        if d["status"] == "finished":
            self.progress.emit(100)
            self.log.emit("Processing file…")

    def stop(self):
        """Called if the GUI wants to cancel the download."""
        self._stop_requested = True

    def _cleanup(self):
        """Ensure no subprocesses linger."""
        try:
            os.killpg(0, signal.SIGTERM)
        except Exception:
            pass
