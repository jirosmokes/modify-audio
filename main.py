import os
import sys
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QLabel, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
    QMessageBox, QMainWindow, QStackedWidget, QProgressBar
)

from extractAudio import extract_audio, create_video_without_audio
from audioAnalysis import analyze_audio_stft, analyze_audio_mfcc, visualize_loudness

class ProcessingThread(QThread):
    progress = pyqtSignal(int)
    completed = pyqtSignal(str, str)
    error = pyqtSignal(str)

    def __init__(self, file_path, video_counter, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.video_counter = video_counter

    def run(self):
        try:
            # Define the folder paths
            audio_output_folder = "extracted_audio_folder"
            video_output_folder = "video_without_audio_folder"
            stft_output_folder = "stft_spectrogram_images"
            mfcc_output_folder = "mfcc_spectrogram_images"
            loudness_output_folder = "loudness_images"

            # Create output folders
            os.makedirs(audio_output_folder, exist_ok=True)
            os.makedirs(video_output_folder, exist_ok=True)
            os.makedirs(stft_output_folder, exist_ok=True)
            os.makedirs(mfcc_output_folder, exist_ok=True)
            os.makedirs(loudness_output_folder, exist_ok=True)

            # Generate unique filenames
            audio_filename = f"extracted_audio_{self.video_counter}.mp3"
            video_filename = f"video_without_audio_{self.video_counter}.mp4"

            audio_file = os.path.join(audio_output_folder, audio_filename)
            video_without_audio_file = os.path.join(video_output_folder, video_filename)

            # Step 1: Extract audio
            self.progress.emit(25)
            extracted_audio = extract_audio(self.file_path, audio_output_folder, audio_file)
            if not extracted_audio:
                self.error.emit("Failed to extract audio from the video.")
                return

            # Step 2: Visualize loudness
            self.progress.emit(50)
            visualize_loudness(extracted_audio, threshold_loudness=0.1, output_dir=loudness_output_folder)

            # Step 3: Create video without audio
            video_without_audio = create_video_without_audio(self.file_path, video_output_folder, video_without_audio_file)
            if not video_without_audio:
                self.error.emit("Failed to create video without audio.")
                return

            # Step 4: Perform audio analysis (STFT and MFCC)
            self.progress.emit(75)
            analyze_audio_stft(extracted_audio, stft_output_folder)
            analyze_audio_mfcc(extracted_audio, mfcc_output_folder)

            # Finalize
            self.progress.emit(100)
            self.completed.emit(audio_file, video_without_audio_file)
        except Exception as e:
            self.error.emit(str(e))


class MainApp(QMainWindow):
    COUNTER_FILE = "counter.txt"  # File to store the counter

    def __init__(self):
        super().__init__()
        self.setWindowTitle("AKIRA - Audio & Video Processor")
        self.setGeometry(100, 60, 1500, 900)
        self.setStyleSheet("background-color: #FFFFFF;")

        # Set Window Icon
        icon_path = os.path.join(os.path.dirname(__file__), "AKIRA_LOGO.png")
        if os.path.exists(icon_path):
            app_icon = QtGui.QIcon(icon_path)
            self.setWindowIcon(app_icon)

        # Initialize stacked widget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Initialize pages
        self.main_page = QWidget()
        self.results_page = QWidget()
        self.stacked_widget.addWidget(self.main_page)
        self.stacked_widget.addWidget(self.results_page)

        self.video_counter = self.load_counter()

        # Setup UI for each page
        self.setup_main_page()
        self.setup_results_page()
        # Set the default page to be the results page
        #self.stacked_widget.setCurrentWidget(self.results_page)

    def setup_main_page(self):
        layout = QHBoxLayout(self.main_page)

        # Sidebar
        sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_widget.setStyleSheet("background-color: #F1FBEF; border-radius: 10px;")
        sidebar_layout.setAlignment(Qt.AlignTop)
        sidebar_layout.setContentsMargins(20, 20, 20, 20)
        sidebar_layout.setSpacing(20)
        sidebar_widget.setFixedWidth(440)

        logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), "AKIRA_LOGO.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path).scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_label.setPixmap(pixmap)
        else:
            logo_label.setText("AKIRA LOGO")
        sidebar_layout.addWidget(logo_label, alignment=Qt.AlignCenter)

        self.upload_btn = QPushButton("UPLOAD")
        self.upload_btn.setFont(QFont("Arial", 14, QFont.Bold))
        self.upload_btn.setFixedSize(200, 60)
        self.upload_btn.setStyleSheet("background-color: #1A3C10; color: #FFFFFF; border-radius: 10px;")
        self.upload_btn.clicked.connect(self.upload_video)
        self.upload_btn.clicked.connect(self.start_extraction)
        sidebar_layout.addWidget(self.upload_btn, alignment=Qt.AlignCenter)

        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedWidth(400)

        # Modern styling
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #5e5e5e;
                border-radius: 10px;
                text-align: center;
                background-color: #f3f3f3;
            }
            QProgressBar::chunk {
                background-color: #78D35F; 
                width: 20px;
                margin: 0.5px;
                border-radius: 5px;
            }
        """)
        self.progress_bar.setVisible(False)
        sidebar_layout.addWidget(self.progress_bar)

        layout.addWidget(sidebar_widget)  # Add the sidebar_widget to the layout

        # Content
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_widget.setStyleSheet("background-color: #1A3C10; border-radius: 10px;")
        content_layout.setAlignment(Qt.AlignCenter)
        content_layout.setContentsMargins(50, 20, 50, 20)

        self.title_label = QLabel("AKIRA")
        self.title_label.setFont(QFont("Arial", 70, QFont.Bold))
        self.title_label.setStyleSheet("color: #F1FBEF;")
        self.title_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(self.title_label)
        content_layout.addSpacing(20)

        self.description_box = QLabel(
            "Welcome to the project on \"Extracting Overstimulating Audio Signals from Cartoon Videos Using STFT, MFCC, and VGG16 CNN and Retuning Audio Playback for Child-Friendly Listening.\"\n\n"
            "This research aims to enhance children's audio experiences by analyzing overstimulating audio signals from cartoons. "
            "Using Short-Time Fourier Transform (STFT), Mel Frequency Cepstral Coefficients (MFCC), and VGG16 Convolutional Neural Networks (CNN), "
            "we process and retune audio to create child-friendly listening environments."
        )
        self.description_box.setFont(QFont("Arial", 15))
        self.description_box.setFixedSize(1000, 400)
        self.description_box.setStyleSheet(
            "background-color: #F1FBEF; border-radius: 10px; padding: 20px; color: black;")
        self.description_box.setWordWrap(True)
        self.description_box.setAlignment(Qt.AlignJustify)
        content_layout.addWidget(self.description_box)

        layout.addWidget(content_widget)

    def start_extraction(self):
        self.progress_bar.setVisible(True)

    def end_extraction(self):
        self.progress_bar.setVisible(False)

    def setup_results_page(self):
        layout = QVBoxLayout(self.results_page)

        # Set the background color for the whole page layout
        self.results_page.setStyleSheet("background-color: #1A3C10;")

        # Create a container that will hold all components (results label, containers, and back button)
        outer_container = QWidget()
        outer_container_layout = QVBoxLayout(outer_container)

        # Set the outer container's background color to green
        outer_container.setStyleSheet("background-color: #F1FBEF; border-radius: 10px;")  # Green color

        # Results label
        self.results_label = QLabel("Results")
        self.results_label.setFont(QFont("Arial", 40, QFont.Bold))
        outer_container_layout.addWidget(self.results_label, alignment=Qt.AlignCenter)

        # Horizontal layout to hold the three containers
        containers_layout = QHBoxLayout()
        containers_layout.setSpacing(30)  # Increased spacing between containers
        containers_layout.setContentsMargins(20, 0, 20, 0)  # Add margins around containers

        # Function to create a container (to avoid repetitive code)
        def create_container(title):
            container = QWidget()
            container_layout = QVBoxLayout(container)
            container_label = QLabel(title)
            container_label.setFont(QFont("Arial", 12, QFont.Bold))
            container_label.setAlignment(Qt.AlignCenter)  # Center label text
            container_layout.addWidget(container_label)

            # Add content placeholders (replace with your actual content)
            content_label = QLabel("Content goes here...")  # Example content
            content_label.setStyleSheet("Color: #FFFFFF;")
            content_label.setAlignment(Qt.AlignCenter)
            container_layout.addWidget(content_label)

            # Set container style with extra padding and rounded borders
            container.setStyleSheet("""
                background-color: #1A3C10; 
                border-radius: 10px; 
                padding: 30px;  
                color: #FFFFFF;
            """)
            return container

        # Create the containers using the function
        container1 = create_container("Container 1")
        container2 = create_container("Container 2")
        container3 = create_container("Container 3")

        # Add the containers to the containers_layout
        containers_layout.addWidget(container1)
        containers_layout.addWidget(container2)
        containers_layout.addWidget(container3)

        # Add the containers_layout to the outer_container layout
        outer_container_layout.addLayout(containers_layout)

        # Back button
        self.back_button = QPushButton("Back to Main Menu")
        self.back_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.back_button.setFixedSize(300, 60)
        self.back_button.setStyleSheet("background-color: #1A3C10; color: #FFFFFF; border-radius: 10px;")
        self.back_button.clicked.connect(self.go_to_main_page)
        self.back_button.clicked.connect(self.end_extraction)
        outer_container_layout.addWidget(self.back_button, alignment=Qt.AlignCenter)

        # Add the outer_container to the main layout
        layout.addWidget(outer_container)

    def upload_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Video", "", "Video Files (*.mp4)")
        if file_path:
            self.progress_bar.setValue(0)

            # Start processing in a separate thread
            self.thread = ProcessingThread(file_path, self.video_counter)
            self.thread.progress.connect(self.progress_bar.setValue)
            self.thread.completed.connect(self.on_processing_complete)
            self.thread.error.connect(self.on_processing_error)
            self.thread.start()

    def on_processing_complete(self, audio_path, video_path):
        self.video_counter += 1
        self.save_counter()
        #self.results_label.setText(f"Processing complete!\nAudio saved at: {audio_path}\nVideo saved at: {video_path}")
        self.stacked_widget.setCurrentWidget(self.results_page)

    def on_processing_error(self, error_message):
        QMessageBox.critical(self, "Error", error_message)

    def go_to_main_page(self):
        self.stacked_widget.setCurrentWidget(self.main_page)

    def load_counter(self):
        if os.path.exists(self.COUNTER_FILE):
            with open(self.COUNTER_FILE, "r") as f:
                return int(f.read().strip())
        return 1

    def save_counter(self):
        with open(self.COUNTER_FILE, "w") as f:
            f.write(str(self.video_counter))


if __name__ == "__main__":
    app = QApplication([])
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
