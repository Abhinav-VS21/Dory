from PySide6.QtWidgets import QApplication, QListView, QVBoxLayout, QPushButton, QWidget, QFileDialog ,QFileSystemModel
import sys

class FileExplorer(QWidget):
    def __init__(self):
        super(FileExplorer, self).__init__()

        # Create a QFileSystemModel
        self.file_system_model = QFileSystemModel()
        self.file_system_model.setRootPath('/')  # Initial root path

        # Create a QListView
        self.list_view = QListView(self)
        self.list_view.setModel(self.file_system_model)
        self.list_view.setRootIndex(self.file_system_model.index('/'))  # Set initial root index

        # Button to change root directory
        self.change_dir_button = QPushButton("Change Directory")
        self.change_dir_button.clicked.connect(self.change_directory)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.list_view)
        layout.addWidget(self.change_dir_button)
        self.setLayout(layout)

    def change_directory(self):
        # Open a file dialog to select a new directory
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            # Get the index for the new directory and update the root index
            new_index = self.file_system_model.index(directory)
            if new_index.isValid():
                self.list_view.setRootIndex(new_index)  # Change the root index of the view

if __name__ == '__main__':
    app = QApplication(sys.argv)
    explorer = FileExplorer()
    explorer.setWindowTitle('Dynamic File Explorer')
    explorer.resize(400, 300)
    explorer.show()
    sys.exit(app.exec_())
