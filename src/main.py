import sys
import random
from PySide6 import QtWidgets, QtCore
from sshconfig import SSHConfig
        
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    font = app.font()
    font.setPointSize(12)
    app.setFont(font)
    
    widget = SSHConfig()
    widget.show()
    
    sys.exit(app.exec())