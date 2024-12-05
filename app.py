import sys
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from visualizer import run_visualizer  # Import the function from the second file

# Global variable for the selected audio file
AUDIO_FILE = None
visualizer_thread = None  # To ensure only one thread runs the visualizer

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set the window title
        self.setWindowTitle("Music Visualizer")
        self.setFixedSize(800,300)

        # Create a vertical layout
        layout = QVBoxLayout()

        # Add a welcome text
        self.welcome_label = QLabel("Welcome to the Music Visualizer!")
        self.welcome_label.setFont(QFont("Arial", 16))  # Set larger font
        #self.welcome_label.setFixedSize(400, 100)
        layout.addWidget(self.welcome_label,alignment = Qt.AlignHCenter)

        # Add a file upload button
        self.upload_button = QPushButton("Upload File")
        self.upload_button.setFont(QFont("Arial", 16))  # Set larger font
        self.upload_button.setFixedSize(400, 50)  # Make button larger
        self.upload_button.setStyleSheet("""
            background-color: #3498db;
            color: white;
            border-radius: 8px;
        """)
        self.upload_button.clicked.connect(self.upload_file)
        layout.addWidget(self.upload_button,alignment=Qt.AlignHCenter)

        # Add a confirmation button
        self.confirm_button = QPushButton("Confirm and Start")
        self.confirm_button.setFont(QFont("Arial", 14))  # Set larger font
        self.confirm_button.setFixedSize(400, 50)  # Make button larger
        self.confirm_button.clicked.connect(self.confirm_action)
        layout.addWidget(self.confirm_button,alignment=Qt.AlignHCenter)

        # Set the layout
        self.setLayout(layout)

    def upload_file(self):
        global AUDIO_FILE
        # Open a file dialog to upload a file
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Audio Files (*.wav)")
        if file_name:
            AUDIO_FILE = file_name
            self.welcome_label.setText(f"Selected File: {AUDIO_FILE}")

    def confirm_action(self):
        global AUDIO_FILE, visualizer_thread
        if AUDIO_FILE:
            if visualizer_thread is None or not visualizer_thread.is_alive():
                self.welcome_label.setText("Starting the visualizer...")
                self.confirm_button.setEnabled(False)  # Disable button to prevent multiple threads
                visualizer_thread = threading.Thread(target=self.start_visualizer, daemon=True)
                visualizer_thread.start()
            else:
                self.welcome_label.setText("Visualizer is already running!")
        else:
            self.welcome_label.setText("Please upload an audio file first!")
        self.hide()

    def start_visualizer(self):
        global AUDIO_FILE
        run_visualizer(AUDIO_FILE)  # Call the visualizer function
        self.confirm_button.setEnabled(True)  # Re-enable the button after the visualizer ends
        self.welcome_label.setText("Visualizer finished. Ready for another file!")
    
    def hide_window(self):
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
