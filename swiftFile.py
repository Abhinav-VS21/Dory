from PySide6.QtWidgets import QApplication , QMainWindow ,QWidget , QVBoxLayout , QSplitter , QTreeView , QMenuBar
from PySide6.QtCore import Qt
from fileTreeView import FileTreeViewWidget
from iconviewerWidget import IconViewer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Swift File")
        self.resize(823, 727)
        maxColumnWidth = 300
        initWidth = 200
        
        
        self.centralwidget = QWidget(self)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        
        # using qsplitter
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setOrientation(Qt.Horizontal)
        
        # adding the file tree view widget to the splitter
        self.fileTreeViewWidget = FileTreeViewWidget(maxColumnWidth)
        self.fileTreeViewWidget.setObjectName(u"FiletreeView")
        self.fileTreeViewWidget.fileTreeView.hideColumn(1)
        self.fileTreeViewWidget.fileTreeView.hideColumn(2)
        self.fileTreeViewWidget.fileTreeView.hideColumn(3)
        
        self.fileTreeViewWidget.setMaximumWidth(maxColumnWidth) # Set the desired maximum width in pixels
    
        self.iconViewer = IconViewer(self.fileTreeViewWidget.homeDirectory)
        self.iconViewer.setObjectName(u"iconViewer")
        
        self.splitter.addWidget(self.fileTreeViewWidget)
        self.splitter.addWidget(self.iconViewer)
        
        

        self.verticalLayout.addWidget(self.splitter)
        self.setCentralWidget(self.centralwidget)
        
        self.fileTreeViewWidget.fileTreeView.doubleClicked.connect(self.on_double_click)
    
    
    def on_double_click(self , index):
        indexItem = self.fileTreeViewWidget.fileSystemModel.index(index.row() , 0 , index.parent())
        filePath = self.fileTreeViewWidget.fileSystemModel.filePath(indexItem)
        self.iconViewer.populate_file_list(filePath)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()  