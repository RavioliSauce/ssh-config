from PySide6 import QtWidgets, QtCore

class SSHConfig(QtWidgets.QDialog):
    
    def __init__(self):
        super().__init__()
        
        self.text = QtWidgets.QLabel("Hello World", alignment=QtCore.Qt.AlignCenter)
        
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)