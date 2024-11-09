from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSlider, QLabel
from PySide6.QtCore import Qt , Signal
from PySide6.QtGui import QIcon
from catchExecptions import catch_exceptions

class StatusBarWidget(QWidget):
    # Signals
    icon_size       = Signal(int)  
    toggle_left_sidebar = Signal()
    
    @catch_exceptions
    def __init__(self, parent=None):
        super().__init__(parent)

        
        layout = QHBoxLayout(self)

       
        self.toggle_bookmark_button = QPushButton("")
        self.toggle_bookmark_button.setIcon(QIcon("icons/bookmark-fill.svg"))
        self.toggle_bookmark_button.setToolTip("Toggle Bookmark Sidebar")

        
        self.status_label = QLabel("Ready")  
        self.status_label.setAlignment(Qt.AlignCenter)  

        # Create a slider for adjusting icon sizes
        self.icon_size_slider = QSlider(Qt.Horizontal)
        self.icon_size_slider.setRange(16, 128)  
        self.icon_size_slider.setValue(64)  
        self.icon_size_slider.setFixedWidth(150)
        
        
        # Add widgets to the layout
        layout.addWidget(self.toggle_bookmark_button)
        layout.addStretch()  
        layout.addWidget(self.status_label)  
        layout.addStretch()  
        layout.addWidget(self.icon_size_slider)  

        # Set the layout for this widget
        self.setLayout(layout)

        # Connect signals to slots
        self.toggle_bookmark_button.clicked.connect(lambda : self.toggle_left_sidebar.emit())
        self.icon_size_slider.valueChanged.connect(lambda int : self.icon_size.emit(int))
        
        
    @catch_exceptions
    def updateStatus(self, message='ready'):
        """updates the status message shown in the status bar."""
        self.status_label.setText(message)  # Update the status message
