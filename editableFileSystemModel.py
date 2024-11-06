from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileSystemModel

class EditableFileSystemModel(QFileSystemModel):
    def flags(self, index):
        base_flags = super().flags(index)
        # Force the item to be editable for testing
        return base_flags | Qt.ItemIsEditable