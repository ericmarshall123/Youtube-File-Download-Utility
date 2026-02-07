import sys
import os
import json
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog,
    QTextEdit, QProgressBar, QMessageBox
)
from PySide6.QtCore import Qt, QThread

import yt_backend
from yt_worker import YTWorker


class YouTubeUtility(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Utility (PySide6)")
        self.setMinimumSize(700, 500)

        layout = QVBoxLayout()

        # URL input
        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel("YouTube URL:"))
        self.url_input = QLineEdit()
        url_layout.addWidget(self.url_input)
        layout.addLayout(url_layout)

        # Directory picker
        dir_layout = QHBoxLayout()
        dir_layout.addWidget(QLabel("Save Directory:"))
        self.dir_input = QLineEdit()
        dir_layout.addWidget(self.dir_input)

        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.pick_directory)
        dir_layout.addWidget(browse_btn)

        layout.addLayout(dir_layout)

        # Buttons
        btn_layout = QHBoxLayout()

        self.meta_btn = QPushButton("Download Metadata")
        self.meta_btn.clicked.connect(self.download_metadata)
        btn_layout.addWidget(self.meta_btn)

        self.transcript_btn = QPushButton("Download Transcript")
        self.transcript_btn.clicked.connect(self.download_transcript)
        btn_layout.addWidget(self.transcript_btn)

        self.audio_btn = QPushButton("Download Audio")
        self.audio_btn.clicked.connect(self.download_audio)
        btn_layout.addWidget(self.audio_btn)

        layout.addLayout(btn_layout)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setValue(0)
        layout.addWidget(self.progress)

        # Log output
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)

        self.setLayout(layout)

    # ---------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------

    def pick_directory(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.dir_input.setText(folder)

    def log_message(self, text):
        self.log.append(text)

    def _get_inputs(self):
        url = self.url_input.text().strip()
        save_dir = self.dir_input.text().strip()

        if not url:
            QMessageBox.warning(self, "Missing URL", "Please enter a YouTube URL.")
            return None, None

        if not save_dir:
            QMessageBox.warning(self, "Missing Directory", "Please choose a save directory.")
            return None, None

        os.makedirs(save_dir, exist_ok=True)
        return url, save_dir

    # ---------------------------------------------------------
    # Worker Thread System
    # ---------------------------------------------------------

    def start_worker(self, url, opts):
        self.progress.setValue(0)

        self.thread = QThread()
        self.worker = YTWorker(url, opts)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.progress.setValue)
        self.worker.log.connect(self.log_message)
        self.worker.error.connect(self._on_error)
        self.worker.finished.connect(self._on_finished)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def _on_error(self, msg):
        self.log_message("ERROR: " + msg)
        QMessageBox.critical(self, "Error", msg)

    def _on_finished(self):
        self.log_message("Done.")
        self.progress.setValue(100)

    # ---------------------------------------------------------
    # Button Handlers
    # ---------------------------------------------------------

    def download_metadata(self):
        url, save_dir = self._get_inputs()
        if not url:
            return

        self.log_message("Fetching metadata...")

        try:
            metadata, info = yt_backend.fetch_metadata(url)
            title = yt_backend.sanitize_filename(metadata["title"])
            json_path = yt_backend.save_metadata_json(metadata, save_dir, title)

            self.log_message(f"Metadata saved to {json_path}")

        except Exception as e:
            self._on_error(str(e))

    def download_transcript(self):
        url, save_dir = self._get_inputs()
        if not url:
            return

        self.log_message("Fetching transcript...")

        try:
            metadata, info = yt_backend.fetch_metadata(url)
            title = yt_backend.sanitize_filename(metadata["title"])

            transcript = yt_backend.fetch_transcript(url, save_dir, title, info)

            txt_path = os.path.join(save_dir, f"{title}.txt")
            self.log_message(f"Transcript saved to {txt_path}")

        except Exception as e:
            self._on_error(str(e))

    def download_audio(self):
        url, save_dir = self._get_inputs()
        if not url:
            return

        self.log_message("Starting audio download...")

        try:
            metadata, info = yt_backend.fetch_metadata(url)
            title = yt_backend.sanitize_filename(metadata["title"])
            uploader = metadata["uploader"]

            audio_path = yt_backend.download_audio(url, save_dir, title, uploader)

            self.log_message(f"Audio saved to {audio_path}")

        except Exception as e:
            self._on_error(str(e))


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YouTubeUtility()
    window.show()
    sys.exit(app.exec())
