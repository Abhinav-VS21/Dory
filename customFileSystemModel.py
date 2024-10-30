from PySide6.QtWidgets import QApplication, QFileSystemModel, QStyle 
from PySide6.QtCore import Qt

# Override the model's data method to add a default icon

class CustomDirectoryModel(QFileSystemModel):
    
    def __init__(self, parent=None):
        super().__init__(parent)  # Initialize the base class
        
    def data(self, index, role=Qt.DisplayRole):
        
        if role == Qt.DecorationRole:
            icon = super().data(index, role)
            # Check if the icon is invalid
            
            if not icon or icon.isNull():
                
                # Use the application default icon as a fallback
                icon = QApplication.style().standardIcon(QStyle.SP_FileIcon)

            return icon
        
        return super().data(index, role)


