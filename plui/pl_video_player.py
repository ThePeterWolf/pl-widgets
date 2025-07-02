from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget


class PLVideoPlayer(QtWidgets.QWidget):
    """
    A simple video player widget using QMediaPlayer and QVideoWidget.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Player backend
        self.player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.player.setAudioOutput(self.audio_output)

        # Video display
        self.video_widget = QVideoWidget(self)
        self.video_widget.setMinimumSize(QtCore.QSize(200, 150))
        self.player.setVideoOutput(self.video_widget)

        # Controls
        self.play_button = QtWidgets.QPushButton("▶")
        self.open_button = QtWidgets.QPushButton("📂")
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.time_label = QtWidgets.QLabel("00:00 / 00:00")

        self.play_button.setFixedSize(32, 32)
        self.open_button.setFixedSize(32, 32)

        # Layout
        controls = QtWidgets.QHBoxLayout()
        controls.addWidget(self.open_button)
        controls.addWidget(self.play_button)
        controls.addWidget(self.slider)
        controls.addWidget(self.time_label)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.video_widget)
        layout.addLayout(controls)
        self.setLayout(layout)

        # Connections
        self.open_button.clicked.connect(self.open_file)
        self.play_button.clicked.connect(self.toggle_play)
        self.slider.sliderMoved.connect(self.seek)

        self.player.positionChanged.connect(self.update_position)
        self.player.durationChanged.connect(self.update_duration)

        self._duration = 0

    def open_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open Video", "", "Video Files (*.mp4 *.avi *.mov *.mkv)"
        )
        if file_path:
            self.player.setSource(QtCore.QUrl.fromLocalFile(file_path))
            self.player.play()
            self.play_button.setText("⏸")

    def toggle_play(self):
        if self.player.playbackState() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.play_button.setText("▶")
        else:
            self.player.play()
            self.play_button.setText("⏸")

    def seek(self, value):
        if self._duration > 0:
            self.player.setPosition(int(self._duration * value / 100))

    def update_position(self, pos):
        if self._duration > 0:
            self.slider.setValue(int(pos / self._duration * 100))
        self.update_time_label(pos)

    def update_duration(self, duration):
        self._duration = duration

    def update_time_label(self, pos):
        def fmt(ms):
            s = ms // 1000
            return f"{s // 60:02}:{s % 60:02}"
        self.time_label.setText(f"{fmt(pos)} / {fmt(self._duration)}")
