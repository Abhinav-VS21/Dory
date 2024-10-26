from PySide6.QtWidgets import QMenuBar, QInputDialog, QMessageBox, QApplication, QDialog , QVBoxLayout , QListWidget
from PySide6.QtGui import QAction 
from PySide6.QtCore import Signal
import os

class MenuBar(QMenuBar):
    
    # Defining Refresh Signals
    refresh_view_signal = Signal()
    
    # Defining View Signals
    switch_to_icon_mode_signal = Signal()
    switch_to_list_mode_signal = Signal()
    
    
    # Defining Tools Signals
    open_search_dialog_signal = Signal()
    batch_rename_signal = Signal()
    open_properties_dialog_signal = Signal()
    open_quick_access_signal = Signal()
    create_bookmark_signal = Signal()
    go_to_home_signal = Signal()
    
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
        batch_rename_action = QAction("Batch Rename", self)
        properties_action = QAction("Properties", self)
        quick_access_action = QAction("Quick Access", self)
        bookmark_action = QAction("Bookmark", self)
        go_to_home_action = QAction("Home", self)

        tools_menu.addAction(search_action)
        tools_menu.addAction(batch_rename_action)
        tools_menu.addAction(properties_action)
        tools_menu.addAction(quick_access_action)
        tools_menu.addAction(bookmark_action)
        tools_menu.addAction(go_to_home_action)
        
        
        # Connect Tools Menu Actions
        search_action.triggered.connect(self.openSearchDialog)
        batch_rename_action.triggered.connect(self.batchRename)
        properties_action.triggered.connect(self.openPropertiesDialog)
        quick_access_action.triggered.connect(self.openQuickAccess)
        bookmark_action.triggered.connect(self.createBookmark)
        go_to_home_action.triggered.connect(self.goToHome)
        
        
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
        self.search_files()

    def get_search_parameters(self):
        # Get search directory
        search_directory = QInputDialog.getText(self, "Search Directory", "Enter directory to search:")
        
        # Get file name
        file_name = QInputDialog.getText(self, "File Name", "Enter file name to search:")
        
        # Get case sensitivity option
        case_sensitive = QInputDialog.getItem(self, "Case Sensitivity", "Case Sensitive:", ["Yes", "No"], 0, False)
        
        ignore_extension = QInputDialog.getItem(self, "Ignore Extension", "Ignore File Extension:", ["Yes", "No"], 0, False)

        return search_directory[0], file_name[0], case_sensitive == "Yes", ignore_extension == "Yes"
    
    def search_files(self):
        search_directory, file_name, case_sensitive, ignore_extension = self.get_search_parameters()
        
        if not os.path.isdir(search_directory):
            QMessageBox.warning(self, "Warning", "Invalid directory.")
            return

        results = []
        
        for root, dirs, files in os.walk(search_directory):
            for name in files:
                # Adjust matching based on options
                base_name, ext = os.path.splitext(name)
                if ignore_extension:
                    match_name = base_name
                else:
                    match_name = name

                if case_sensitive:
                    if file_name in match_name:
                        results.append(os.path.join(root, name))
                else:
                    if file_name.lower() in match_name.lower():
                        results.append(os.path.join(root, name))

        if results:
            self.display_results(results)
        else:
            QMessageBox.information(self, "No Results", "No matching files found.")
            
    def display_results(self, results):
        result_dialog = QDialog(self)
        result_dialog.setWindowTitle("Search Results")
        layout = QVBoxLayout(result_dialog)

        list_widget = QListWidget(result_dialog)
        layout.addWidget(list_widget)

        for file in results:
            list_widget.addItem(file)

        result_dialog.setLayout(layout)
        result_dialog.exec()

    def batchRename(self):
        print("Batch Rename")

    def openPropertiesDialog(self):
        print("Opened Properties Dialog")
        
    def openQuickAccess(self):
        print("Opened Quick Access")
    
    def createBookmark(self):
        print("Created Bookmark")
    
    def goToHome(self):
        print("Home")

    # Help Menu Actions
    def showAboutDialog(self):
        QMessageBox.about(self, "About", "File Explorer Application\nVersion 1.0")



# # for debugging
# app = QApplication([])
# menu_bar = MenuBar()
# menu_bar.show()
# app.exec()