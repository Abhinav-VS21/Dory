from PySide6.QtWidgets import QTreeView , QHeaderView , QFileSystemModel
from PySide6.QtCore  import QDir, Signal
from catchExecptions import catch_exceptions


class DirectoryTree(QTreeView):
    # Signals
    dir_double_clicked = Signal(str)
    
    
    @catch_exceptions
    def __init__(self,root_directory = QDir.homePath()):
        super().__init__()
        self.dir_system_model = QFileSystemModel()
        self.dir_system_model.setRootPath(root_directory)
        
        
        self.setModel(self.dir_system_model)
        self.setRootIndex(self.dir_system_model.index(root_directory))
        
        for i in range(1, self.dir_system_model.columnCount()):
            self.hideColumn(i)
            
        self.dir_system_model.setFilter( QDir.NoDotAndDotDot | QDir.AllDirs)
        
        # Disable user resizing
        header = self.header()
        header.setSectionsMovable(False)
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        
        #Connection Double Clicked
        self.doubleClicked.connect(self.onDoubleClicked)
        
    # Methods
    @catch_exceptions
    def refreshView(self):
        """Refreshes the view to reflect any changes in the current directory."""
        
        self.dir_system_model.setRootPath(self.dir_system_model.rootPath())
        
    @catch_exceptions   
    def traverseDirectoryTree(self , directory):
        """
        Expands the directory tree to show the given directory path.
        
        Args:
            directory (str): The path to the directory to expand to.
        """
        
        root_path = QDir(self.dir_system_model.rootPath())

        relative_path = root_path.relativeFilePath(directory)
        

        traversal = []

        current_path = QDir(root_path)

        parts = relative_path.split(QDir.separator())  # Use QDir.separator() for cross-platform compatibility

        for part in parts:
            if part:  
                current_path.cd(part)  
                traversal.append(current_path.absolutePath())  

        for path in traversal:
            index = self.dir_system_model.index(path)
            self.setExpanded(index, True)
            
    @catch_exceptions        
    def onDoubleClicked(self,index):
        """Handles double-click events on directories."""
         
        dir_path = self.dir_system_model.filePath(index)
        self.dir_double_clicked.emit(dir_path)
        print('emits signal:', dir_path)
    
    #Slots
    
    @catch_exceptions    
    def hideSelf(self):
        """Hides the DirectoryTree widget."""
        self.hide()
     
    @catch_exceptions   
    def showSelf(self):
        """Shows the DirectoryTree widget."""
        self.show()
    



# from PySide6.QtWidgets import QApplication , QMainWindow , QWidget , QVBoxLayout
# if __name__ == "__main__":

#     app = QApplication([])
    
#     main_window = QMainWindow()
#     main_window.setWindowTitle("Directory Tree View")
    
#     central_widget = QWidget()
#     main_layout = QVBoxLayout(central_widget)
    
#     directory_tree = DirectoryTree()
#     main_layout.addWidget(directory_tree)
    
#     main_window.setCentralWidget(central_widget)
#     main_window.resize(800, 600)
#     main_window.show()
    
#     app.exec()