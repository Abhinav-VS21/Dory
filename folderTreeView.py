from PySide6.QtCore import QDir , QTimer
from PySide6.QtWidgets import QApplication , QWidget , QFileSystemModel 
import sys 
from folderTreeView_ui import Ui_folderTreeViewWidget

class FileWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Folder Tree View")
        
        # ui object that displays the file tree view
        self.folderTreeUI = Ui_folderTreeViewWidget()         
        self.folderTreeUI.setupUi(self)
        
        
        # initilizing file system model with user directory
        self.folderSystemModel = QFileSystemModel()
        
        self.homeDirectory = QDir.homePath()
        self.folderSystemModel.setRootPath(self.homeDirectory)   # setting the root path of the model to the user directory

        # setting the model to the tree view with the index as user directory
        self.folderTreeUI.folderTreeView.setModel(self.folderSystemModel)
        self.folderTreeUI.folderTreeView.setRootIndex(self.folderSystemModel.index(self.homeDirectory))
        
               
        # filter to only show directories
        self.folderSystemModel.setFilter(QDir.Dirs | QDir.NoDotAndDotDot)
        # connect the clicked signal slot to the custom slot 
        # self.fileTreeUI.folderTreeView.clicked.connect(self.onTreeViewNameColumnChange)
        
        
        self.folderTreeUI.folderTreeView.expanded.connect(self.resizeNameColumn)
        self.folderTreeUI.folderTreeView.collapsed.connect(self.resizeNameColumn)
        
        
    def resizeNameColumn(self):
        QTimer.singleShot(1,self.resizeColumn(0))
        
        
    def resizeColumn(self , index):
        self.folderTreeUI.folderTreeView.resizeColumnToContents(index)
    