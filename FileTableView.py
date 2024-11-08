from PySide6.QtWidgets import QTableView , QMenu  ,QHeaderView
from PySide6.QtCore import Signal ,Qt , QAbstractTableModel 
from PySide6.QtGui import  QAction 
from catchExecptions import catch_exceptions
import os 

class FileTableModel(QAbstractTableModel):
    COLUMNS = ['Name', 'Path', 'Size', 'Type', 'Modified Date']
    
    def __init__(self):
        super().__init__()
        self._data: list[tuple] = []
    
    def rowCount(self, parent=None):
        return len(self._data)
    
    def columnCount(self, parent=None):
        return len(self.COLUMNS)
    
    @catch_exceptions
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
            
        value = self._data[index.row()][index.column()]
        
        if role == Qt.DisplayRole:
            if isinstance(value, int):  # File size
                # Convert bytes to human-readable format
                for unit in ['B', 'KB', 'MB', 'GB']:
                    if value < 1024:
                        return f"{value:.1f} {unit}"
                    value /= 1024
                return f"{value:.1f} TB"
            return str(value)
            
        elif role == Qt.TextAlignmentRole:
            if isinstance(self._data[index.row()][index.column()], int):
                return Qt.AlignRight | Qt.AlignVCenter
            return Qt.AlignLeft | Qt.AlignVCenter
            
        return None
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.COLUMNS[section]
        return None
    
    def sort(self, column, order=Qt.AscendingOrder):
        self.layoutAboutToBeChanged.emit()
        self._data.sort(
            key=lambda x: x[column],
            reverse=(order == Qt.DescendingOrder)
        )
        self.layoutChanged.emit()
    
    def update_results(self, file_tuples: list[tuple]):
        self.beginResetModel()
        self._data = file_tuples
        self.endResetModel()

class FileTableView(QTableView):
    path_double_clicked = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.order = Qt.AscendingOrder
        
        # Create and set the file_table_model
        self.file_table_model = FileTableModel()
        self.setModel(self.file_table_model)
        
        # Setup the view
        self.setup_appearance()
        
        self.doubleClicked.connect(self.onDoubleClick)
        
    def setup_appearance(self):
        # Enable sorting
        self.setSortingEnabled(True)
        
        # Enable alternating row colors
        self.setAlternatingRowColors(True)
        
        # Setup header
        header = self.horizontalHeader()
        header.setStretchLastSection(False)
        
        # Set column resize modes
        for i in range(len(FileTableModel.COLUMNS)):
            if i == 1:  # Path column
                # Path column stretches to fill space
                header.setSectionResizeMode(i, QHeaderView.Stretch)
            else:
                # Other columns resize to content
                header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        
        # Optional: Set selection behavior
        self.setSelectionBehavior(QTableView.SelectRows)  # Select entire rows
        self.setSelectionMode(QTableView.SingleSelection)  # One row at a time
        
    def updateResults(self, results: list[tuple]):
        print('updating results')
        self.file_table_model.update_results(results)
        
    def toggleReverseOrder(self):
        """Toggles the reverse order flag and updates the sorting order."""
        self.order = Qt.DescendingOrder if self.order == Qt.AscendingOrder else Qt.AscendingOrder
    
    
    @catch_exceptions
    def contextMenuEvent(self, event):
        menu = QMenu(self)

        # Add sorting actions
        sort_by_name_action = QAction("Sort by Name", self)
        sort_by_size_action = QAction("Sort by Size", self)
        sort_by_date_action = QAction("Sort by Date Modified", self)
        
        # Connect actions to sorting methods
        sort_by_name_action.triggered.connect(lambda: self.sortByColumn(0, self.order))
        sort_by_size_action.triggered.connect(lambda: self.sortByColumn(2, self.order))
        sort_by_date_action.triggered.connect(lambda: self.sortByColumn(3, self.order))

        # Add a checkable action for reverse order
        reverse_order_action = QAction("Reverse Order", self, checkable=True)
        reverse_order_action.setChecked(self.order == Qt.DescendingOrder)
        reverse_order_action.triggered.connect(self.toggleReverseOrder)

        # Add actions to the menu
        menu.addAction(sort_by_name_action)
        menu.addAction(sort_by_size_action)
        menu.addAction(sort_by_date_action)
        menu.addAction(reverse_order_action)

        # Show the menu at the cursor position
        menu.exec(event.globalPos())
        
    @catch_exceptions
    def onDoubleClick(self, index):
        path = os.path.dirname(self.file_table_model._data[index.row()][1])
        print(path)
        print(type(path))
        self.path_double_clicked.emit(path)

    