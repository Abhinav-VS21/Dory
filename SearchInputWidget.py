from PySide6.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QWidget, QToolButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal
from catchExecptions import catch_exceptions

class SearchInputWidget(QWidget):
    search_conditions_signal = Signal(dict)
    
    @catch_exceptions
    def __init__(self):
        super().__init__()
        
        # Creating input widgets
        self.search_input = QLineEdit()
        self.search_button = QToolButton()
        self.case_sensitive = QPushButton()
        self.recursive_search = QPushButton()
        self.full_match_search = QPushButton()
        
        # Make buttons checkable
        btn_list = [self.case_sensitive, self.recursive_search, self.full_match_search]
        for btn in btn_list:
            btn.setCheckable(True)
            
        self.case_sensitive.toggled.connect(lambda :self.updateConditions())  # Connect to update method
        self.recursive_search.toggled.connect(lambda :self.updateConditions())
        self.full_match_search.toggled.connect(lambda :self.updateConditions())
        
        # Making button tooltip
        self.search_button.setToolTip("Run Search")
        self.case_sensitive.setToolTip("toggle case-sensitive search")
        self.recursive_search.setToolTip("search-recursively")
        self.full_match_search.setToolTip('full-match-search')
        # Adding icons to the buttons
        self.search_button.setIcon(QIcon("icons/search.svg"))
        self.case_sensitive.setIcon(QIcon("icons/type.svg"))
        self.recursive_search.setIcon(QIcon("icons/recursive.svg"))
        self.full_match_search.setIcon(QIcon("icons/binoculars.svg"))
        
        # Layout the input widgets
        self.layout = QHBoxLayout(self)
        widget_list = [self.search_input, self.search_button] + btn_list
        for widget in widget_list:
            self.layout.addWidget(widget)

        # Initializing the search conditions
        self.search_conditions = {  
            'search_text': '',
            'case_sensitive': False,
            'recursive_search': False,
            'full_match_search': False
        }
        
        # Connecting the search button
        self.search_button.clicked.connect(lambda : self.search())


    @catch_exceptions
    def search(self):
        # Get the current search text and update conditions
        search_text = self.search_input.text()
        self.search_conditions['search_text'] = search_text
        self.updateConditions()
        
        # Emit the search conditions signal
        print('emiting the self.search_conditions')
        self.search_conditions_signal.emit(self.search_conditions)


    @catch_exceptions
    def updateConditions(self):
        # Update the search conditions based on the button states
        self.search_conditions['case_sensitive'] = self.case_sensitive.isChecked()
        self.search_conditions['recursive_search'] = self.recursive_search.isChecked()
        self.search_conditions['full_match_search'] = self.full_match_search.isChecked()

        # Optionally, print conditions for debugging
        print(f"Updated search conditions: {self.search_conditions}")
        
    @catch_exceptions
    def hideSelf(self):
        """Hides the search widget"""
        self.hide()
        
    @catch_exceptions
    def showSelf(self):
        """Shows the search widget"""
        self.show()
        
    

