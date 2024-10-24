from PySide6.QtWidgets import QWidget ,QFileSystemModel, QTreeView , QVBoxLayout , QHeaderView
from PySide6.QtCore  import QDir, QTimer, Qt


class FileTreeViewWidget(QWidget):
    def __init__(self , maxColumnWidth = 300):
        super().__init__()
        self.setWindowTitle("File Tree View")
        self.maxColumnWidth = maxColumnWidth
        
        self.fileSystemModel = QFileSystemModel()
        self.homeDirectory = QDir.homePath()  #change this for root directory
        
        self.fileSystemModel.setRootPath(self.homeDirectory)
        
        self.fileTreeView = QTreeView(self)
        self.fileTreeView.setModel(self.fileSystemModel)
        self.fileTreeView.setRootIndex(self.fileSystemModel.index(self.homeDirectory))

        
        self.fileTreeView.hideColumn(1)
        self.fileTreeView.hideColumn(2)
        self.fileTreeView.hideColumn(3)
        
        
        header = self.fileTreeView.header()
        
        # Disable user resizing
        header.setSectionsMovable(False)  # Prevents dragging columns
        header.setStretchLastSection(False)  # Prevents automatic stretching of the last column
        
        
        vLayout = QVBoxLayout(self)
        vLayout.addWidget(self.fileTreeView)
        self.setLayout(vLayout)
        
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        
        
        # signal for clicking directory 
        
        
        
        
        
        
        
        

