from PySide6.QtWidgets import QWidget , QTreeView , QVBoxLayout , QHeaderView , QApplication
from PySide6.QtCore  import QDir, Signal
from customFileSystemModel import CustomDirectoryModel
import os


class DirectoryTreeView(QTreeView):
    
    #Signals
    file_double_clicked = Signal(str)
    folder_double_clicked = Signal(str)
    
    def __init__(self ,root_directory = QDir.homePath()): 
        super().__init__()
        self.setWindowTitle("File Tree View")        
        
        self.file_system_model = CustomDirectoryModel()
        self.file_system_model.setRootPath(root_directory)
        
        self.setModel(self.file_system_model)
        self.setRootIndex(self.file_system_model.index(root_directory))

        
        for i in range(1, self.file_system_model.columnCount()):
            self.hideColumn(i)
            
        self.setHeaderHidden(True)
        
        self.file_system_model.setFilter( QDir.NoDotAndDotDot | QDir.AllDirs)
        
        
        # Disable user resizing
        header = self.header()
        header.setSectionsMovable(False)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        
        
        #Connection Double Clicked
        self.doubleClicked.connect(self.onDoubleClicked)
        
    # Defining the slots
    def refreshView(self):
        current_directory = self.rootIndex()
        self.setRootIndex(current_directory)
        
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
            self.setExpanded(index, True)
            
    def onDoubleClicked(self , index):
        file_path = self.file_system_model.filePath(index)
        if os.path.isfile(file_path):
            self.file_double_clicked.emit(file_path)
        else:
            self.folder_double_clicked.emit(file_path)
        
    