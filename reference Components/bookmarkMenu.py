from PySide6.QtWidgets import QMenu, QMessageBox , QInputDialog
from PySide6.QtCore import QDir , Signal
from PySide6.QtGui import QAction

class Bookmark(QMenu):
    #Signals
    path_added = Signal(str , str)
    open_bookmarkListView = Signal()
    def __init__(self, parent=None):
        super().__init__("Bookmarks", parent)  # Initialize the QMenu with a title

        # Create actions for the Bookmark menu
        self.add_bookmark_action = QAction("Add Bookmark", parent)
        self.view_bookmarks_action = QAction("View Bookmarks", parent)

        # Connect actions to slots
        self.add_bookmark_action.triggered.connect(self.addBookmark)
        self.view_bookmarks_action.triggered.connect(self.viewBookmarks)

        # Add actions to the Bookmark menu
        self.addAction(self.add_bookmark_action)
        self.addAction(self.view_bookmarks_action)
        
    def currentPath(self, path:str):
        self.path = path

    def addBookmark(self):
        name, ok = QInputDialog.getText(self, "Add Bookmark", "Enter the name of the bookmark:")
        if ok:
            self.path_added.emit(name , self.path)
        
    def viewBookmarks(self):
        self.open_bookmarkListView.emit()