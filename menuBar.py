from PySide6.QtWidgets import QMenuBar, QInputDialog, QMessageBox, QApplication, QDialog , QVBoxLayout , QListWidget
from PySide6.QtGui import QAction 
from PySide6.QtCore import Signal , QDir
from searchDialog import SearchDialog
import os

class MenuBar(QMenuBar):
    
    # Defining Refresh Signals
    refresh_view_signal = Signal()
    
    # Defining View Signals
    switch_to_icon_mode_signal = Signal()
    switch_to_list_mode_signal = Signal()
    
    # Defining switching directories to view signals
    switch_to_new_icon_list_root_index = Signal(str)   
    
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_menu()

    def init_menu(self):
        # create menu
        create_menu = self.addMenu("Create")
        create_new_file = QAction("Create New File" ,self)
        create_new_folder = QAction("Create New Folder",self)
        create_menu.addAction(create_new_folder)
        create_menu.addAction(create_new_file)
        
        #connect create menu actions
        create_new_file.triggered.connect(self.createNewFile)
        create_new_folder.triggered.connect(self.createNewFolder)
    
        
        # View Menu
        view_menu = self.addMenu("View")
        icon_mode_action = QAction("Icon Mode", self)
        list_mode_action = QAction("List Mode", self)
        refresh_action = QAction("Refresh", self)

        view_menu.addAction(icon_mode_action)
        view_menu.addAction(list_mode_action)
        view_menu.addAction(refresh_action)

        # Connect View Menu Actions
        icon_mode_action.triggered.connect(self.switchToIconMode)
        list_mode_action.triggered.connect(self.switchToListMode)
        refresh_action.triggered.connect(self.refreshView)


        # Tools Menu
        tools_menu = self.addMenu("Tools")
        
        search_action = QAction("Search", self)
        bookmark_action = QAction("Bookmark", self)
        properties_action = QAction("Properties", self)

        tools_menu.addAction(search_action)
        tools_menu.addAction(bookmark_action)
        tools_menu.addAction(properties_action)
        
        # Connect Tools Menu Actions
        search_action.triggered.connect(self.openSearchDialog)
        properties_action.triggered.connect(self.openPropertiesDialog)
        bookmark_action.triggered.connect(self.createBookmark)
        
        
        # QuickAccess Menu 
        quick_access_menu = self.addMenu("Quick Access")
        
        go_to_home_action = QAction("Go to Home", self)
        go_to_root_action = QAction("Go to Root", self)
        
        quick_access_menu.addAction(go_to_home_action)
        quick_access_menu.addAction(go_to_root_action)
        
        bookmark_menu = quick_access_menu.addMenu("Bookmarks")
        
        # Connect QuickAccess Menu Actions
        go_to_home_action.triggered.connect(self.goToHome)
        go_to_root_action.triggered.connect(self.goToRoot)
        
        
        
        
        
        # Help Menu
        help_menu = self.addMenu("Help")
        about_action = QAction("About", self)
        help_menu.addAction(about_action)

        # Connect Help Menu Actions
        about_action.triggered.connect(self.showAboutDialog)

    # Create Menu Actions
    def createNewFile(self):
        print("Creating a New File Action")
        
        current_directory = self.parent().getCurrentDirectory()
        
        file_name, ok = QInputDialog.getText(self, "New File", "Enter the file name:")
        
        if ok and file_name:
            # Create the full path for the new file
            file_path = os.path.join(current_directory, file_name)

            try:
                # Create the new file
                with open(file_path, 'w') as new_file:
                    # Optionally, write some default content
                    new_file.write("")  # Empty file
                QMessageBox.information(self, "Success", f"File '{file_name}' created successfully.")
                
                # Refresh the icon view to show the new file
                self.refreshView()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create file: {str(e)}")

    def createNewFolder(self):
        print("Create New Folder Action")
        
        current_directory = self.parent().getCurrentDirectory()
        dir_name, ok = QInputDialog.getText(self, "New Folder", "Enter the folder name:")
        
        

        
        if ok and dir_name:
            # Create the full path for the new folder
            dir_path = os.path.join(current_directory, dir_name)
            
            if os.path.exists(dir_path):
                QMessageBox.warning(self, "Warning", f"Folder '{dir_name}' already exists.")
                return
            
            try:
                # Create the new folder
                os.makedirs(dir_path)
                QMessageBox.information(self, "Success", f"Folder '{dir_name}' created successfully.")
                
                # Refresh the icon view to show the new folder
                self.refreshView()
            except PermissionError:
                QMessageBox.critical(self, "Error", f"Permission denied: Unable to create folder '{dir_name}'.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create folder: {str(e)}")

    

    # View Menu Actions
    def switchToIconMode(self):
        self.switch_to_icon_mode_signal.emit()

    def switchToListMode(self):
        self.switch_to_list_mode_signal.emit()

    def refreshView(self):
        self.refresh_view_signal.emit()
        print("View Refreshed")

    # Tools Menu Actions
    def openSearchDialog(self):
        print("Opened Search Dialog")
        search_dialog = SearchDialog()
        search_dialog.select_parent_folder_path.connect(self.setNewIconListRootIndex)
        search_dialog.exec()
    
    def setNewIconListRootIndex(self , directory):
        self.switch_to_new_icon_list_root_index.emit(directory)
        
    def openPropertiesDialog(self):
        print("Opened Properties Dialog")
        
        
    # Quick Access Menu Actions
    
    def goToHome(self):
        print("Go to Home Action")
        self.switch_to_new_icon_list_root_index.emit(QDir.homePath())
        
    def goToRoot(self):
        print("Go to Root Action")
        self.switch_to_new_icon_list_root_index.emit(QDir.rootPath())    
    
    def createBookmark(self):
        pass
    
    # Help Menu Actions
    def showAboutDialog(self):
        QMessageBox.about(self, "About", "File Explorer Application\nVersion 1.0")



# # for debugging
# app = QApplication([])
# menu_bar = MenuBar()
# menu_bar.show()
# app.exec()