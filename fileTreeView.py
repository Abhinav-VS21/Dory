from PySide6.QtWidgets import QWidget , QTreeView , QVBoxLayout , QHeaderView
from PySide6.QtCore  import QDir
from customFileSystemModel import CustomFileSystemModel


class FileTreeViewWidget(QWidget):
    def __init__(self ,directory = QDir.homePath()): 
        super().__init__()
        self.setWindowTitle("File Tree View")
        
        
        self.file_system_model = CustomFileSystemModel()
        directory = QDir.homePath()  #change this for root directory
        
        self.file_system_model.setRootPath(directory)
        
        self.file_tree_view = QTreeView(self)
        self.file_tree_view.setModel(self.file_system_model)
        self.file_tree_view.setRootIndex(self.file_system_model.index(directory))

        
        self.file_tree_view.hideColumn(1)
        self.file_tree_view.hideColumn(2)
        self.file_tree_view.hideColumn(3)
        
        
        header = self.file_tree_view.header()
        
        # Disable user resizing
        header.setSectionsMovable(False)  # Prevents dragging columns
        header.setStretchLastSection(False)  # Prevents automatic stretching of the last column
        
        
        v_layout = QVBoxLayout(self)
        v_layout.addWidget(self.file_tree_view)
        self.setLayout(v_layout)
        
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        
        
        
        
        
        
        
        
        
        

