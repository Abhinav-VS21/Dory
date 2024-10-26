from PySide6.QtWidgets import QApplication , QMainWindow ,QWidget , QVBoxLayout , QSplitter , QTreeView , QMenuBar 
from PySide6.QtCore import Qt , QTimer , QDir
from fileTreeView import FileTreeViewWidget
from iconviewerWidget import IconListViewerWidget
from menuBar import MenuBar
from addressBar import AddressBar

class MainWindow(QMainWindow): 
    def __init__(self):
        super().__init__()
        
        self.central_widget = QWidget(self)
        
        
        # using qsplitter
        self.splitter = QSplitter(self.central_widget)  
        self.splitter.setOrientation(Qt.Horizontal)
        
        # adding the file tree view widget to the splitter
        self.file_tree_view_widget = FileTreeViewWidget()        
        self.icon_list_viewer_widget = IconListViewerWidget()
        self.addressBar = AddressBar()
        
        
        self.setCentralWidget(self.central_widget)
        self.v_layout = QVBoxLayout(self.central_widget)
        self.v_layout.addWidget(self.addressBar)
        self.v_layout.addWidget(self.splitter)
        self.splitter.addWidget(self.file_tree_view_widget)
        self.splitter.addWidget(self.icon_list_viewer_widget)
        
        
        
        # Setting the mainWindow properties
        self.setWindowTitle("Swift File")
        self.resize(823, 727)
        
        # Create a menu bar
        self.menu_bar = MenuBar()
        self.setMenuBar(self.menu_bar)
        
        
    # Connecting FileTreeViewWidget and iconViewerWidget
        self.file_tree_view_widget.file_tree_view.doubleClicked.connect(self.findFilePathOnItem)
    
    # Connection View MenuBar
        self.menu_bar.switch_to_icon_mode_signal.connect(self.icon_list_viewer_widget.setIconView)
        self.menu_bar.switch_to_list_mode_signal.connect(self.icon_list_viewer_widget.setListView)
        self.menu_bar.refresh_view_signal.connect(self.icon_list_viewer_widget.refreshView)
    
    
    
    
    
    
    def findFilePathOnItem(self , model_index):
        
        #returns the filePath of the selected item
        index_item  = self.file_tree_view_widget.file_system_model.index(model_index.row() , 0 , model_index.parent())
        print('the filetree row count' , self.file_tree_view_widget.file_system_model.rowCount(index_item))
        file_path = self.file_tree_view_widget.file_system_model.filePath(index_item) # removes the same model issue
        
        
        # Update the icon viewer to show the contents of the selected directory or file
        if self.file_tree_view_widget.file_system_model.isDir(index_item):
            self.icon_list_viewer_widget.setNewRootIndex(file_path)  
            print('Navigating to directory: ',self.file_tree_view_widget.file_system_model.filePath(index_item))
            
        else:
            print('Opening file: ',self.file_tree_view_widget.file_system_model.filePath(index_item))
        
        # opening the file code goes here
        

app = QApplication([])
window = MainWindow()
window.show()
app.exec()  