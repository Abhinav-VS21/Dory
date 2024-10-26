import sys
import os

from PySide6.QtWidgets import QWidget, QVBoxLayout, QListView , QApplication , QMainWindow , QFileSystemModel
from PySide6.QtGui import  QIcon , QStandardItemModel
from PySide6.QtCore import QDir , QTimer
from customFileSystemModel import CustomFileSystemModel



class IconListViewerWidget(QWidget):
    def __init__(self, directory="/home/MissShah_21"):
        super().__init__()
        #verifing the directory
        print(f"Directory exists: {os.path.exists(directory)}")

        
        # Set up the model for the QListView
        self.model = CustomFileSystemModel()
        self.model.setRootPath(directory)
        self.model.setFilter(QDir.Files | QDir.NoDotAndDotDot | QDir.AllDirs)
        
        # Create a list view to show icons
        self.icon_list_view = QListView(self)
        self.icon_list_view.setModel(self.model)

        # Set the root index for the directory
        root_index = self.model.index(directory)
        self.icon_list_view.setRootIndex(root_index)

        # Debugging: Print the number of items in the directory
        item_count = self.model.rowCount(root_index)
        print(f"Number of items in '{directory}': {item_count}")

        layout = QVBoxLayout(self)
        layout.addWidget(self.icon_list_view)

        
    def setNewRootIndex(self , directory):
        newRootIndex = self.model.index(directory)
        self.icon_list_view.setRootIndex(newRootIndex)
        print('The new root index is set to: ',newRootIndex)
        
    def setIconView(self):
        self.icon_list_view.setViewMode(QListView.IconMode)
        self.icon_list_view.setSpacing(5)          
        
    def setListView(self):
        self.icon_list_view.setViewMode(QListView.ListMode)
        self.icon_list_view.setSpacing(5)  
        
    def refreshView(self):
        current_directory = self.icon_list_view.rootIndex()
        self.icon_list_view.setRootIndex(current_directory)
        


'''debugging'''
# app = QApplication(sys.argv)
# icon_viewer = IconViewer()
# icon_viewer.setWindowTitle('Icon Viewer')
# icon_viewer.resize(400, 30    0)
# icon_viewer.show()
# app.exec()