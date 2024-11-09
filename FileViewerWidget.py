from PySide6.QtWidgets import  (QListView , QFileSystemModel ,QMenu ,
                                QMessageBox , QDialog , QLabel , QVBoxLayout,
                                QPushButton,QFormLayout , QAbstractItemView)

from PySide6.QtCore import QDir , Signal , Qt , QFile , QSize
from PySide6.QtGui import QAction
from catchExecptions import catch_exceptions
from editableFileSystemModel import EditableFileSystemModel
import os
import random
import time
import shutil
import subprocess
import platform


class FileListViewer(QListView):
    #Signals
    open_file           = Signal(str)
    open_folder         = Signal(str)
    open_in_new_window  = Signal(str)
    add_bookmark_path   = Signal((str,str))
    copy_file_signal    = Signal(str)
    cut_file_signal     = Signal(str)
    copy_folder_signal  = Signal(str)
    cut_folder_signal   = Signal(str)
    paste_signal        = Signal(str)
    
    
    @catch_exceptions
    def __init__(self, root_directory = QDir.homePath()) -> None:
        super().__init__()
        
        
        # Setting up the directory model
        self.directory_model = EditableFileSystemModel()
        self.directory_model.setRootPath(root_directory)
        self.directory_model.setFilter(QDir.Files | QDir.NoDotAndDotDot | QDir.AllDirs)
        self.reverse_order_action = QAction("Reverse Order", self, checkable=True)
        
        
        # Setting up the file list view
        self.setModel(self.directory_model)
        self.setRootIndex(self.directory_model.index(root_directory))
        self.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked | QAbstractItemView.EditTrigger.SelectedClicked)

        # Persistent context menu action 
        self.show_hidden_files_action = QAction("Show Hidden Files", self , checkable = True)
        self.current_size = 70
        
        # Defining connections
        self.doubleClicked.connect(self.onDoubleClicked)
        
        # Initialize settings
        self.initSettings()
        
    @catch_exceptions
    def initSettings(self):
        self.setIconView()
        
    # Defining the slots
    @catch_exceptions
    def onDoubleClicked(self, index):
        if not index.isValid():
            print("Invalid index in FileListWidget")
            return
        path = self.directory_model.filePath(index)
        if self.directory_model.isDir(index):
            self.open_folder.emit(path)
        else:
            self.open_file.emit(path)
                   
    @catch_exceptions
    def contextMenuEvent(self, event):
        index = self.indexAt(event.pos())
        menu = QMenu(self)
        
        if index.isValid():
            print('double click on file or folder')
            if self.directory_model.isDir(index):
                # Context Menu for a folder
                open_folder_action = QAction("Open", self)
                open_folder_new_window_action = QAction("Open in New Window", self)
                cut_folder_action = QAction("Cut", self)
                copy_folder_action = QAction("Copy", self)
                bookmark_action = QAction("Bookmark", self)
                delete_folder_action = QAction("Delete", self)             # Implimentation done in class
                rename_folder_action = QAction("Rename", self)             # Implimentation done in class
                properties_folder_action = QAction("Properties", self)     # Implimentation done in class
                open_folder_in_terminal_action = QAction("Open in Terminal", self)  
                
                menu.addActions([open_folder_action, open_folder_new_window_action, 
                                 cut_folder_action, copy_folder_action, bookmark_action, 
                                 delete_folder_action, rename_folder_action, properties_folder_action , open_folder_in_terminal_action])
                
                open_folder_action.triggered.connect(lambda: self.open_folder.emit(self.directory_model.filePath(index)))
                open_folder_new_window_action.triggered.connect(lambda: self.open_in_new_window.emit(self.directory_model.filePath(index)))
                bookmark_action.triggered.connect(lambda: self.add_bookmark_path.emit((self.directory_model.filePath(index), self.directory_model.fileName(index))))
                cut_folder_action.triggered.connect(lambda: self.cut_folder_signal.emit(self.directory_model.filePath(index)))
                copy_folder_action.triggered.connect(lambda: self.copy_folder_signal.emit(self.directory_model.filePath(index)))
                delete_folder_action.triggered.connect(lambda: self.deleteRecursively(index)) # doesnt work
                rename_folder_action.triggered.connect(lambda: self.renameFolder(index))
                properties_folder_action.triggered.connect(lambda: self.propertiesFolder(index))
                open_folder_in_terminal_action.triggered.connect(lambda: self.openInTerminal(self.directory_model.filePath(index)))
            
            else:
                
                open_file_action = QAction("Open file", self)
                cut_file_action = QAction("Cut", self)
                copy_file_action = QAction("Copy", self)
                rename_file_action = QAction("Rename", self)
                delete_file_action = QAction("Delete", self)
                properties_file_action = QAction("Properties", self)
                
                menu.addActions([open_file_action, cut_file_action, copy_file_action, 
                                 rename_file_action, delete_file_action,
                                 properties_file_action])
        
                open_file_action.triggered.connect(lambda: self.open_file.emit(self.directory_model.filePath(index)))
                cut_file_action.triggered.connect(lambda: self.cut_file_signal.emit(self.directory_model.filePath(index)))
                copy_file_action.triggered.connect(lambda: self.copy_file_signal.emit(self.directory_model.filePath(index)))
                rename_file_action.triggered.connect(lambda: self.renameFile(index))
                delete_file_action.triggered.connect(lambda: self.directory_model.remove(index))
                properties_file_action.triggered.connect(lambda: self.propertiesFile(index))
                
        else:
            print('double click on empty space')
            
            # Context Menu for the empty space
            paste_action = QAction("Paste", self)
            create_file_action = QAction("Create File", self)
            create_folder_action = QAction("Create Folder", self)
            open_in_terminal_action = QAction("Open in Terminal", self)
            curr_dir_properties_action = QAction("Properties", self)
            sort_by_menu = menu.addMenu("Sort By")
            sort_by_name_action = QAction("Name", self)
            sort_by_size_action = QAction("Size", self)
            sort_by_date_action = QAction("Date Modified", self)
            
            
            sort_by_menu.addActions([sort_by_name_action, sort_by_size_action, sort_by_date_action , self.reverse_order_action])

            menu.addActions([paste_action, create_file_action, create_folder_action, 
                             open_in_terminal_action, self.show_hidden_files_action, 
                             curr_dir_properties_action])
            
            paste_action.triggered.connect(lambda : self.paste())
            create_file_action.triggered.connect(lambda: self.createNewFile())
            create_folder_action.triggered.connect(lambda: self.createNewFolder())
            open_in_terminal_action.triggered.connect(lambda: self.openInTerminal())
            self.show_hidden_files_action.triggered.connect(lambda bool: self.directory_model.toggleHiddenFiles(bool))
            curr_dir_properties_action.triggered.connect(lambda: self.currDirProperties())
            sort_by_name_action.triggered.connect(lambda: self.sortBy(0))
            sort_by_size_action.triggered.connect(lambda: self.sortBy(1))
            sort_by_date_action.triggered.connect(lambda: self.sortBy(3))
            self.reverse_order_action.triggered.connect(lambda: self.sortBy(0, True))
            
        # Show the context menu at the cursor position
        menu.exec(event.globalPos())
                 
    @catch_exceptions
    def updateRootIndex(self, directory : str):
        """Sets the new root index of the file list viewer""" 
         
        newRootIndex = self.directory_model.index(directory)
        if not newRootIndex.isValid():
            print('The new root index is not valid')
            return
        
        self.setRootIndex(newRootIndex)
                  
    @catch_exceptions
    def refreshView(self):
        self.directory_model.setRootPath(self.directory_model.rootPath())

    @catch_exceptions
    def setIconView(self):
        self.setViewMode(QListView.IconMode)
        self.setIconSize(QSize(self.current_size , self.current_size))
        self.setGridSize(QSize(self.current_size + 30 ,self.current_size + 30))
        self.setResizeMode(QListView.Adjust)
        self.setFlow(QListView.LeftToRight)
        
    @catch_exceptions
    def setListView(self):
        self.setViewMode(QListView.ListMode)
        self.setIconSize(QSize(30,30))
        self.setGridSize(QSize())
        self.setResizeMode(QListView.Adjust)
        self.setWordWrap(True)
        self.setFlow(QListView.TopToBottom)
          
        self.current_size = 30
    @catch_exceptions
    def changeIconSize(self,size:int):
        """Change icon size in QListView if in IconMode."""
        print('Changing icon size to:', size)
        self.current_size = size
        if self.viewMode() == QListView.IconMode :
            self.setIconSize(QSize(size,size))
            self.setGridSize(QSize(size + 30 , size + 30))
                
    @catch_exceptions
    def getCurrentDirectoryPath(self):
        return self.directory_model.filePath(self.rootIndex())
    
    
    @catch_exceptions
    def hideSelf(self):
        self.hide()
    
    
    @catch_exceptions
    def showSelf(self):
        self.show()
        
    
    # File operations
    @catch_exceptions
    def createNewFile(self):
        current_dir = self.getCurrentDirectoryPath()
        random_file_name = 'new_file' + str(random.randint(1,1000)) + '.txt'
        full_path = os.path.join(current_dir, random_file_name)
        
        try:
            with open(full_path, 'w') as new_file:
                new_file.write('')
                            
            # Refresh the icon view to show the new file
            self.refreshView()
            
        except PermissionError:
                QMessageBox.critical(self, "Error", f"Permission denied: Unable to create file '{full_path}'.")
        except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create file: {str(e)}")

        file_index = self.directory_model.index(full_path)
        self.renameFile(file_index)
        
        
    @catch_exceptions
    def createNewFolder(self):
        current_dir = self.getCurrentDirectoryPath()
        random_folder_name = 'new_folder' + str(random.randint(1,1000))
        full_path = os.path.join(current_dir, random_folder_name)
        
        try:
            os.makedirs(full_path)
        except PermissionError:
            QMessageBox.critical(self, "Error", f"Permission denied: Unable to create folder '{full_path}'.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create folder: {str(e)}")
            
        self.renameFile(self.directory_model.index(full_path))
        
    @catch_exceptions
    def onFileRenamed(self, topLeft, bottomRight):
        
        """Handles the file rename operation."""
        
        index = topLeft
        if index.isValid():
            old_path = self.directory_model.filePath(index)
            new_name = self.directory_model.fileName(index)
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            
            # Check if the rename was successful (if the path has changed)
            if old_path != new_path and not QFile(new_path).exists():
                if not os.rename(old_path, new_path):
                    QMessageBox.critical(self, "Error", "Failed to rename the file.")
            else:
                # Revert the change if the name is not valid
                self.directory_model.setData(index, os.path.basename(old_path), Qt.EditRole)  # Reset to old name
         
                QMessageBox.warning(self, "Warning", "Invalid file name or name already exists.")

    @catch_exceptions
    def onFolderRenamed(self, topLeft, bottomRight):
        """Handles the folder rename operation."""
        index = topLeft
        if index.isValid():
            old_path = self.directory_model.filePath(index)
            new_name = self.directory_model.fileName(index)
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            
            # Check if the rename was successful (if the path has changed)
            if old_path != new_path and not QFile(new_path).exists():
                if not os.rename(old_path, new_path):
                    QMessageBox.critical(self, "Error", "Failed to rename the folder.")
            else:
                # Revert the change if the name is not valid
                self.directory_model.setData(index, os.path.basename(old_path), Qt.EditRole)

    def renameFolder(self,index):
        ''' Puts the selected folder in rename mode '''
        if index.isValid():
            self.edit(index)
            self.directory_model.dataChanged.connect(self.onFolderRenamed)
        else:
            print('Invalid index in renameFolder')
    
    @catch_exceptions
    def renameFile(self,index):
        ''' Puts the selected file in rename mode '''
        if index.isValid():
            self.edit(index)
            self.directory_model.dataChanged.connect(self.onFileRenamed)
        else:
            print('Invalid index in renameFile')
            
            
    @catch_exceptions
    def propertiesFile(self,index):
        if not index.isValid():
            return
        
        file_path = self.directory_model.filePath(index)
        
        # Retrieve properties
        properties = {
            "File Name": self.directory_model.fileName(index),
            "Size": f"{os.path.getsize(file_path)} bytes",
            "Date Modified": time.ctime(os.path.getmtime(file_path)),
            "Type": self.directory_model.type(index)
        }
        
        dialog = PropertiesDialog("File Properties", properties)
        dialog.exec()
        
        
    @catch_exceptions
    def propertiesFolder(self,index):
        if not index.isValid():
            return
        
        folder_path = self.directory_model.filePath(index)
        
        # Retrieve properties
        try:
 
            properties = {
                "Folder Name": self.directory_model.fileName(index),
                "Number of Files": str(len(os.listdir(folder_path))),
                "Date Modified": time.ctime(os.path.getmtime(folder_path)),
                "Type": "Folder"
            }
            
            dialog = PropertiesDialog("Folder Properties", properties)
            dialog.exec()\
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to retrieve folder properties: {str(e)}")

    # widgets operations
    
    @catch_exceptions
    def paste(self):
        self.paste_signal.emit(self.getCurrentDirectoryPath())
    
    @catch_exceptions
    def openInTerminal(self , pwd = None):
        if pwd is None:
            current_dir = self.getCurrentDirectoryPath()  # Get the current directory path
        else:
            current_dir = pwd
            
        if not current_dir:
            print("No valid current directory to open in terminal.")
            return
        
        linux_terminals = {
        'gnome-terminal': '--working-directory',
        'konsole': '--workdir',
        'alacritty': '--working-directory',
        'xfce4-terminal': '--working-directory',
        'lxterminal': '--working-directory',
        'terminator': '--working-directory'
}

        print('Opening terminal in:', current_dir)
        try:
            if platform.system() == "Windows":  # Windows
                # Use 'start' to open the command prompt in the specified directory
                subprocess.Popen(f'start cmd /K "cd {current_dir}"', shell=True)
            elif platform.system() == "Darwin":  # macOS
                # Use 'open' with 'Terminal' to open the terminal in the specified directory
                subprocess.Popen(['open', '-a', 'Terminal', current_dir])
            elif platform.system() == "Linux":  # Linux
                for terminal , flag  in linux_terminals.items():
                    if shutil.which(terminal):
                        subprocess.Popen([terminal, flag, current_dir])
                        break
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open terminal: {str(e)}")


    @catch_exceptions
    def updateRootIndex(self, directory: str):
        """Sets the new root index of the file list viewer."""
        new_root_index = self.directory_model.index(directory)
        if not new_root_index.isValid():
            print("The new root index is not valid.")
            return

        self.setRootIndex(new_root_index)
    
    @catch_exceptions
    def currDirProperties(self):
        folder_path =  self.getCurrentDirectoryPath()
        
        # Retrieve properties
        try:
            properties = {
                "Folder Name": os.path.basename(folder_path),
                "Number of Files": str(len(os.listdir(folder_path))),
                "Date Modified": time.ctime(os.path.getmtime(folder_path)),
                "Type": "Folder"
            }
            
            dialog = PropertiesDialog("Folder Properties", properties)
            dialog.exec()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to retrieve folder properties: {str(e)}")

    @catch_exceptions
    def deleteRecursively(self,index):
        path = self.directory_model.filePath(index)
        
        reply = QMessageBox.question(
                self,
                "Confirm Deletion",
                f"Are you sure you want to delete '{path}' and all its contents?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
        if reply == QMessageBox.No:
            print("Deletion cancelled.")
            return
        
        if not os.path.exists(path):
            print("Invalid path in deleteRecursively")
            return
    
        for root , dirs , files in os.walk(path , topdown = False):
            for name in files:
                os.remove(os.path.join(root,name))
            for name in dirs:
                os.rmdir(os.path.join(root,name))
        
        os.rmdir(path)
        
    @catch_exceptions
    def sortBy(self , column , reverse = False):
        if reverse:
            order = Qt.AscendingOrder
        else:
            order = Qt.DescendingOrder
            
        self.directory_model.sort(column , order)
    
    
class PropertiesDialog(QDialog):
    @catch_exceptions
    def __init__(self, title, properties):
        super().__init__()
        self.setWindowTitle(title)
        layout = QVBoxLayout()

        form_layout = QFormLayout()
        for key, value in properties.items():
            form_layout.addRow(QLabel(key), QLabel(value))

        layout.addLayout(form_layout)

        button = QPushButton("Close")
        button.clicked.connect(self.accept)
        layout.addWidget(button)

        self.setLayout(layout)
        
    