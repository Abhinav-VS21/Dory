from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QApplication
from DirectoryCompleter import DirectoryCompleter  # Assuming your class is in this file

class SearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Set up the dialog layout
        self.setWindowTitle("Search Dialog")
        self.setGeometry(300, 200, 400, 200)
        layout = QVBoxLayout()

        # Create the input field for directory search
        self.search_dir_input = QLineEdit()
        self.search_dir_input.setPlaceholderText("Enter directory path...")

        # Create an instance of DirectoryCompleter and set it to the QLineEdit
        self.directory_completer = DirectoryCompleter(self.search_dir_input, default_path='/home/MissShah_21/Documents')
        self.search_dir_input.textChanged.connect(self.directory_completer.updateCompleter)

        # Add the QLineEdit to the dialog layout
        layout.addWidget(self.search_dir_input)

        # Create a button to simulate searching
        search_button = QPushButton("Search")
        layout.addWidget(search_button)

        # Set the layout for the dialog
        self.setLayout(layout)

# Example of running the application with the dialog
if __name__ == "__main__":
    app = QApplication([])

    # Create and show the dialog
    dialog = SearchDialog()
    dialog.exec()
