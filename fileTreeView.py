from PySide6.QtWidgets import QWidget , QTreeView , QVBoxLayout , QHeaderView , QApplication
from PySide6.QtCore  import QDir, Signal
from customFileSystemModel import CustomDirectoryModel
import os


class DirectoryTreeViewWidget(QWidget):
    #Signals
    
    file_double_clicked = Signal(str)
    folder_double_clicked = Signal(str)
    def __init__(self ,root_directory = QDir.rootPath()): 
        super().__init__()
        self.setWindowTitle("File Tree View")        
        
        self.file_system_model = CustomDirectoryModel()
        self.file_system_model.setRootPath(root_directory)
        
        self.file_tree_view = QTreeView(self)
        self.file_tree_view.setModel(self.file_system_model)
        self.file_tree_view.setRootIndex(self.file_system_model.index(root_directory))

        
        for i in range(1, self.file_system_model.columnCount()): # Hide all columns except the first one
            self.file_tree_view.hideColumn(i)
        
        self.file_tree_view.setHeaderHidden(True)
        
        self.file_system_model.setFilter( QDir.NoDotAndDotDot | QDir.AllDirs)  

        header = self.file_tree_view.header()
        
        # Disable user resizing
        header.setSectionsMovable(False)  # Prevents dragging columns
               
        
        v_layout = QVBoxLayout(self)
        v_layout.addWidget(self.file_tree_view)
        self.setLayout(v_layout)
        
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        
        
        #Connection Double Clicked
        self.file_tree_view.doubleClicked.connect(self.onDoubleClicked)
        
    
    # Defining the slots
    def refreshView(self):
        current_directory = self.getCurrentDirectory()
        self.file_tree_view.setRootIndex(current_directory)
        
        
    def traverseDirectoryTree(self , directory):
     
        root_path = QDir(self.file_system_model.rootPath())
        print('root_path:', root_path.absolutePath())
        print('directory:', directory)

        relative_path = root_path.relativeFilePath(directory)
        print('relative_path:', relative_path)

        traversal = []

        current_path = root_path

        parts = relative_path.split(QDir.separator())  # Use QDir.separator() for cross-platform compatibility

        for part in parts:
            if part:  
                current_path.cd(part)  
                traversal.append(current_path.absolutePath())  

        print('traversal:', traversal)

        for path in traversal:
            index = self.file_system_model.index(path)
            self.file_tree_view.setExpanded(index, True)

    def getCurrentDirectory(self):
        return self.file_tree_view.rootIndex()
    
    def onDoubleClicked(self , index):
        path = self.file_system_model.filePath(index)
        if self.file_system_model.isDir(index):
            self.folder_double_clicked.emit(path)
        else:
            self.file_double_clicked.emit(path)
        
        
        
        
        
        
        
        
        
        

