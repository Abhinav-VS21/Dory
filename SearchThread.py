from PySide6.QtCore import QThread , Signal 
from PySide6.QtGui import QStandardItem , Qt
from catchExecptions import catch_exceptions
import os
import time
import mimetypes


class SearchThread(QThread):
    
    #Signals 
    list_of_file_items = Signal(list)
    
    
    @catch_exceptions
    def __init__(self , condition_dict: dict , current_directory : str ,parent = None):
        super().__init__(parent)
        print('thread initialised')
        self.current_directory = current_directory
        self.search_text = condition_dict['search_text']
        self.case_sensitive = condition_dict['case_sensitive']
        self.recursive_search = condition_dict['recursive_search']
        self.full_match_search = condition_dict['full_match_search']
        
        
    @catch_exceptions
    def searchFiles(self):
        
        def sizeof_fmt(num, suffix="B"):
            for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
                if abs(num) < 1024.0:
                    return f"{num:3.1f}{unit}{suffix}"
                num /= 1024.0
            return f"{num:.1f}Yi{suffix}"


        results = []
        
        for dirpath, dirnames, filenames in os.walk(self.current_directory):
            
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
                    file_size = os.path.getsize(file_path)
                    last_modified = time.ctime(os.path.getmtime(file_path))
                    file_type = mimetypes.guess_type(file_path)[0] or "Unknown"
                    
                    
                    # create a tuple of the file item
                    file_tuple = (filename , file_path , file_size , file_type , last_modified)    
                    
                    results.append(file_tuple)
          
            if not self.recursive_search:
                dirnames.clear()     
        return results
    
    
    def run(self):
        print('running the file')
        results = self.searchFiles()
        print('emiting list of files')
        self.list_of_file_items.emit(results)