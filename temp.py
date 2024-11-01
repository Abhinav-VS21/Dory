from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.widget1 = QWidget(self)
        self.widget1.setStyleSheet("background-color: lightblue;")
        
        self.widget2 = QWidget(self)
        self.widget2.setStyleSheet("background-color: lightgreen;")
        
        # Only show the first widget initially
        self.widget1.show()
        self.widget2.hide()
        
        self.toggle_button = QPushButton("Toggle Widget", self)
        self.toggle_button.clicked.connect(self.toggle_widget)

        layout = QVBoxLayout()
        layout.addWidget(self.toggle_button)
        layout.addWidget(self.widget1)
        layout.addWidget(self.widget2)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def toggle_widget(self):
        if self.widget1.isVisible():
            self.widget1.hide()
            self.widget2.show()
        else:
            self.widget1.show()
            self.widget2.hide()

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
