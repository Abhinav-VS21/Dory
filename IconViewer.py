import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListView , QApplication , QMainWindow , QFileSystemModel
from PySide6.QtGui import  QIcon , QStandardItemModel
from PySide6.QtCore import QDir , QTimer , Signal , QSize
from customFileSystemModel import CustomDirectoryModel

class FileListViewer(QListView):
    #Signals
    file_double_clicked = Signal(str)
    folder_double_clicked = Signal(str)
    
    
    def __init__(self, root_directory = QDir.homePath()) -> None:
        super().__init__()
        
        
        # Setting up the directory model
        self.directory_model = CustomDirectoryModel()
        self.directory_model.setRootPath(root_directory)
        self.directory_model.setFilter(QDir.Files | QDir.NoDotAndDotDot | QDir.AllDirs)
        
        # Setting up the file list view
        self.setModel(self.directory_model)
        self.setRootIndex(self.directory_model.index(root_directory))
        
        
        # Defining connections
        self.doubleClicked.connect(self.onDoubleClicked)
        
    # Defining the slots
    def onDoubleClicked(self, index):
        if not index.isValid():
            print("Invalid index in FileListWidget")
            return
        path = self.directory_model.filePath(index)
        if self.directory_model.isDir(index):
            self.folder_double_clicked.emit(path)
        else:
            self.file_double_clicked.emit(path)
            
    def setNewRootIndex(self, directory : str):
        
        # Debugging
        print('Setting new root index to: ',directory) 
         
        newRootIndex = self.directory_model.index(directory)
        if not newRootIndex.isValid():
            print('The new root index is not valid')
            return
        
        self.setRootIndex(newRootIndex)
        print('The new root index is set to: ',newRootIndex)
        
    def setIconView(self):
        self.setViewMode(QListView.IconMode)
        self.setResizeMode(QListView.Adjust)
        self.setWordWrap(True)
        self.refreshView()
        
    def setListView(self):
        self.setViewMode(QListView.ListMode)
        self.setResizeMode(QListView.Adjust)
        self.setWordWrap(True)
        self.refreshView()
        
    def refreshView(self):
        current_dir_path= self.getCurrentDirectoryPath()
        self.setRootIndex(self.directory_model.index(current_dir_path))
        
    def getCurrentDirectoryPath(self):
        return self.directory_model.filePath(self.rootIndex())
    