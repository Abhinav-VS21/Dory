from PySide6.QtWidgets import QLineEdit , QCompleter, QApplication , QWidget , QHBoxLayout 
from PySide6.QtCore import QDir , Qt , Signal , QStringListModel
from PySide6.QtCore import Signal
from DirectoryCompleter import DirectoryCompleter

class AddressBar(QLineEdit):
    address_path_changed = Signal(str)  # Custom signal to emit when path is changed

    def __init__(self, default_path="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Enter directory path...")
        self.setText(default_path)
        
        #Initializing Completer
        self.completer = DirectoryCompleter(self)
        # Connect to the method to navigate when Enter is pressed
        self.returnPressed.connect(self.emit_path)

    def emit_path(self):
        path = self.text()
        if QDir(path).exists():
            self.address_path_changed.emit(path)
        else:
            self.setText("Invalid Path")
            self.selectAll()        

# debug 

# app = QApplication([])
# window = QWidget()
# window.setWindowTitle("Address Bar Test")
# window.resize(400, 100)
# address_bar = AddressBar()
# h_layout = QHBoxLayout(window)
# h_layout.addWidget(address_bar)
# window.setLayout(h_layout)
# window.show()
# app.exec()
