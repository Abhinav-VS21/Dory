from PySide6.QtWidgets import QListView , QMenu
from PySide6.QtCore import Signal, QDir, QSortFilterProxyModel, Qt
from PySide6.QtGui import QStandardItemModel , QAction
from catchExecptions import catch_exceptions
class SearchResultWidget(QListView):
    path_double_clicked = Signal(str)
    
    @catch_exceptions
    def __init__(self, parent=None):
        super().__init__(parent)  # Pass parent to the superclass
        self.item_model = QStandardItemModel(self)  # Set the model's parent
        self.setModel(self.model)
        self.doubleClicked.connect(self.item_double_clicked_slot)  # Corrected method name
        self.item_model.setHorizontalHeaderLabels(["Name", "Path", "Size", "Date Modified", "File Type"])

        # Create a proxy model to enable sorting
        self.proxy_model = QSortFilterProxyModel(self)
        self.proxy_model.setSourceModel(self.item_model)
        self.proxy_model.setSortCaseSensitivity(Qt.CaseInsensitive)
        self.setModel(self.proxy_model)

        self.setSortingEnabled(True)
        self.doubleClicked.connect(self.item_double_clicked_slot)
    
    
    @catch_exceptions
    def item_double_clicked_slot(self, index):  # Fixed method name to match the signal
        item = self.item_model.itemFromIndex(index)
        if item:  # Ensure item is valid
            self.path_double_clicked.emit(item.text())
        
        
    @catch_exceptions
    def clearResults(self):
        self.item_model.clear()  # Renamed for clarity
        
        
    @catch_exceptions
    def setResults(self, results):
        self.clearResults()  # Call the renamed clear method
        for result in results:
            self.item_model.appendRow(list(result))
            
            
    @catch_exceptions
    def contextMenuEvent(self, event):
        menu = QMenu(self)

        # Add sorting actions
        sort_by_name_action = QAction("Sort by Name", self)
        sort_by_size_action = QAction("Sort by Size", self)
        sort_by_date_action = QAction("Sort by Date Modified", self)
        
        # Connect actions to sorting methods
        sort_by_name_action.triggered.connect(lambda: self.sortByColumn(0))
        sort_by_size_action.triggered.connect(lambda: self.sortByColumn(2))
        sort_by_date_action.triggered.connect(lambda: self.sortByColumn(3))

        # Add a checkable action for reverse order
        reverse_order_action = QAction("Reverse Order", self, checkable=True)
        reverse_order_action.setChecked(self.reverse_order)
        reverse_order_action.triggered.connect(self.toggleReverseOrder)

        # Add actions to the menu
        menu.addAction(sort_by_name_action)
        menu.addAction(sort_by_size_action)
        menu.addAction(sort_by_date_action)
        menu.addAction(reverse_order_action)

        # Show the menu at the cursor position
        menu.exec(event.globalPos())


    @catch_exceptions
    def toggleReverseOrder(self):
        self.reverse_order = not self.reverse_order
        # Re-sort the current column with the new order
        column_index = self.proxy_model.sortColumn()
        self.proxy_model.sort(column_index, Qt.DescendingOrder if self.reverse_order else Qt.AscendingOrder)


    @catch_exceptions
    def sortByColumn(self, column_index):
        # Sort the proxy model by the specified column and current order
        self.proxy_model.sort(column_index, Qt.DescendingOrder if self.reverse_order else Qt.AscendingOrder)

    @catch_exceptions
    def hideSelf(self):
        """Hides the result widget"""
        self.hide()
        
    @catch_exceptions
    def showSelf(self):
        """Shows the result widget"""
        self.show()