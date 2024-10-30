from PySide6.QtWidgets import QApplication, QListView, QStyledItemDelegate, QStyleOptionViewItem, QFileSystemModel
from PySide6.QtGui import QIcon 
from PySide6.QtCore import QSize, Qt, QDir

class WrappingItemDelegate(QStyledItemDelegate):
    def paint(self, painter, option: QStyleOptionViewItem, index):
        # Draw the icon and the default text (file name) using the base class
        super().paint(painter, option, index)

        # Get the file name for wrapping
        file_name = index.data(Qt.DisplayRole)  # Get the file name from the model
        font_metrics = option.fontMetrics

        # Get the rectangle for the item
        text_rect = option.rect.adjusted(0, option.iconSize.height(), 0, 0)  # Adjust for the icon's height

        # Draw the text with wrapping
        painter.drawText(text_rect, Qt.TextWordWrap | option.displayAlignment, file_name)

    def sizeHint(self, option: QStyleOptionViewItem, index):
        file_name = index.data(Qt.DisplayRole)  # Get the file name from the model
        font_metrics = option.fontMetrics
        
        # Calculate the height needed for wrapped text
        text_height = font_metrics.boundingRect(file_name).height()
        
        # Return a fixed width and calculated height
        return QSize(100, text_height + 50)  # Width of 100 and additional space for icon and padding

def main():
    app = QApplication([])
    
    index = QDir.homePath()

    list_view = QListView()
    list_view.resize(400,400)
    list_view.setViewMode(QListView.IconMode)
    list_view.setSpacing(10)
    
    # Create a QFileSystemModel and set the root path
    file_system_model = QFileSystemModel()
    file_system_model.setRootPath(index)  # Set the root path to the desired directory

    list_view.setModel(file_system_model)
    
    # Set a custom delegate
    delegate = WrappingItemDelegate()
    list_view.setItemDelegate(delegate)

    # Set the root index for the list view to display
    root_index = file_system_model.index(index)  # Change this to the desired directory path
    list_view.setRootIndex(root_index)

    list_view.show()
    app.exec()

if __name__ == "__main__":
    main()
