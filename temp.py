from PyQt5.QtWidgets import QApplication, QMainWindow , QPushButton
from PyQt5.QtCore import QSize , Qt
import sys	


class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        
        button = QPushButton("Click Me")
        
        self.setCentralWidget(button)
        
        self.setFixedSize(QSize(480, 320))
        
        
        

app = QApplication(sys.argv)
window = mainWindow()
window.show()

app.exec_()
