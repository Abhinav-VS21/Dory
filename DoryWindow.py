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
    def __init__(self , init_root_dir : str = QDir.homePath() , current_dir : str = QDir.homePath()):
        super().__init__()

        self.setWindowTitle("Dory")
        self.setMinimumSize(800 , 600)
        self.init_root_dir = init_root_dir
        self.current_dir = current_dir

        self.initLayout()
        self.initWindow()
        
        # Connecting Signals and Slots
        self.fileConnections()
        self.directoryConnections()
        self.bookmarkConnections()
        self.menubarConnections()
        
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
        
        
    def initWindow(self):
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
        
        # Creating Clipboard
        self.clipboard = QApplication.clipboard()
        self.clipboard_mode = None
        
        
    def fileConnections(self):
        self.file_viewer.open_folder.connect(lambda folder_path : self.updateRootIndexWithTraversal(folder_path))
        self.file_viewer.open_in_new_window.connect(lambda folder_path: self.openNewWindow(folder_path))
        self.file_viewer.open_file.connect(lambda file_path : self.openFile(file_path))
        self.file_viewer.copy_file_signal.connect(lambda file_path : self.copyFile(file_path))
        self.file_viewer.cut_file_signal.connect(lambda file_path : self.cutFile(file_path))
        self.file_viewer.copy_folder_signal.connect(lambda folder_path : self.copyFolder(folder_path))
        self.file_viewer.cut_folder_signal.connect(lambda folder_path : self.cutFolder(folder_path))
        self.file_viewer.paste_signal.connect(lambda target_directory : self.paste(target_directory))
        self.file_viewer.add_bookmark_path.connect(lambda path,name : self.bookmark_tree.addBookmark(path,name))
        
    def directoryConnections(self):
        self.directory_tree.dir_double_clicked.connect(lambda folder_path : self.updateRootIndex(folder_path))
        # self.directory_tree.dir_right_clicked.connect(lambda folder_path : self.updateRootIndex(folder_path))  to be implemented

    def bookmarkConnections(self):
        self.bookmark_tree.open_in_cur_window.connect(lambda path : self.updateRootIndexWithTraversal(path))
        self.bookmark_tree.open_in_new_window.connect(lambda path : self.openNewWindow(path))
       
    def menubarConnections(self):
        self.menu_bar.open_bookmark.connect(lambda: self.showBookmarkTree())
        self.menu_bar.open_new_window.connect(lambda : self.openNewWindow(self.current_dir))
        self.menu_bar.refresh_view.connect(lambda : self.refreshView())
        self.menu_bar.to_icon_mode.connect(lambda : self.setIconView())
        self.menu_bar.to_list_mode.connect(lambda : self.setListView())
        self.menu_bar.change_directory.connect(lambda path: self.updateRootIndexWithTraversal(path))
        self.menu_bar.run_search_widget.connect(lambda: self.search_input.setVisible(not self.search_input.isVisible()))
        self.menu_bar.add_current_dir_bookmark_signal.connect(lambda : self.bookmark_tree.addBookmark(self.current_dir , os.path.basename(self.current_dir) ))
        self.menu_bar.create_new_file.connect(lambda : self.file_viewer.createNewFile())
        self.menu_bar.create_new_folder.connect(lambda : self.file_viewer.createNewFolder())
        self.menu_bar.open_dir_properties.connect(lambda : self.file_viewer.currDirProperties())
    
    def searchConnections(self):
        self.search_input.search_conditions_signal.connect(lambda condition_dict: self.runSearchTherad(condition_dict))
        self.search_result.path_double_clicked.connect(lambda path: self.openInFileView(path))
        
        
    # defining actions and slots
    @catch_exceptions
    def updateRootIndexWithTraversal(self , folder_path : str):
        """Updates the root index of the file viewer and traverses the directory tree."""
        self.current_dir = folder_path
        self.file_viewer.updateRootIndex(folder_path)
        self.directory_tree.traverseDirectoryTree(folder_path)
        self.address_bar_widget.updatePlaceholder(folder_path)
        
        
        # Show the directory tree and hide the bookmark tree
        self.directory_tree.setVisible(True)
        self.bookmark_tree.setVisible(False)
        self.file_viewer.setVisible(True)
        self.search_result.setVisible(False)
    
    @catch_exceptions
    def updateRootIndex(self , folder_path):
        """
        On Double Clicking the Directory Tree
        Updates the root index of the file viewer.
        """
        self.current_dir = folder_path
        self.file_viewer.updateRootIndex(folder_path)
        self.address_bar_widget.updatePlaceholder(folder_path)
        
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
            
    @catch_exceptions
    def copyFile(self , file_path:str):
        """Copies the file to the clipboard."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File does not exist: {file_path}")
        
        
        self.clipboard.setText(file_path)
        self.clipboard_mode = "copy"
        
    @catch_exceptions
    def cutFile(self , path:str):
        """Cuts the file path to the clipboard."""
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        
        self.clipboard.setText(path)
        self.clipboard_mode = "cut"
        
    @catch_exceptions
    def copyFolder(self , folder_path:str):
        """Copies the folder to the clipboard."""
        
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder does not exist: {folder_path}")
        
        self.clipboard.setText(folder_path)
        self.clipboard_mode = "copy"
        
    @catch_exceptions 
    def cutFolder(self , folder_path:str):
        """Cuts the folder to the clipboard."""
        
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder does not exist: {folder_path}")
        
        self.clipboard.setText(folder_path)
        self.clipboard_mode = "cut"
     
    @catch_exceptions
    def paste(self, target_directory: str):
        """Pastes the file or folder from the clipboard into the target directory."""
        source_path = self.clipboard.text()
        
        print(f"Source Path: {source_path}")
        
        if not source_path or not os.path.exists(source_path):
            raise FileNotFoundError("No valid file or folder in clipboard to paste")
        
        # Define the destination path (same name as source but in target directory)
        destination_path = os.path.join(target_directory, os.path.basename(source_path))
        
        # Handle the copy or move operation based on clipboard mode
        if self.clipboard_mode == "copy":
            if os.path.isfile(source_path):
                shutil.copy2(source_path, destination_path)  # Copy file
            elif os.path.isdir(source_path):
                shutil.copytree(source_path, destination_path)  # Copy directory (recursively)
        
        elif self.clipboard_mode == "cut":
            if os.path.isdir(source_path):
                shutil.move(source_path, destination_path)  # Move directory
            elif os.path.isfile(source_path):
                shutil.move(source_path, destination_path)  # Move file

        # Clear clipboard after pasting
        self.clipboard.clear()  
        print(f"Pasted {source_path} to {destination_path}")

    @catch_exceptions
    def showBookmarkTree(self):
        """Shows the bookmark tree widget."""
        self.bookmark_tree.setVisible(True)
        self.directory_tree.setVisible(False)
        
    @catch_exceptions
    def toggleBookmarkDirectory(self):
        """Toggles the bookmark tree visibility."""
        self.bookmark_tree.setVisible(not self.bookmark_tree.isVisible())
        self.directory_tree.setVisible(not self.directory_tree.isVisible())

    @catch_exceptions
    def refreshView(self):
        """Refreshes the file viewer."""
        self.file_viewer.refreshView()
        self.directory_tree.refreshView()
        print("Refreshed view")
    
    @catch_exceptions
    def setIconView(self):
        """Switches the file viewer to icon view."""
        self.file_viewer.setIconView()
        
    @catch_exceptions
    def setListView(self):
        """Switches the file viewer to list view."""
        self.file_viewer.setListView()
        
    @catch_exceptions
    def runSearchTherad(self , condition_dict):
        """Runs the search thread with the given conditions."""
        search_thread = SearchThread(condition_dict)
        search_thread.start()
        search_thread.search_result.connect(lambda result : self.search_result.updateSearchResult(result))
        search_thread.finished.connect(lambda : self.search_result.setVisible(True))
    
# Running Application
if __name__ == "__main__":
    DoryApp = QApplication([])
    window = DoryWindow()
    window.show()
    DoryApp.exec()