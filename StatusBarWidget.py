from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSlider, QLabel
from PySide6.QtCore import Qt

class StatusBarWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create layout
        layout = QHBoxLayout(self)

        # Create buttons
        self.toggle_bookmark_button = QPushButton("Toggle Bookmark/TreeView")
        self.hide_sidebar_button = QPushButton("Hide Sidebar")

        # Create a label to show status messages
        self.status_label = QLabel("Ready")  # Default status message
        self.status_label.setAlignment(Qt.AlignCenter)  # Center align label

        # Create a slider for adjusting icon sizes
        self.icon_size_slider = QSlider(Qt.Horizontal)
        self.icon_size_slider.setRange(16, 128)  # Set range for icon sizes
        self.icon_size_slider.setValue(64)  # Default value
        self.icon_size_slider.setFixedWidth(150)  # Optional: Set a fixed width for the slider

        # Add widgets to the layout
        layout.addWidget(self.toggle_bookmark_button)
        layout.addWidget(self.hide_sidebar_button)
        layout.addStretch()  # Add stretchable space between buttons and label
        layout.addWidget(self.status_label)  # Center label
        layout.addStretch()  # Add stretchable space between label and slider
        layout.addWidget(self.icon_size_slider)  # Right align slider

        # Set the layout for this widget
        self.setLayout(layout)

    def update_status(self, message):
        self.status_label.setText(message)  # Update the status message


# from PySide6.QtWidgets import QApplication, QMainWindow

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         # Set window title and size
#         self.setWindowTitle("My Application")
#         self.setGeometry(100, 100, 800, 600)

#         # Create an instance of StatusBarWidget
#         self.status_bar_widget = StatusBarWidget()
        
#         # Add the StatusBarWidget at the bottom of the main window
#         self.setCentralWidget(self.status_bar_widget)

#         # Example of updating the status bar message
#         self.status_bar_widget.update_status("Ready")

# if __name__ == "__main__":
#     import sys

#     app = QApplication(sys.argv)

#     # Create and show the main window
#     window = MainWindow()
#     window.show()

#     # Run the application
#     sys.exit(app.exec())