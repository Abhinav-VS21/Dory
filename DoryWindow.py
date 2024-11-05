from PySide6.QtWidgets import QMainWindow , QVBoxLayout , QHBoxLayout , QWidget , QSplitter , QApplication 
from PySide6.QtCore import Qt , QDir
from AddressBarWidget import AddressBarWidget
from BookmarkTree import BookmarkTree
from DirectoryTree import DirectoryTree
from FileViewerWidget import FileListViewer
from MenuBarWidget import MenuBar
from SearchInputWidget import SearchInputWidget
from SearchResultWidget import SearchResultWidget
from SearchThread import SearchThread
from StatusBarWidget import StatusBarWidget
from catchExecptions import catch_exceptions
import os
import subprocess
import platform
import shutil

class DoryWindow(QMainWindow):
    def __init__(self , init_root_dir = QDir.homePath() , current_dir = QDir.homePath()):
        super().__init__()

        self.setWindowTitle("Dory")
        self.setMinimumSize(800 , 600)
        self.init_root_dir = init_root_dir
        self.current_dir = current_dir

        self.initLayout()
        self.fileConnections()
        self.directoryConnections()
        
    def initLayout(self):
        # Creating widgets
        
        self.menu_bar               = MenuBar()
        self.address_bar_widget     = AddressBarWidget()
        self.directory_tree         = DirectoryTree(root_directory=self.init_root_dir)
        self.bookmark_tree          = BookmarkTree(bookmarks_file="bookmarks.json")
        self.file_viewer            = FileListViewer(root_directory=self.init_root_dir)
        self.search_input           = SearchInputWidget()
        self.search_result          = SearchResultWidget()
        self.status_bar_widget      = StatusBarWidget()
        
        
        # Set size of the address bar
        height = 40
        self.address_bar_widget.setFixedHeight(height)
        self.status_bar_widget.setFixedHeight(height)
        
        margin = 1
        # Setting the main layout
        directory_bookmark_widget = QWidget()
        directory_bookmark_layout = QHBoxLayout()
        directory_bookmark_layout.setContentsMargins(margin,margin,margin,margin)
        directory_bookmark_widget.setLayout(directory_bookmark_layout)
        directory_bookmark_layout.addWidget(self.directory_tree)
        directory_bookmark_layout.addWidget(self.bookmark_tree)
        
        file_result_widget = QWidget()
        file_result_layout = QHBoxLayout()
        file_result_layout.setContentsMargins(margin , margin , margin , margin)
        file_result_widget.setLayout(file_result_layout)
        file_result_layout.addWidget(self.file_viewer)
        file_result_layout.addWidget(self.search_result)
        
        input_search_widget = QWidget()
        input_search_layout = QVBoxLayout()
        input_search_layout.setContentsMargins(margin , margin , margin , margin)
        input_search_widget.setLayout(input_search_layout)
        input_search_layout.addWidget(self.search_input)
        input_search_layout.addWidget(file_result_widget)
        
        splitter = QSplitter()
        splitter.setHandleWidth(8)
        splitter.setOrientation(Qt.Horizontal)
        splitter.addWidget(directory_bookmark_widget)
        splitter.addWidget(input_search_widget)
        
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(margin , margin , margin , margin)
        central_widget.setLayout(main_layout)
        main_layout.addWidget(self.address_bar_widget)
        main_layout.addWidget(splitter)  
        main_layout.addWidget(self.status_bar_widget)      
        
        
        # Setting up the main window
        self.setCentralWidget(central_widget)
        self.setMenuBar(self.menu_bar)
        
        # Setting up the initial stage
        self.search_input.setVisible(False)
        self.search_result.setVisible(False)
        self.bookmark_tree.setVisible(False)
        self.directory_tree.setVisible(True)
        self.file_viewer.setVisible(True)
        self.status_bar_widget.setVisible(True)
        self.address_bar_widget.setVisible(True)    
        
        
        # initializing the window 
        self.updateRootIndexWithTraversal(self.current_dir)
        
    def fileConnections(self):
        self.file_viewer.open_folder.connect(lambda folder_path : self.updateRootIndexWithTraversal(folder_path))
        self.file_viewer.open_in_new_window.connect(lambda folder_path: self.openNewWindow(folder_path))
        self.file_viewer.open_file.connect(lambda file_path : self.openFile(file_path))
    def directoryConnections(self):
        self.directory_tree.dir_double_clicked.connect(lambda folder_path : self.updateRootIndex(folder_path))
        # self.directory_tree.dir_right_clicked.connect(lambda folder_path : self.updateRootIndex(folder_path))  to be implemented

    # defining actions and slots
    @catch_exceptions
    def updateRootIndexWithTraversal(self , folder_path):
        """Updates the root index of the file viewer and traverses the directory tree."""
        self.current_dir = folder_path
        self.file_viewer.updateRootIndex(folder_path)
        self.directory_tree.traverseDirectoryTree(folder_path)
    
    @catch_exceptions
    def updateRootIndex(self , folder_path):
        """
        On Double Clicking the Directory Tree
        Updates the root index of the file viewer.
        """
        self.current_dir = folder_path
        self.file_viewer.updateRootIndex(folder_path)
        
    @catch_exceptions
    def openNewWindow(self , folder_path):
        new_window = DoryWindow(init_root_dir=QDir.homePath() , current_dir=folder_path)
        new_window.show()
        
    @catch_exceptions
    def openFile(self , file_path:str):
        if platform.system() == "Windows":
            os.startfile(file_path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open" , file_path])
        else:
            subprocess.Popen(["xdg-open" , file_path])
            
# Running Application
if __name__ == "__main__":
    DoryApp = QApplication([])
    window = DoryWindow()
    window.show()
    DoryApp.exec()