import sys

from PyQt5.QtCore import Qt , QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QSlider,
    QSpinBox,
    QWidget,
    QVBoxLayout
    
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        widget = QCheckBox("This is a checkbox")
        widget.setCheckState(Qt.Checked)
        # widget.setTristate(True)
        widget.stateChanged.connect(self.checkStateChanged)
        
        self.setCentralWidget(widget)
        
        
    def checkStateChanged(self,s):
        print(s == Qt.Checked)
        print(s)
    
    

class comboBoxWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        
        # setting Qcombobox
        self.widget = QComboBox()
        self.widget.addItems([str(x) for x in range(1,11)])
        self.widget.setEditable(True)
        self.widget.setInsertPolicy(QComboBox.InsertAtCurrent)
        
        
        self.setCentralWidget(self.widget) # setting widget to central widget
        
        #handeling combobox signals 
        self.widget.currentIndexChanged.connect(self.indexChanged)
        self.widget.currentTextChanged.connect(self.textChanged)
        
        
    def indexChanged(self,i):
        print('index is ' + str(i))
        
    def textChanged(self,t):
        print('text is ' + t)
        

class inputWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        widget = QLineEdit()
        widget.setMaxLength(10)
        widget.setPlaceholderText("Enter your text")

        #widget.setReadOnly(True) # uncomment this to make it read-only

        widget.returnPressed.connect(self.return_pressed)
        widget.selectionChanged.connect(self.selection_changed)
        widget.textChanged.connect(self.text_changed)
        widget.textEdited.connect(self.text_edited)

        self.setCentralWidget(widget)

    def return_pressed(self):
        print("Return pressed!")
        self.centralWidget().setText("BOOM!")

    def selection_changed(self):
        print("Selection changed")
        print(self.centralWidget().selectedText())

    def text_changed(self, s):
        print("Text changed...")
        print(s)

    def text_edited(self, s):
        print("Text edited...")
        print(s)

    
        
            

app = QApplication(sys.argv)
window = inputWindow()
window.show()
app.exec()
