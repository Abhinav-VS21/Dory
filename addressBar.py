from PySide6.QtWidgets import QLineEdit , QCompleter, QApplication , QWidget , QHBoxLayout 
from PySide6.QtCore import QDir , Qt , Signal , QStringListModel
from PySide6.QtCore import Signal

class AddressBar(QLineEdit):
    pathChanged = Signal(str)  # Custom signal to emit when path is changed

    def __init__(self, default_path="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText("Enter directory path...")
        self.setText(default_path)
        
        #Initializing Completer
        self.completer = QCompleter(self)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.setCompleter(self.completer)
        
        # Set a default list of suggestions (you can customize this)
        self.update_completer([default_path, "/home", "/home/user/Documents", "/usr/local"])

        # Connect to the method to navigate when Enter is pressed
        self.returnPressed.connect(self.emit_path)

    def emit_path(self):
        path = self.text()
        if QDir(path).exists():
            self.pathChanged.emit(path)
        else:
            print("Invalid path. Please enter a valid directory.")

    def update_completer(self, paths):
        # Update the completer's model with new paths
        model = QStringListModel(paths)
        self.completer.setModel(model)
# debug 

# app = QApplication([])
# window = QWidget()
# window.setWindowTitle("Address Bar Test")
# window.resize(400, 100)
# address_bar = AddressBar(default_path="/home")
# address_bar.pathChanged.connect(lambda path: print(f"Path changed to: {path}"))
# h_layout = QHBoxLayout(window)
# h_layout.addWidget(address_bar)
# window.setLayout(h_layout)
# window.show()
# app.exec()
