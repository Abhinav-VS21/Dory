from PySide6.QtCore import QProcess
import shutil


class TerminalOpener:
    """
    A utility class to open terminal windows across different Linux distributions.
    Supports common terminal emulators like gnome-terminal, konsole, xterm, etc.
    """
    
    def __init__(self):
        # List of common terminal emulators and their launch commands
        self.terminals = {
            'gnome-terminal': ['gnome-terminal', '--'],
            'konsole': ['konsole', '-e'],
            'xfce4-terminal': ['xfce4-terminal', '-x'],
            'xterm': ['xterm', '-e'],
            'terminator': ['terminator', '-x'],
            'mate-terminal': ['mate-terminal', '-x'],
            'kitty': ['kitty'],
            'alacritty': ['alacritty']
        }
        
        # Find available terminal emulator
        self.default_terminal = self._find_terminal()
        
    def _find_terminal(self):
        """Find the first available terminal emulator."""
        for terminal in self.terminals:
            if shutil.which(terminal):
                return terminal
        return None
    
    def open_terminal(self, working_dir=None, command=None):
        """
        Open a new terminal window.
        
        Args:
            working_dir (str, optional): Working directory for the new terminal
            command (str, optional): Command to execute in the new terminal
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.default_terminal:
            raise RuntimeError("No terminal emulator found!")
            
        process = QProcess()
        
        # Set working directory if specified
        if working_dir:
            process.setWorkingDirectory(working_dir)
        
        # Prepare command
        cmd_list = self.terminals[self.default_terminal].copy()
        
        # Add the command if specified
        if command:
            if self.default_terminal in ['kitty', 'alacritty']:
                cmd_list.extend(['-e', command])
            else:
                cmd_list.append(command)
                
        # Start the process
        process.startDetached(cmd_list[0], cmd_list[1:])
        
        return True
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    terminal = TerminalOpener()
    
    # Open terminal in specific directory with a command
    terminal.open_terminal(
        working_dir="/home/MissShah_21",
        command="echo 'Hello from new terminal!'"
    )
    
    sys.exit(app.exec())
