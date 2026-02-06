from PySide6.QtCore import QObject, Signal, Slot
from yt_dlp import YoutubeDL
import traceback

class YTWorker(QObject):
    progress = Signal(float)       # 0–100
    log = Signal(str)              # text log
    finished = Signal()            # done
    error = Signal(str)            # error message

    def __init__(self, url, opts):
        super().__init__()
        self.url = url
        self.opts = opts

    @Slot()
    def run(self):
        try:
            # Inject progress hook
            self.opts["progress_hooks"] = [self._hook]

            with YoutubeDL(self.opts) as ydl:
                ydl.download([self.url])

            self.finished.emit()

        except Exception as e:
            tb = traceback.format_exc()
            self.error.emit(str(e) + "\n" + tb)

    def _hook(self, d):
        if d["status"] == "downloading":
            percent = d.get("downloaded_bytes", 0) / max(d.get("total_bytes", 1), 1)
            self.progress.emit(percent * 100)

        if d["status"] == "finished":
            self.progress.emit(100)
            self.log.emit("Processing file…")
