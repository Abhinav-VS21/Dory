from PySide6.QtCore import Qt , QDir
from PySide6.QtWidgets import QFileSystemModel

class EditableFileSystemModel(QFileSystemModel):
    def __init__(self, parent=None):
        super().__init__(parent)  # This is necessary!

    def flags(self, index):
        base_flags = super().flags(index)
        return base_flags | Qt.ItemIsEditable
    
    def toggleHiddenFiles(self, show_hidden):
        current_filter = self.filter()
        if show_hidden:
            self.setFilter(current_filter | QDir.Hidden)
        else:
            self.setFilter(current_filter & ~QDir.Hidden)           # ~ is the bitwise NOT operator