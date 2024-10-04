from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow , QWidget , QVBoxLayout , QHBoxLayout , QGridLayout , QStackedLayout , QPushButton , QTabWidget
from PyQt5.QtGui import QColor , QPalette

colors = ['maroon','pink','orange']

class colorWidget(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)
        
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
         
        self.setWindowTitle("My App")
        
        pagelayout = QVBoxLayout()
        btnlayout = QHBoxLayout()
        self.colorLayout = QStackedLayout()
        
        
        pagelayout.addLayout(self.colorLayout)   
        pagelayout.addLayout(btnlayout)
        
        for color in colors:
            self.colorLayout.addWidget(colorWidget(color))
            
        def create_button(color, slot, index):
            btn = QPushButton(color)
            btn.pressed.connect(slot)
            btnlayout.addWidget(btn)
            self.colorLayout.addWidget(colorWidget(color))
            return btn
        
        self.buttons = [
            create_button("red", self.activate_tab_1, 0),
            create_button("green", self.activate_tab_2, 1),
            create_button("yellow", self.activate_tab_3, 2)
        ]
        
        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)

    def activate_tab_1(self):
        self.colorLayout.setCurrentIndex(0)

    def activate_tab_2(self):
        self.colorLayout.setCurrentIndex(1)

    def activate_tab_3(self):
        self.colorLayout.setCurrentIndex(2)
        
class MainGridWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        
        layout = QVBoxLayout()
        
        layout = QGridLayout()

        layout.addWidget(colorWidget('red'), 0, 0)
        layout.addWidget(colorWidget('green'), 1, 0)
        layout.addWidget(colorWidget('blue'), 1, 1)
        layout.addWidget(colorWidget('purple'), 2, 1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)     
        
class MainStackWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        
        layout = QStackedLayout()
        
        for color in colors:
            layout.addWidget(colorWidget(color))
            
        widget = QWidget()
        widget.setLayout(layout)
        layout.setCurrentIndex(2)
        self.setCentralWidget(widget)
        
        
        
class MainTabWidgetWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("tab window")
        
        tabWiget = QTabWidget()
        tabWiget.setTabPosition(QTabWidget.South)
        tabWiget.setMovable(True)
        
        for color in colors:
            tabWiget.addTab(colorWidget(color), color)
        
        self.setCentralWidget(tabWiget)
        
app = QApplication([])

window = MainTabWidgetWindow()
window.show()

app.exec()