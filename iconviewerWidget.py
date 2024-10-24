import sys

from PySide6.QtWidgets import QWidget, QVBoxLayout, QListView , QApplication , QMainWindow
from PySide6.QtGui import QStandardItemModel, QIcon , QStandardItem
from PySide6.QtCore import Qt , QDir


class IconViewer(QWidget):
    def __init__(self, directory):
        super().__init__()
        self.layout = QVBoxLayout(self)

        # Create a list view to show icons
        self.icon_view = QListView(self)
        self.layout.addWidget(self.icon_view)

        # Set up the model for the QListView
        self.model = QStandardItemModel(self.icon_view)
        self.icon_view.setModel(self.model)

        # Populate the list view with icons from the specified directory
        self.populate_file_list(directory)
        

        
    def populate_file_list(self, directory):
        # Create a QDir object for the specified directory
        self.model.clear()
        dir = QDir(directory)

        # Check if the directory exists
        if dir.exists():
            # Get a list of all files in the directory
            file_info = dir.entryInfoList(QDir.Files | QDir.NoDotAndDotDot)

            # Populate the model with the file names and icons
            for info in file_info:
                item = QStandardItem(QIcon(info.filePath()), info.fileName())
                item.setEditable(False)  # Make items non-editable
                self.model.appendRow(item)
        else:
            print(f"The directory '{directory}' does not exist.")
      
            
       
