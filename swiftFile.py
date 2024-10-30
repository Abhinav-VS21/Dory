from PySide6.QtWidgets import QApplication , QMainWindow ,QWidget , QVBoxLayout , QSplitter
from PySide6.QtCore import Qt , QDir
from DirectoryTreeView import DirectoryTreeView
from IconViewer import FileListViewer
from menuBar import MenuBar
from addressBar import AddressBar

class MainWindow(QMainWindow): 
    def __init__(self):
        super().__init__()
        root_directory = QDir.homePath()
        index_directory = QDir.homePath()
        self.central_widget = QWidget(self)
        
        
        # using qsplitter
        self.splitter = QSplitter(self.central_widget)  
        self.splitter.setOrientation(Qt.Horizontal)
        
        # adding the file tree view widget to the splitter
        self.directory_tree_view = DirectoryTreeView()
        self.file_list_viewer = FileListViewer(root_directory)
        self.addressBar = AddressBar()
                
        self.setCentralWidget(self.central_widget)
        self.v_layout = QVBoxLayout(self.central_widget)
        self.v_layout.addWidget(self.addressBar)
        self.v_layout.addWidget(self.splitter)
        self.splitter.addWidget(self.directory_tree_view)
        self.splitter.addWidget(self.file_list_viewer)
        
        
        # Setting the mainWindow properties
        self.setWindowTitle("Swift File")
        self.resize(1000, 1000)
        
        
        # Create a menu bar
        self.menu_bar = MenuBar()
        self.setMenuBar(self.menu_bar)
        
        
        # Connecting FileTreeViewWidget
        self.directory_tree_view.file_double_clicked.connect(self.openFilePath)
        self.directory_tree_view.folder_double_clicked.connect(self.updateIconListRootIndex) # note,no need to connect to expandDirectoryTreeView
        
        
        # Connecting IconListViewerWidget
        self.file_list_viewer.file_double_clicked.connect(self.openFilePath)
        self.file_list_viewer.folder_double_clicked.connect(self.updateIconListRootIndex)
        self.file_list_viewer.folder_double_clicked.connect(self.expandDirectoryTreeView)
        
        # Qsplitter being used to resize the widgets
        self.splitter.splitterMoved.connect(self.refreshView)
    
        # Connection View MenuBar
        self.menu_bar.switch_to_icon_mode_signal.connect(self.file_list_viewer.setIconView)
        self.menu_bar.switch_to_list_mode_signal.connect(self.file_list_viewer.setListView)
        self.menu_bar.refresh_view_signal.connect(self.file_list_viewer.refreshView)
    
        # Connection Tools MenuBar
        self.menu_bar.switch_to_new_icon_list_root_index.connect(self.updateIconListRootIndex)
        self.menu_bar.switch_to_new_icon_list_root_index.connect(self.expandDirectoryTreeView)
        
        
        # Connection AddressBar
        self.addressBar.address_path_changed.connect(self.updateIconListRootIndex)
        self.addressBar.address_path_changed.connect(self.expandDirectoryTreeView)
    
    
    
        
    def openFilePath(self , file_path):
        print('Opening file: ',file_path)
        # opening the file code goes here
    
    def getCurrentDirectory(self):
        return self.file_list_viewer.getCurrentDirectoryPath()
    
    def refreshView(self):
        self.file_list_viewer.refreshView()
        self.directory_tree_view.refreshView()
        
    def updateIconListRootIndex(self , parent_folder_path) :
        self.file_list_viewer.setNewRootIndex(parent_folder_path)
    
        
    def expandDirectoryTreeView(self , directory):
        self.directory_tree_view.traverseDirectoryTree(directory)
        

app = QApplication([])
window = MainWindow()
window.show()
app.exec()  