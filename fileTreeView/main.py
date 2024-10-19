from PySide6.QtCore import QDir , QTimer
from PySide6.QtWidgets import QApplication , QWidget , QFileSystemModel 
import sys 
from fileTreeView_ui import Ui_fileTreeViewWidget

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

        # setting the model to the tree view with the index as user directory
        self.fileTreeUI.fileTreeView.setModel(self.fileSystemModel)
        self.fileTreeUI.fileTreeView.setRootIndex(self.fileSystemModel.index(self.homeDirectory))
        
               
        
        # connect the clicked signal slot to the custom slot 
        # self.fileTreeUI.fileTreeView.clicked.connect(self.onTreeViewNameColumnChange)
        
        
        self.fileTreeUI.fileTreeView.expanded.connect(self.resizeNameColumn)
        self.fileTreeUI.fileTreeView.collapsed.connect(self.resizeNameColumn)
        
        
    def resizeNameColumn(self):
        QTimer.singleShot(1,self.resizeColumn(0))
        
        
    def resizeColumn(self , index):
        self.fileTreeUI.fileTreeView.resizeColumnToContents(index)
    
        
    


app = QApplication(sys.argv)
window = FileWindow()
#window.showMaximized()
window.show()
app.exec()
    