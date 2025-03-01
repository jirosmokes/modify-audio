import os
import sys

from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (
    QLabel, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
    QMainWindow, QStackedWidget, QProgressBar, QSpacerItem, QSizePolicy
)

from appflow.extractSpectroSound import process_video


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AKIRA - Audio & Video Processor")
        self.setGeometry(100, 60, 1200, 900)
        self.setStyleSheet("background-color: #F7F9FC;")
        self.setWindowIcon(QIcon("AKIRA_LOGO.png"))

        # Initialize stacked widget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Initialize pages
        self.main_page = QWidget()
        self.upload_page = QWidget()
        self.results_page = QWidget()

        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.upload_page)
        self.stacked_widget.addWidget(self.results_page)

        # Setup UI for each page
        self.setup_main_page()
        self.setup_upload_page()
        self.setup_results_page()

        self.stacked_widget.setCurrentWidget(self.main_page)

    def setup_main_page(self):
        layout = QVBoxLayout(self.main_page)

        # Content
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_widget.setStyleSheet("background-color: #1A3C10; border-radius: 10px;")
        content_layout.setAlignment(Qt.AlignTop)  # Align content to the top

        # Horizontal layout for title and logo
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignCenter)  # Align header to the left
        spacer = QSpacerItem(-100, 0)
        header_layout.addItem(spacer)

        # Logo
        logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), "AKIRA_LOGO.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():  # Check if pixmap is valid
                pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                logo_label.setPixmap(pixmap)
            else:
                logo_label.setText("Failed to load logo")  # Error text if pixmap is invalid
        else:
            logo_label.setText(f"Logo file not found: {logo_path}")  # Display an error if file not found

        # Title
        self.title_label = QLabel("AKIRA")
        self.title_label.setFont(QFont("Arial", 70, QFont.Black))
        self.title_label.setStyleSheet("color: #F1FBEF;")

        # Add logo and title to the header_layout
        header_layout.addWidget(logo_label)
        header_layout.addWidget(self.title_label)

        # Add header_layout to content_layout (this ensures the header stays at the top)
        content_layout.addLayout(header_layout)

        # Description Box (Centering the box)
        self.description_box = QLabel(
            "Welcome to the project on \"Extracting Overstimulating Audio Signals from Cartoon Videos Using STFT, MFCC, and VGG16 CNN and Retuning Audio Playback for Child-Friendly Listening.\"\n\n"
            "This research aims to enhance children's audio experiences by analyzing overstimulating audio signals from cartoons. "
            "Using Short-Time Fourier Transform (STFT), Mel Frequency Cepstral Coefficients (MFCC), and VGG16 Convolutional Neural Networks (CNN), "
            "we process and retune audio to create child-friendly listening environments."
        )
        self.description_box.setFont(QFont("Arial", 17))
        self.description_box.setFixedSize(1000, 450)
        self.description_box.setStyleSheet(
            "background-color: #F1FBEF; border-radius: 10px; padding: 60px; color: black;")
        self.description_box.setWordWrap(True)
        self.description_box.setAlignment(Qt.AlignJustify)
        content_layout.addWidget(self.description_box, alignment=Qt.AlignCenter)  # Center the description box

        # Next Button (Centering the button)
        self.next_btn = QPushButton("→")
        self.next_btn.setFont(QFont("Arial", 20, QFont.Black))
        self.next_btn.setFixedSize(100, 60)
        self.next_btn.setStyleSheet("background-color: #F1FBEF; color: #1A3C10; border-radius: 10px;")
        self.next_btn.clicked.connect(self.go_to_upload_page)  # Navigate to the upload page
        content_layout.addWidget(self.next_btn, alignment=Qt.AlignRight)  # Center the button
        # Create a horizontal layout for the button
        button_layout = QHBoxLayout()

        # Add a spacer item before the button to control positioning (move the button to the right)
        button_layout.addItem(QSpacerItem(900, 0))  # Move right
        button_layout.addWidget(self.next_btn)

        # Add the button_layout to the content_layout
        content_layout.addLayout(button_layout)

        # Add content_widget to main layout
        layout.addWidget(content_widget)

    def setup_upload_page(self):
        # Set background color for the entire page (widget containing the layout)
        self.upload_page.setStyleSheet("background-color: #F1FBEF;")

        layout = QVBoxLayout(self.upload_page)

        # Logo
        logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), "AKIRA_LOGO.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():  # Check if pixmap is valid
                pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                logo_label.setPixmap(pixmap)
            else:
                logo_label.setText("Failed to load logo")  # Error text if pixmap is invalid
        else:
            logo_label.setText(f"Logo file not found: {logo_path}")  # Display an error if file not found

        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label, alignment=Qt.AlignCenter)

        # Description Box with Numbering
        self.description_box = QLabel(
            "<div style='text-align: center; font-size: 40px;'><b>Upload a Cartoon Video</b></div><br>"
            "1. Click on the \"UPLOAD\" button.<br><br>"
            "2. A window will open asking you to select a file from your computer or phone.<br><br>"
            "3. Locate the cartoon video you want to upload.<br><br>"
            "4. Click on the file, then press \"Open\" to start the upload.<br><br>"
            "5. Wait for the video to be uploaded; this may take a few seconds or minutes."
        )
        self.description_box.setFont(QFont("Arial", 15))
        self.description_box.setStyleSheet(
            "background-color: #1A3C10; border-radius: 10px; padding: 50px; color: #F1FBEF;")
        self.description_box.setWordWrap(True)
        self.description_box.setAlignment(Qt.AlignJustify)  # Centering the description text
        self.description_box.setFixedWidth(1000)  # Set a fixed width for the description box
        layout.addWidget(self.description_box, alignment=Qt.AlignCenter)

        # Upload Button
        self.upload_btn = QPushButton("UPLOAD")
        self.upload_btn.setFont(QFont("Arial", 14, QFont.Bold))
        self.upload_btn.setStyleSheet("background-color: #1A3C10; color: #F1FBEF; padding: 10px; border-radius: 10px;")
        self.upload_btn.setFixedSize(200, 60)
        self.upload_btn.clicked.connect(self.upload_video)
        layout.addWidget(self.upload_btn, alignment=Qt.AlignCenter)

        # Add some space between upload button and progress bar
        layout.addSpacing(20)  # Adjust spacing as needed

        # Progress Bar Section
        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setFixedWidth(400)
        self.progress_bar.setStyleSheet(""" 
            QProgressBar { 
                border: 2px solid #5e5e5e; 
                border-radius: 10px; 
                text-align: center; 
            }
            QProgressBar::chunk { 
                background-color: #78D35F; 
                width: 20px; 
                border-radius: 5px; 
            }
        """)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar, alignment=Qt.AlignCenter)

        # Add spacing at the bottom for better layout flow
        layout.addStretch()



    def setup_results_page(self):
        layout = QVBoxLayout(self.results_page)

        # Set background color and border radius
        self.results_page.setStyleSheet("background-color: #F1FBEF; border-radius: 10px; margin: 3px;")

        # Header Container
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignLeft)
        header_layout.setContentsMargins(10, 0, 10, 0)

        # Header widget
        header_layout_widget = QWidget()
        header_layout_widget.setStyleSheet("background-color: #1A3C10; border-radius: 10px;")
        header_layout_widget.setFixedHeight(70)
        header_layout_widget.setLayout(header_layout)

        # Create header buttons
        button1 = QPushButton("←")
        button2 = QPushButton("→")

        # Style buttons
        button_style = "background-color: #F1FBEF; color: #1A3C10; border-radius: 5px; padding: 10px; font-size: 20px;"
        button1.setStyleSheet(button_style)
        button2.setStyleSheet(button_style)

        # Connect button1 to go back to the upload page
        button1.clicked.connect(self.go_to_upload_page)

        # Add buttons to header
        header_layout.addWidget(button1)
        header_layout.addWidget(button2)

        # Add header to layout
        layout.addWidget(header_layout_widget)

        # Main layout (horizontal for left and right sections)
        main_layout = QHBoxLayout()

        # Left side layout
        left_layout = QVBoxLayout()

        # Video display container (Top Box)
        top_box = QWidget()
        top_box.setStyleSheet("background-color: #1A3C10; border-radius: 10px;")
        top_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        top_box_layout = QVBoxLayout(top_box)

        # Video widget container (for rounded corners)
        video_container_top = QWidget()
        video_container_top.setStyleSheet("background-color: black; border-radius: 15px;")
        video_container_top.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        video_container_top_layout = QVBoxLayout(video_container_top)
        video_container_top_layout.setContentsMargins(0, 0, 0, 0)

        # Create a QVideoWidget for displaying video in top box
        self.video_widget_top = QVideoWidget()
        self.video_widget_top.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Media Player
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_widget_top)

        # Add video widget to the rounded container (Top Box)
        video_container_top_layout.addWidget(self.video_widget_top)

        # Play Button
        self.play_button = QPushButton(" || ")
        self.play_button.setStyleSheet(button_style)
        self.play_button.setFixedSize(100, 50)  # Set the size here (adjust width and height as needed)
        self.play_button.clicked.connect(self.play_video)

        # Add elements to top_box
        top_box_layout.addWidget(video_container_top)
        top_box_layout.addWidget(self.play_button, alignment=Qt.AlignLeft)

        # Video display container (Bottom Box)
        bottom_box = QWidget()
        bottom_box.setStyleSheet("background-color: #1A3C10; border-radius: 10px;")
        bottom_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        bottom_box_layout = QVBoxLayout(bottom_box)

        # Video widget container (for rounded corners in Bottom Box)
        video_container_bottom = QWidget()
        video_container_bottom.setStyleSheet("background-color: black; border-radius: 15px;")
        video_container_bottom.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        video_container_bottom_layout = QVBoxLayout(video_container_bottom)
        video_container_bottom_layout.setContentsMargins(0, 0, 0, 0)

        # Create another QVideoWidget for displaying video in bottom box
        self.video_widget_bottom = QVideoWidget()
        self.video_widget_bottom.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Separate Media Player for Bottom Box
        self.media_player_bottom = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player_bottom.setVideoOutput(self.video_widget_bottom)

        # Load video file into bottom player
        video_path = "app-test-retuned.mp4"  # Replace with the actual video path
        self.media_player_bottom.setMedia(QMediaContent(QUrl.fromLocalFile(video_path)))

        # Add video widget to the rounded container (Bottom Box)
        video_container_bottom_layout.addWidget(self.video_widget_bottom)

        # Play Button for Bottom Box
        self.play_button_bottom = QPushButton(" || ")
        self.play_button_bottom.setStyleSheet(button_style)
        self.play_button_bottom.setFixedSize(100, 50)
        self.play_button_bottom.clicked.connect(self.play_video_bottom)

        # Add elements to bottom_box
        bottom_box_layout.addWidget(video_container_bottom)
        bottom_box_layout.addWidget(self.play_button_bottom, alignment=Qt.AlignLeft)

        # Add to left layout
        left_layout.addWidget(top_box, 1)
        left_layout.addWidget(bottom_box, 1)

        # Right-side box
        right_box = QWidget()
        right_box.setStyleSheet("background-color: #1A3C10; border-radius: 10px; padding: 10px;")
        right_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Add left and right sections to main layout
        main_layout.addLayout(left_layout, 1)
        main_layout.addWidget(right_box, 1)

        # Add main layout
        layout.addLayout(main_layout)

    def go_to_upload_page(self):
        self.stacked_widget.setCurrentWidget(self.upload_page)

    from extractSpectroSound import process_video


    def load_and_detect_segments(self):
        from detectModel import load_ai_model, detect_overstimulating_segments, save_and_print_results
        ai_model = load_ai_model()
        segment_folder = "spectrogram_segments"  # Folder containing segmented spectrogram images

        # Detect overstimulating segments
        overstim_results = detect_overstimulating_segments(segment_folder, ai_model)
        save_and_print_results(overstim_results)

    def retune_and_display(self, fileName):
        from retunedDetected import load_overstim_segments, retune_audio, attach_audio_to_video
        json_file = "overstimulating_segments.json"
        input_audio = "extracted_audio_boosted.mp3"
        output_audio = "retuned_audio.mp3"
        input_video = fileName
        output_video = "app-test-retuned.mp4"

        overstim_segments = load_overstim_segments(json_file)
        retune_audio(input_audio, output_audio, overstim_segments)
        attach_audio_to_video(input_video, output_audio, output_video)

    def upload_video(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "MP4 Files (*.mp4)", options=options)
        if file_name:
            output_mp3 = "extracted_audio.mp3"
            full_spectrogram_img = "full_spectrogram.png"
            output_segments_folder = "spectrogram_segments"
            output_mp4 = "original-boosted.mp4"

            # Ensure the output folder exists
            if not os.path.exists(output_segments_folder):
                os.makedirs(output_segments_folder)

            process_video(file_name, output_mp3, full_spectrogram_img, output_segments_folder, output_mp4)

            self.video_path = output_mp4  # Store the selected video path
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(100)  # Simulating upload completion
            self.stacked_widget.setCurrentWidget(self.results_page)
            # Load video into the media player
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(self.video_path)))
            self.load_and_detect_segments()
            self.retune_and_display(file_name)

    def play_video(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.play_button.setText(" ▶ ")
        else:
            self.media_player.play()
            self.play_button.setText(" || ")

    def play_video_bottom(self):
        if self.media_player_bottom.state() == QMediaPlayer.PlayingState:
            self.media_player_bottom.pause()
            self.play_button_bottom.setText(" ▶ ")
        else:
            self.media_player_bottom.play()
            self.play_button_bottom.setText(" || ")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())