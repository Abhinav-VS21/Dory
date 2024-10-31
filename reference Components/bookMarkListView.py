from PySide6.QtWidgets import QListView, QMenu, QMessageBox
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt, QPoint , Signal

class BookmarkListView(QListView):
    #Signals
    open_bookmark = Signal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = QStandardItemModel(self)
        self.setModel(self.model)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openContextMenu)
        
        # Connect double-click to remove bookmark with confirmation
        self.doubleClicked.connect(self.openBookmark)

    def addBookmark(self, path: str):
        item = QStandardItem(path)
        item.setEditable(False)
        item.setData(path, Qt.UserRole)
        self.model.appendRow(item)

    def openContextMenu(self, position: QPoint):
        context_menu = QMenu(self)
        remove_action = context_menu.addAction("Remove Bookmark")
        open_action = context_menu.addAction("Open Bookmark")

        action = context_menu.exec_(self.viewport().mapToGlobal(position))
        index = self.indexAt(position)
        if action == remove_action:
            self.confirmRemoveBookmark(index)
        elif action == open_action:
            self.openBookmark(index)

    def confirmRemoveBookmark(self, index):
        # Confirm deletion on double-click
        reply = QMessageBox.question(self, "Remove Bookmark", 
                                     "Are you sure you want to remove this bookmark?", 
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.removeBookmark(index)

    def removeBookmark(self, index):
        if index.isValid():
            self.model.removeRow(index.row())

    def openBookmark(self, index):
        path = index.data(Qt.UserRole)
        # Implementation to open path goes here (could emit a signal or open in app)
