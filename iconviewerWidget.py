import sys
import os

from PySide6.QtWidgets import QWidget, QVBoxLayout, QListView , QApplication , QMainWindow , QFileSystemModel
from PySide6.QtGui import  QIcon , QStandardItemModel
from PySide6.QtCore import QDir , QTimer
from customFileSystemModel import CustomFileSystemModel
# from wrappingItemDelegate import WrappingItemDelegate



class IconListViewerWidget(QWidget):
    def __init__(self, root_directory=QDir.rootPath(),index_directory = QDir.homePath()):
        super().__init__()
        #verifing the directory
        print(f"Directory exists: {os.path.exists(root_directory)}")

        
        # Set up the model for the QListView
        self.model = CustomFileSystemModel()
        self.model.setRootPath(root_directory)
        self.model.setFilter(QDir.Files | QDir.NoDotAndDotDot | QDir.AllDirs)
        
        # Create a list view to show icons
        self.icon_list_view = QListView(self)
        self.icon_list_view.setModel(self.model)

        # Set the root index for the directory
        root_index = self.model.index(root_directory)
        self.icon_list_view.setRootIndex(root_index)

        # Debugging: Print the number of items in the directory
        item_count = self.model.rowCount(root_index)
        print(f"Number of items in '{root_directory}': {item_count}")

        layout = QVBoxLayout(self)
        layout.addWidget(self.icon_list_view)

        
    def setNewRootIndex(self , directory):
        print('Setting new root index to: ',directory)  
        newRootIndex = self.model.index(directory)
        if not newRootIndex.isValid():
            print('The new root index is not valid')
            return
        
        self.icon_list_view.setRootIndex(newRootIndex)
        print('The new root index is set to: ',newRootIndex)
        
    def setIconView(self):
        self.icon_list_view.setViewMode(QListView.IconMode)
        self.icon_list_view.setSpacing(5)
        self.icon_list_view.setWordWrap(True)
        
        
        self.refreshView()    
        
    def setListView(self):
        self.icon_list_view.setViewMode(QListView.ListMode)
        self.icon_list_view.setSpacing(5)  
        self.refreshView()
    
    def refreshView(self):
        current_dir_path= self.getCurrentDirectoryPath()
        self.icon_list_view.setRootIndex(self.model.index(current_dir_path))
        
    def getCurrentDirectoryPath(self):
        return self.model.filePath(self.icon_list_view.rootIndex())

'''debugging'''
# app = QApplication(sys.argv)
# icon_viewer = IconListViewerWidget()
# icon_viewer.setWindowTitle('Icon Viewer')
# icon_viewer.show()
# icon_viewer.setIconView()
# app.exec()