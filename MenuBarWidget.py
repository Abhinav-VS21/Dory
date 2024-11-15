from PySide6.QtWidgets import QMenuBar, QMessageBox
from PySide6.QtGui import QAction 
from PySide6.QtCore import Signal, QDir
from catchExecptions import catch_exceptions

class MenuBar(QMenuBar):
    # Signals
    open_new_window                 = Signal()
    refresh_view                    = Signal()
    to_icon_mode                    = Signal()
    to_list_mode                    = Signal()
    change_directory                = Signal(str)   
    run_search_widget               = Signal()
    add_current_dir_bookmark_signal = Signal()
    open_bookmark                   = Signal()      
    create_new_file                 = Signal()
    create_new_folder               = Signal()
    open_dir_properties             = Signal()

    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_menu()
    
    
    @catch_exceptions
    def init_menu(self):
        # Setup individual menus
        self.setup_file_menu()
        self.setup_view_menu()
        self.setup_go_menu()
        self.setup_bookmarks_menu()
        self.setup_help_menu()
    
    
    @catch_exceptions
    def setup_file_menu(self):
        file_menu = self.addMenu("File")
        new_window = QAction('Open New Window', self)
        create_new_file = QAction('Create New File', self)
        create_new_folder = QAction('Create New Folder', self)
        dir_property = QAction('Directory Property', self)
        
        file_menu.addActions([new_window, create_new_file, create_new_folder, dir_property])
        
        # Connect actions to signals
        new_window.triggered.connect(lambda : self.open_new_window.emit())
        dir_property.triggered.connect(lambda: self.open_dir_properties.emit())
        create_new_file.triggered.connect(lambda : self.create_new_file.emit())
        create_new_folder.triggered.connect(lambda: self.create_new_folder.emit())
        
    
    
    @catch_exceptions
    def setup_view_menu(self):
        view_menu = self.addMenu("View")
        icon_mode_action = QAction("Icon Mode", self)
        list_mode_action = QAction("List Mode", self)
        refresh_action = QAction("Refresh", self)
        
        view_menu.addActions([icon_mode_action, list_mode_action, refresh_action])
        
        # Connect actions to signals
        icon_mode_action.triggered.connect(lambda : self.to_icon_mode.emit())
        list_mode_action.triggered.connect(lambda:self.to_list_mode.emit())
        refresh_action.triggered.connect(lambda: self.refresh_view.emit())
    
    
    @catch_exceptions
    def setup_go_menu(self):
        go_menu = self.addMenu("Go")
        go_home = QAction("Home", self)
        go_root = QAction("Root", self)
        search_file = QAction("Search for file", self)
        
        go_menu.addActions([go_home, go_root, search_file])
        
        # Connect actions to methods and signals
        go_home.triggered.connect(self.goToHome)
        go_root.triggered.connect(self.goToRoot)
        search_file.triggered.connect(self.run_search_widget)
    
    
    @catch_exceptions
    def setup_bookmarks_menu(self):
        bookmarks_menu = self.addMenu("Bookmarks")
        add_bookmark = QAction("Add Bookmark", self)
        open_bookmark = QAction("Edit Bookmark", self)
        
        bookmarks_menu.addActions([add_bookmark, open_bookmark])
        
        # Connect actions to signals
        add_bookmark.triggered.connect(self.add_current_dir_bookmark_signal)
        open_bookmark.triggered.connect(self.open_bookmark)
    
    
    @catch_exceptions
    def setup_help_menu(self):
        help_menu = self.addMenu("Help")
        about_action = QAction("About", self)
        all_shortcuts = QAction("All Shortcuts", self)
        
        help_menu.addActions([all_shortcuts, about_action])
        
        # Connect actions to dialog methods
        about_action.triggered.connect(self.showAboutDialog)
        all_shortcuts.triggered.connect(self.showShortcutsDialog)

    # Go Menu Actions
    @catch_exceptions
    def goToHome(self):
        """Changes the current directory to the user's home directory"""
        self.change_directory.emit(QDir.homePath())
    
    
    @catch_exceptions
    def goToRoot(self):
        """Changes the current directory to the root directory"""
        self.change_directory.emit(QDir.rootPath())
               
    # Help Menu Actions
    @catch_exceptions
    def showAboutDialog(self):
        """Shows the about dialog."""
        QMessageBox.about(self, "About", "This is a simple file manager")
    
    
    @catch_exceptions
    def showShortcutsDialog(self):
        """Shows the shortcuts dialog."""
        QMessageBox.about(self, "Shortcuts", "Here are the shortcuts for this application")
