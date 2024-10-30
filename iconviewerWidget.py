
import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListView , QApplication , QMainWindow , QFileSystemModel
from PySide6.QtGui import  QIcon , QStandardItemModel
from PySide6.QtCore import QDir , QTimer , Signal , QSize
from customFileSystemModel import CustomFileSystemModel
from WrappingItemDelegate import TextWrappingIconDelegate



class IconListViewerWidget(QWidget):
    # Signals
    file_double_clicked = Signal(str)
    folder_double_clicked = Signal(str)
    
    def __init__(self, root_directory=QDir.homePath()):
        super().__init__()
               
        
        self.directory_model = CustomFileSystemModel()
        self.directory_model.setRootPath(root_directory)
        self.directory_model.setFilter(QDir.Files | QDir.NoDotAndDotDot | QDir.AllDirs)
        
        self.icon_list_view = QListView(self)
        self.icon_list_view.setModel(self.directory_model)

        root_index = self.directory_model.index(root_directory)
        self.icon_list_view.setRootIndex(root_index)     

        layout = QVBoxLayout(self)
        layout.addWidget(self.icon_list_view)
        

        # defining connections
        self.icon_list_view.doubleClicked.connect(self.onDoubleClicked)
        
        
    # Defining the slots
    def onDoubleClicked(self, index):
        if not index.isValid():
            print("Invalid index in iconViewerWidget")
            return
        path = self.directory_model.filePath(index)
        if self.directory_model.isDir(index):
            self.folder_double_clicked.emit(path)
        else:
            self.file_double_clicked.emit(path)
            
    
    def setNewRootIndex(self , directory):
        print('Setting new root index to: ',directory)  
        newRootIndex = self.directory_model.index(directory)
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
        self.icon_list_view.setRootIndex(self.directory_model.index(current_dir_path))
        
    def getCurrentDirectoryPath(self):
        return self.directory_model.filePath(self.icon_list_view.rootIndex())
    
    

'''debugging'''
# app = QApplication([])
# icon_viewer = IconListViewerWidget()
# icon_viewer.setWindowTitle('Icon Viewer')
# icon_viewer.show()
# icon_viewer.setIconView()
# app.exec()