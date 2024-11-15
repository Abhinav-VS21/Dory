from PySide6.QtWidgets import QTreeView, QToolTip ,QMenu
from PySide6.QtGui import QStandardItemModel, QStandardItem , QAction
from PySide6.QtCore import Qt, Signal
from catchExecptions import catch_exceptions
import json


class BookmarkTree(QTreeView):
    #Signals
    open_in_cur_window     = Signal(str)  
    open_in_new_window      = Signal(str)
       
       
    @catch_exceptions
    def __init__(self, bookmarks_file="bookmarks.json", parent=None):
        super().__init__(parent)
        self.bookmarks_file = bookmarks_file
        
        self.setMouseTracking(True)  

        # Set up the model
        self.bookmark_model = QStandardItemModel()
        self.bookmark_model.setHorizontalHeaderLabels(["Bookmarks"])
        self.setModel(self.bookmark_model)

        
        self.load_bookmarks()

        # Connections
        self.doubleClicked.connect(self.on_bookmark_clicked)
        
        
    @catch_exceptions
    def mouseMoveEvent(self, event):
        index = self.indexAt(event.pos())  # Get the index at the mouse position
        if index.isValid():
            path = index.data(Qt.UserRole)  # Retrieve the stored path
            if path:
                # Use globalPosition() for PySide6 compatibility
                QToolTip.showText(event.globalPosition().toPoint(), path, self)
            else:
                QToolTip.hideText()
        else:
            QToolTip.hideText()
        super().mouseMoveEvent(event)
        
        
    @catch_exceptions   
    def mouseDoubleClickEvent(self, event):
        index = self.indexAt(event.pos())
        if index.isValid():
            # Emit the custom signal to open the bookmark
            self.open_in_cur_window   .emit(self.bookmark_model.itemFromIndex(index).data(Qt.UserRole))
        else:
            super().mouseDoubleClickEvent(event)
          
          
    @catch_exceptions  
    def contextMenuEvent(self, event):
        index = self.indexAt(event.pos())
        if index.isValid():
            menu = QMenu(self)

            # Create actions for the context menu
            open_action = QAction("Open", self)
            open_new_window_action = QAction("Open in New Window", self)
            remove_action = QAction("Remove", self)
            rename_action = QAction("Rename", self)

            # Connect actions to their respective signals
            open_action.triggered.connect(lambda: self.open_in_cur_window.emit(self.bookmark_model.itemFromIndex(index).data(Qt.UserRole)))
            open_new_window_action.triggered.connect(lambda: self.open_in_new_window.emit(self.bookmark_model.itemFromIndex(index).data(Qt.UserRole)))
            remove_action.triggered.connect(lambda: self.remove_bookmark(self.bookmark_model.itemFromIndex(index).text()))
            rename_action.triggered.connect(lambda: self.rename_bookmark(index))

            # Add actions to the context menu
            menu.addAction(open_action)
            menu.addAction(open_new_window_action)
            menu.addAction(remove_action)
            menu.addAction(rename_action)

            # Show the context menu at the cursor position
            menu.exec(event.globalPos())
    

    @catch_exceptions
    def remove_bookmark(self, name):
        """Removes a bookmark by name and updates the persistent store."""
        for row in range(self.bookmark_model.rowCount()):
            item = self.bookmark_model.item(row)
            if item.text() == name:
                self.bookmark_model.removeRow(row)
                self.save_bookmarks()  
                break
         
         
    @catch_exceptions   
    def rename_bookmark(self, index):
        """Puts the selected bookmark in rename mode."""
        if index.isValid():
            self.edit(index)
     
                      
    @catch_exceptions
    def load_bookmarks(self):
        """Loads bookmarks from the JSON file."""
        try:
            with open(self.bookmarks_file, 'r') as file:
                bookmarks = json.load(file)
                for name, path in bookmarks.items():
                    item = QStandardItem(name)
                    item.setData(path, Qt.UserRole)
                    self.bookmark_model.appendRow(item)
        except (FileNotFoundError, json.JSONDecodeError):
            # If file doesn't exist or is corrupt, start with an empty list
            print("No bookmarks found or file is invalid. Starting fresh.")


    @catch_exceptions
    def save_bookmarks(self):
        """Saves the current bookmarks to the JSON file."""
        bookmarks = {}
        for row in range(self.bookmark_model.rowCount()):
            item = self.bookmark_model.item(row)
            name = item.text()
            path = item.data(Qt.UserRole)
            bookmarks[name] = path

        with open(self.bookmarks_file, 'w') as file:
            json.dump(bookmarks, file, indent=4)


    @catch_exceptions
    def on_bookmark_clicked(self, index):
        """Handles bookmark double-click to emit the stored path."""
        item = self.bookmark_model.itemFromIndex(index)
        path = item.data(Qt.UserRole)
        self.open_in_cur_window.emit(path)
       
       
    @catch_exceptions 
    def hideSelf(self):
        """Hides the BookmarkTree widget."""
        self.hide()
       
       
    @catch_exceptions 
    def showSelf(self):
        """Shows the BookmarkTree widget."""
        self.show()
            
           
    # slots
    @catch_exceptions
    def addBookmark(self,path:str, name:str):
        """Adds a new bookmark to the tree and saves it persistently."""
        
        # Create a new item for the bookmark
        item = QStandardItem(name)
        item.setData(path, Qt.UserRole)  # Store the path in UserRole

        # Add the item to the model
        self.bookmark_model.appendRow(item)

        # Save the updated bookmarks list to file
        self.save_bookmarks()
    
        
# from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
# class BookmarkManager(QWidget):
#     """A simple UI to manage the BookmarkTree with add/remove functionality."""
#     def __init__(self):
#         super().__init__()

#         # Layout
#         layout = QVBoxLayout(self)
#         self.bookmark_tree = BookmarkTree()

#         # Buttons to add and remove bookmarks
#         self.add_button = QPushButton("Add Bookmark")
#         self.remove_button = QPushButton("Remove Bookmark")

#         layout.addWidget(self.bookmark_tree)
#         layout.addWidget(self.add_button)
#         layout.addWidget(self.remove_button)

#         # Example: Add or remove bookmarks manually (could connect to dialogs)
#         self.add_button.clicked.connect(lambda: self.bookmark_tree.add_bookmark("Example", QDir.homePath()))
#         self.remove_button.clicked.connect(lambda: self.bookmark_tree.remove_bookmark("Example"))

#         self.setLayout(layout)


# app = QApplication([])
# window = BookmarkManager()
# window.show()
# app.exec()