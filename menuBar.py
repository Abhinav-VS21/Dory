from PySide6.QtWidgets import QMenuBar, QFileDialog, QMessageBox, QApplication 
from PySide6.QtGui import QAction 
from PySide6.QtCore import Signal

class MenuBar(QMenuBar):
    
    # Defining View Signals
    switch_to_icon_mode_signal = Signal()
    switch_to_list_mode_signal = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_menu()

    def init_menu(self):
        # File Menu
        file_menu = self.addMenu("File")
        new_file_action = QAction("New File", self)
        new_folder_action = QAction("New Folder", self)
        open_action = QAction("Open...", self)
        rename_action = QAction("Rename", self)
        delete_action = QAction("Delete", self)
        exit_action = QAction("Exit", self)

        file_menu.addAction(new_file_action)
        file_menu.addAction(new_folder_action)
        file_menu.addSeparator()
        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(rename_action)
        file_menu.addAction(delete_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        # Connect File Menu Actions
        
        new_folder_action.triggered.connect(self.new_folder)
        open_action.triggered.connect(self.open_file)
        rename_action.triggered.connect(self.rename_item)
        delete_action.triggered.connect(self.delete_item)
        exit_action.triggered.connect(self.close_app)

        # Edit Menu
        edit_menu = self.addMenu("Edit")
        cut_action = QAction("Cut", self)
        copy_action = QAction("Copy", self)
        paste_action = QAction("Paste", self)
        select_all_action = QAction("Select All", self)

        edit_menu.addAction(cut_action)
        edit_menu.addAction(copy_action)
        edit_menu.addAction(paste_action)
        edit_menu.addSeparator()
        edit_menu.addAction(select_all_action)

        # Connect Edit Menu Actions
        cut_action.triggered.connect(self.cut_item)
        copy_action.triggered.connect(self.copy_item)
        paste_action.triggered.connect(self.paste_item)
        select_all_action.triggered.connect(self.select_all)

        # View Menu
        view_menu = self.addMenu("View")
        icon_mode_action = QAction("Icon Mode", self)
        list_mode_action = QAction("List Mode", self)
        refresh_action = QAction("Refresh", self)

        view_menu.addAction(icon_mode_action)
        view_menu.addAction(list_mode_action)
        view_menu.addSeparator()
        view_menu.addAction(refresh_action)

        # Connect View Menu Actions
        icon_mode_action.triggered.connect(self.switch_to_icon_mode)
        list_mode_action.triggered.connect(self.switch_to_list_mode)
        refresh_action.triggered.connect(self.refresh_view)
        
        
        # Navigate Menu
    
        navigate_menu = self.addMenu("Navigate")
        back_action = QAction("Back", self)
        forward_action = QAction("Forward", self)
        up_action = QAction("Up", self)
        home_action = QAction("Home", self)
        favorites_action = QAction("Favorites/Quick Access", self)

        navigate_menu.addAction(back_action)
        navigate_menu.addAction(forward_action)
        navigate_menu.addAction(up_action)
        navigate_menu.addAction(home_action)
        navigate_menu.addSeparator()
        navigate_menu.addAction(favorites_action)

        # Connect Navigate Menu Actions
        back_action.triggered.connect(self.navigate_back)
        forward_action.triggered.connect(self.navigate_forward)
        up_action.triggered.connect(self.navigate_up)
        home_action.triggered.connect(self.navigate_home)
        favorites_action.triggered.connect(self.navigate_favorites)

        # Tools Menu
    
        tools_menu = self.addMenu("Tools")
        search_action = QAction("Search", self)
        batch_rename_action = QAction("Batch Rename", self)
        properties_action = QAction("Properties", self)

        tools_menu.addAction(search_action)
        tools_menu.addAction(batch_rename_action)
        tools_menu.addAction(properties_action)

        # Connect Tools Menu Actions
        search_action.triggered.connect(self.open_search_dialog)
        batch_rename_action.triggered.connect(self.batch_rename)
        properties_action.triggered.connect(self.open_properties_dialog)

        # Help Menu
        help_menu = self.addMenu("Help")
        about_action = QAction("About", self)
        help_menu.addAction(about_action)

        # Connect Help Menu Actions
        about_action.triggered.connect(self.show_about_dialog)

    # File Menu Actions

    def new_folder(self):
        print("New Folder Created")

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "")
        if file_name:
            print(f"Opened file: {file_name}")

    def rename_item(self):
        print("Item Renamed")

    def delete_item(self):
        print("Item Deleted")

    def close_app(self):
        if self.parent():
            self.parent().close()

    # Edit Menu Actions
    def cut_item(self):
        print("Cut Item")

    def copy_item(self):
        print("Copy Item")

    def paste_item(self):
        print("Paste Item")

    def select_all(self):
        print("Select All Items")

    # View Menu Actions
    def switch_to_icon_mode(self):
        self.switch_to_icon_mode_signal.emit()
        

    def switch_to_list_mode(self):
        self.switch_to_list_mode_signal.emit()

    def refresh_view(self):
        print("View Refreshed")

    # Navigate Menu Actions
    def navigate_back(self):
        print("Navigated Back")

    def navigate_forward(self):
        print("Navigated Forward")

    def navigate_up(self):
        print("Navigated Up")

    def navigate_home(self):
        print("Navigated to Home")

    def navigate_favorites(self):
        print("Navigated to Favorites/Quick Access")

    # Tools Menu Actions
    def open_search_dialog(self):
        print("Opened Search Dialog")

    def batch_rename(self):
        print("Batch Rename")

    def open_properties_dialog(self):
        print("Opened Properties Dialog")

    # Help Menu Actions
    def show_about_dialog(self):
        QMessageBox.about(self, "About", "File Explorer Application\nVersion 1.0")



# # for debugging
# app = QApplication([])
# menu_bar = MenuBar()
# menu_bar.show()
# app.exec()