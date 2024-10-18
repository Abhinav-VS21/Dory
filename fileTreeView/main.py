from PySide6.QtCore import QDir
from PySide6.QtWidgets import QApplication , QWidget , QFileSystemModel 
import sys 
from fileTreeView.fileTreeView_ui import Ui_fileTreeViewWidget

class FileWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Tree View")
        
        # ui object that displays the file tree view
        self.fileTreeUI = Ui_fileTreeViewWidget()         
        self.fileTreeUI.setupUi(self)
        
        
        # initilizing file system model with user directory
        self.fileSystemModel = QFileSystemModel()
        
        self.homeDirectory = QDir.homePath()
        self.fileSystemModel.setRootPath(self.homeDirectory)   # setting the root path of the model to the user directory
        self.fileSystemModel.setFilter(QDir.NoDotAndDotDot | QDir.AllDirs) #filter to show only directories


        # setting the model to the tree view with the index as user directory
        self.fileTreeUI.fileTreeView.setModel(self.fileSystemModel)
        self.fileTreeUI.fileTreeView.setRootIndex(self.fileSystemModel.index(self.homeDirectory))
        
        self.fileTreeUI.fileTreeView.header().setVisible(False) 
        
        # hiding all columns
        columnCount = self.fileSystemModel.columnCount()
        for i in range(1,columnCount):
            self.fileTreeUI.fileTreeView.hideColumn(i)
        


app = QApplication(sys.argv)
window = FileWindow()
window.show()
app.exec()
    