from PySide6.QtCore import QThread , Signal 
from PySide6.QtGui import QStandardItem
import os
import time
import mimetypes

class SearchThread(QThread):
    
    #Signals 
    list_of_file_items = Signal(list)
    
    def __init__(self ,  search_text:str ,  case_sensitive:bool , recursive_search:bool ,
                 full_match_search :bool, current_directory:str ,parent = None):
        
        super().__init__(parent)
        self.search_text = 'temp.py'
        self.case_sensitive = False
        self.recursive_search = True
        self.full_match_search = False
        self.current_directory = '/home/MissShah_21'
        
   
    def searchFiles(self):
        
        def sizeof_fmt(num, suffix="B"):
            for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
                if abs(num) < 1024.0:
                    return f"{num:3.1f}{unit}{suffix}"
                num /= 1024.0
            return f"{num:.1f}Yi{suffix}"


        results = []
        iterator = os.walk(self.current_directory) if self.recursive_search else os.walk(self.current_directory)
        
        for dirpath, dirnames, filenames in iterator:
            for filename in filenames:
                
                if self.full_match_search:
                    # matches is a boolean value
                    matches = (
                        (filename == self.search_text) if self.case_sensitive else 
                        (filename.lower() == self.search_text.lower())
                    )
                else:
                    matches = (
                        (self.search_text in filename) if self.case_sensitive else 
                        (self.search_text.lower() in filename.lower())
                    )
                    
                if matches:
                    file_path = os.path.join(dirpath, filename)
                    file_size = sizeof_fmt(os.path.getsize(file_path))
                    last_modified = time.ctime(os.path.getmtime(file_path))
                    file_type = mimetypes.guess_type(file_path)[0]
                    
                    name_item = QStandardItem(filename)
                    path_item = QStandardItem(file_path)
                    size_item = QStandardItem(file_size)
                    modified_item = QStandardItem(last_modified)
                    type_item = QStandardItem(file_type)
                    
                    results.append((name_item, path_item, size_item, modified_item, type_item))
                    
        self.results_ready.emit(results)