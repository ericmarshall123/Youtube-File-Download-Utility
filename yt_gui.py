import sys
import os
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QFileDialog,
    QTextEdit, QProgressBar
)
from PySide6.QtCore import Qt

class YouTubeUtility(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Utility (PySide6)")
        self.setMinimumSize(600, 400)

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

    def pick_directory(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.dir_input.setText(folder)

    def log_message(self, text):
        self.log.append(text)

    # Placeholder methods — we will wire these up next
    def download_metadata(self):
        self.log_message("Metadata download not implemented yet.")

    def download_transcript(self):
        self.log_message("Transcript download not implemented yet.")

    def download_audio(self):
        self.log_message("Audio download not implemented yet.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YouTubeUtility()
    window.show()
    sys.exit(app.exec())
