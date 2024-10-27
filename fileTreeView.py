from PySide6.QtWidgets import QWidget , QTreeView , QVBoxLayout , QHeaderView , QApplication
from PySide6.QtCore  import QDir
from customFileSystemModel import CustomFileSystemModel
import os


class FileTreeViewWidget(QWidget):
    def __init__(self ,root_directory = QDir.homePath()): 
        super().__init__()
        self.setWindowTitle("File Tree View")
        root_directory = QDir.homePath()  #change this for root directory
        
        
        self.file_system_model = CustomFileSystemModel()
        self.file_system_model.setRootPath(root_directory)
        
        self.file_tree_view = QTreeView(self)
        self.file_tree_view.setModel(self.file_system_model)
        self.file_tree_view.setRootIndex(self.file_system_model.index(root_directory))

        
        for i in range(1, self.file_system_model.columnCount()):
            self.file_tree_view.hideColumn(i)
        
        self.file_tree_view.setHeaderHidden(True)
        
        
        self.file_system_model.setFilter( QDir.NoDotAndDotDot | QDir.AllDirs)  

        
        header = self.file_tree_view.header()
        
        # Disable user resizing
        header.setSectionsMovable(False)  # Prevents dragging columns
        header.setStretchLastSection(False)  # Prevents automatic stretching of the last column
        
        
        v_layout = QVBoxLayout(self)
        v_layout.addWidget(self.file_tree_view)
        self.setLayout(v_layout)
        
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        
    def refreshView(self):
        current_directory = self.getCurrentDirectory()
        self.file_tree_view.setRootIndex(current_directory)
        
        
        
    def expandTreeView(self , directory):
        
        # Split the directory path into parts, assuming `directory` is an absolute path
        
        root_path = QDir(self.file_system_model.rootPath())
        print('root_path:', root_path.absolutePath())
        print('directory:', directory)

        # Get the relative path from root_path to the directory
        relative_path = root_path.relativeFilePath(directory)
        print('relative_path:', relative_path)

        # Initialize traversal array
        traversal = []

        # Start with the root directory
        current_path = root_path

        # Split the relative path into parts using '/' as the delimiter
        parts = relative_path.split(QDir.separator())  # Use QDir.separator() for cross-platform compatibility

        # Traverse the parts and build the absolute paths
        for part in parts:
            if part:  # Skip any empty parts
                current_path.cd(part)  # Change to the directory
                traversal.append(current_path.absolutePath())  # Append the absolute path

        print('traversal:', traversal)

        # Expand the tree view
        for path in traversal:
            index = self.file_system_model.index(path)
            self.file_tree_view.setExpanded(index, True)


        
        
        
        
        
        
        
        
        
        

