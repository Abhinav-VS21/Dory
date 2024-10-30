from PySide6.QtWidgets import QMenu, QMessageBox, QMainWindow, QApplication
from PySide6.QtGui import QAction

class Bookmark(QMenu):
    def __init__(self, parent=None):
        super().__init__("Bookmarks", parent)  # Initialize the QMenu with a title

        # Create a list to store bookmarks
        self.bookmarks = []

        # Create actions for the Bookmark menu
        self.add_bookmark_action = QAction("Add Bookmark", parent)
        self.view_bookmarks_action = QAction("View Bookmarks", parent)

        # Connect actions to slots
        self.add_bookmark_action.triggered.connect(self.addBookmark)
        self.view_bookmarks_action.triggered.connect(self.viewBookmarks)

        # Add actions to the Bookmark menu
        self.addAction(self.add_bookmark_action)
        self.addAction(self.view_bookmarks_action)

    def addBookmark(self):
        # Logic to add a bookmark (could be a dialog to select a directory)
        bookmark_name = "Sample Bookmark"  # Replace with actual logic to get a bookmark
        self.bookmarks.append(bookmark_name)
        QMessageBox.information(self.parent(), "Bookmark Added", f"Added: {bookmark_name}")

    def viewBookmarks(self):
        # Logic to view bookmarks (e.g., show in a dialog)
        if not self.bookmarks:
            QMessageBox.information(self.parent(), "Bookmarks", "No bookmarks available.")
            return

        bookmarks_list = "\n".join(self.bookmarks)
        QMessageBox.information(self.parent(), "Bookmarks", bookmarks_list)

# Example usage in a main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a Bookmark menu instance
        self.bookmark_menu = Bookmark(self)

        # Add Bookmark menu to the menu bar
        self.menuBar().addMenu(self.bookmark_menu)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.setWindowTitle("Bookmark Example")
    window.show()
    app.exec()
