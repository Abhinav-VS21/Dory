from PySide6.QtWidgets import QStyledItemDelegate
from PySide6.QtGui import QPainter
from PySide6.QtCore import QRect, QSize, Qt


class TextWrappingIconDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter: QPainter, option, index):
        painter.save()

        # Draw the icon
        icon = index.data(Qt.DecorationRole)
        if icon:
            icon_rect = QRect(option.rect.x(), option.rect.y(), 64, 64)  # Adjust icon size as needed
            icon.paint(painter, icon_rect, Qt.AlignCenter)

        # Draw the text with word wrapping
        text = index.data(Qt.DisplayRole)
        text_rect = QRect(option.rect.x(), option.rect.y() + 70, option.rect.width(), option.rect.height() - 70)
        painter.drawText(text_rect, Qt.AlignCenter | Qt.TextWordWrap, text)

        painter.restore()

    def sizeHint(self, option, index):
        # Set a fixed size for each item in the grid (adjust as necessary)
        return QSize(80, 100)  # Width and height can be adjusted based on item size

