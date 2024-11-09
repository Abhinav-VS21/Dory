from PySide6.QtWidgets import QLineEdit, QWidget, QHBoxLayout, QPushButton
from PySide6.QtCore import QDir, Signal
from PySide6.QtGui import QIcon
from DirectoryCompleter import DirectoryCompleter
from catchExecptions import catch_exceptions


class AddressBar(QLineEdit):
    # Signals
    address_path_changed = Signal(str)  # Custom signal to emit when path is changed

    @catch_exceptions
    def __init__(self, default_path="", parent=None):
        super().__init__(parent)
        
        self.setPlaceholderText("Enter directory path...")
        self.setText(default_path)
        
        
        self.completer = DirectoryCompleter(self)
        # Connect Enter key press to emit_path
        self.returnPressed.connect(self.emit_path)
    
    @catch_exceptions
    def emit_path(self):
        """Emits the address_path_changed signal with the current path."""
        path = self.text()
        if QDir(path).exists():
            self.address_path_changed.emit(path)
        else:
            self.setText("Invalid Path")
            self.selectAll()


class AddressBarWidget(QWidget):
    # Signals
    go_back_signal          = Signal()
    go_forward_signal       = Signal()
    go_up_signal            = Signal()
    run_search              = Signal()
    to_icon_mode            = Signal()
    to_list_mode            = Signal()
    address_path_changed    = Signal(str)

    @catch_exceptions
    def __init__(self):
        super().__init__()
        
        # Creating Widgets
        self.go_back_button         = QPushButton()
        self.go_forward_button      = QPushButton()
        self.go_up_button           = QPushButton()
        self.trigger_search_button  = QPushButton()
        self.icon_mode_button       = QPushButton()
        self.list_mode_button       = QPushButton()
        
        self.address_bar            = AddressBar()
        
        
        self.go_back_button.setIcon(QIcon("icons/chevron-left.svg"))   
        self.go_forward_button.setIcon(QIcon("icons/chevron-right.svg"))
        self.go_up_button.setIcon(QIcon("icons/arrow-90deg-up.svg"))
        self.trigger_search_button.setIcon(QIcon("icons/search.svg"))
        self.icon_mode_button.setIcon(QIcon("icons/grid-3x3-gap.svg"))
        self.list_mode_button.setIcon(QIcon("icons/list-task.svg"))
        
        self.go_back_button.setToolTip("Go Back")
        self.go_forward_button.setToolTip("Go Forward")
        self.go_up_button.setToolTip("Go to Parent Directory")
        self.trigger_search_button.setToolTip("Search")
        self.icon_mode_button.setToolTip("Icon Mode")
        self.list_mode_button.setToolTip("List Mode")

        # Connect buttons directly to signals
        self.go_back_button.clicked.connect(lambda: self.go_back_signal.emit())
        self.go_forward_button.clicked.connect(lambda: self.go_forward_signal.emit())
        self.go_up_button.clicked.connect(lambda: self.go_up_signal.emit())
        self.trigger_search_button.clicked.connect(lambda: self.run_search.emit())
        self.icon_mode_button.clicked.connect(lambda:self.to_icon_mode.emit())
        self.list_mode_button.clicked.connect(lambda:self.to_list_mode.emit())
        
        # Connect AddressBar's path change signal to update_address
        self.address_bar.address_path_changed.connect(self.updateAddress)

        # Set up the layout
        layout = QHBoxLayout(self)
        for widget in [self.go_back_button, self.go_forward_button,self.go_up_button , self.address_bar, 
                       self.trigger_search_button, self.icon_mode_button, self.list_mode_button]:
            layout.addWidget(widget)
        self.setLayout(layout)

    @catch_exceptions
    def updateAddress(self, path):
        """emits the address_path_changed signal with the given path."""
        self.address_path_changed.emit(path)
        
    @catch_exceptions
    def updatePlaceholder(self, text):
        """Updates the placeholder text of the AddressBar."""
        self.address_bar.setPlaceholderText(text)


#debug
# from PySide6.QtWidgets import QApplication
# app = QApplication([])
# window = AddressBarWidget()
# window.show()
# app.exec()