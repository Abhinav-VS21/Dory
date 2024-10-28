from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QCheckBox, QPushButton, QApplication,
    QComboBox, QListWidget, QListWidgetItem, QHBoxLayout, QLabel, QProgressBar, QMessageBox , QApplication , QCompleter 
)
from PySide6.QtCore import  QThread, Signal, QStringListModel
from DirectoryCompleter import DirectoryCompleter
import os 

class SearchThread(QThread):
    # This thread will handle searching to keep the UI responsive
    resultsReady = Signal(list)
    
    def __init__(self, search_dir, name ,search_type, case_sensitive, ignore_extension, parent=None):
        super().__init__(parent)
        self.search_dir = str(search_dir)
        self.name = str(name)
        self.search_type = str(search_type)
        self.case_sensitive = bool(case_sensitive)
        self.ignore_extension = bool(ignore_extension)
        
    
    def run(self):
        
        results = list()
        
        if self.search_type == "Directories":
            results = self.search_directories()
            
        elif self.search_type == "Files":
            results = self.search_files()
            
        elif self.search_type == "Both":
            results = self.search_directories()
            results.extend(self.search_files())
        
        self.resultsReady.emit(results)
        
    def search_directories(self):
        matching_directories = []
        
        for dirpath, dirnames, filenames in os.walk(self.search_dir):
            for dirname in dirnames:
                if self.case_sensitive:
                    if self.name in dirname:
                        matching_directories.append( os.path.join(dirpath, dirname))
                else:
                    if self.name.lower() in dirname.lower():
                        matching_directories.append(os.path.join(dirpath, dirname))
        return matching_directories
    
    def search_files(self):
        matching_files = []
        
        for dirpath, dirnames, filenames in os.walk(self.search_dir):
            for filename in filenames:
                base_name, ext = os.path.splitext(filename)
                if self.ignore_extension:
                    match_name = base_name
                else:
                    match_name = filename
                
                if self.case_sensitive:
                    if self.name in match_name:
                        matching_files.append( os.path.join(dirpath, filename))
                else:
                    if self.name.lower() in match_name.lower():
                        matching_files.append( os.path.join(dirpath, filename))
        return matching_files
        
        

class SearchDialog(QDialog):
    
    select_parent_folder_path = Signal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Search")
        self.setMinimumSize(400, 300)
        
        # Layouts
        layout = QVBoxLayout()

        # Search Input
        self.search_dir_input = QLineEdit()
        self.search_dir_input.setPlaceholderText("Enter Directory to search ...")
        
        # Completer
        self.completer = DirectoryCompleter(self.search_dir_input)
        # self.search_dir_input.setCompleter(self.completer)
        # self.search_dir_input.textChanged.connect(self.updateCompleter)
        
        # Search Name
        self.search_name_input = QLineEdit()
        self.search_name_input.setPlaceholderText("Enter search name...")
        
        # Options (ComboBox for search type, checkboxes for additional options)
        options_layout = QHBoxLayout()
        
        self.search_type_combo = QComboBox()
        self.search_type_combo.addItems(["Directories", "Files", "Both"])
        
        self.case_sensitive_checkbox = QCheckBox("Case Sensitive")
        self.ignore_extension_checkbox = QCheckBox("Ignore Extensions")
        
        options_layout.addWidget(self.search_type_combo)
        options_layout.addWidget(self.case_sensitive_checkbox)
        options_layout.addWidget(self.ignore_extension_checkbox)
        
        # Search Button
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.startSearch)
        
        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        # Results List
        self.result_list = QListWidget()
        self.result_list.itemDoubleClicked.connect(self.openSelectedResult)
        
        # Open Button
        open_button = QPushButton("Open Selected")
        open_button.clicked.connect(self.openSelectedResult)
        
        # Add to layout
        layout.addWidget(self.search_dir_input)
        layout.addWidget(self.search_name_input)
        layout.addLayout(options_layout)
        layout.addWidget(self.search_button)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.result_list)
        layout.addWidget(open_button)
        
        self.setLayout(layout)
    
    def startSearch(self):
        # Read user inputs
        search_dir = self.search_dir_input.text()
        name = self.search_name_input.text()
        search_type = self.search_type_combo.currentText()
        case_sensitive = self.case_sensitive_checkbox.isChecked()
        ignore_extension = self.ignore_extension_checkbox.isChecked()
        
        if not search_dir:
            QMessageBox.warning(self, "Input Error", "Please enter a search query.")
            return
        
        if not name:
            QMessageBox.warning(self, "Input Error", "Please enter a search name.")
            return
        
        
        
        if not os.path.isdir(search_dir):
            QMessageBox.warning(self, "Input Error", "Invalid directory.")
            return
        
        # Show progress bar
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate
        
        # Start the search on a separate thread
        self.search_thread = SearchThread(search_dir, name ,search_type, case_sensitive, ignore_extension)
        self.search_thread.resultsReady.connect(self.displaySearchResults)
        self.search_thread.start()
    
    def displaySearchResults(self, results):
        # Hide the progress bar
        self.progress_bar.setVisible(False)
        
        # Clear current results
        self.result_list.clear()
        
        if not results:
            QMessageBox.information(self, "No Results", "No matching files or directories found.")
            return
        
        # Populate the list with new results
        for file_path in results:
            item = QListWidgetItem(file_path)
            self.result_list.addItem(item)
    
    def openSelectedResult(self):
        selected_item = self.result_list.currentItem()
        if selected_item:
            file_path = selected_item.text()
            # Here, implement logic to open/navigate to the selected parent directory
            self.select_parent_folder_path.emit(os.path.dirname(file_path))
            
            print(f"Opening: {file_path}")


# Debugging
# app = QApplication([])
# dialog = SearchDialog()
# dialog.show()
# app.exec()
