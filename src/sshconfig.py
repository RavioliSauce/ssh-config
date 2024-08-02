from PySide6 import QtWidgets, QtCore, QtGui

class SSHConfig(QtWidgets.QDialog):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SSH Config")
        self.setMinimumHeight(100)
        self.setMinimumWidth(400)
        
        config = self.load()
        self.parse(config)
        
        main_layout = QtWidgets.QGridLayout(self)
        
        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.addItems(["Host1", "Host2", "Host3"])
        
        self.input_layout = QtWidgets.QVBoxLayout()
        self.hostname_label = QtWidgets.QLabel("Hostname:")
        self.hostname_input = QtWidgets.QLineEdit()
        self.port_label = QtWidgets.QLabel("Port:")
        self.port_input = QtWidgets.QLineEdit()
        self.user_label = QtWidgets.QLabel("User:")
        self.user_input = QtWidgets.QLineEdit()
        self.private_key_label = QtWidgets.QLabel("Private Key:")
        self.private_key_input = QtWidgets.QLineEdit()
        self.keepalive_label = QtWidgets.QLabel("Keepalive:")
        self.keepalive_input = QtWidgets.QLineEdit()
        self.save_button = QtWidgets.QPushButton("Save")

        self.input_layout.addWidget(self.hostname_label)
        self.input_layout.addWidget(self.hostname_input)
        self.input_layout.addWidget(self.port_label)
        self.input_layout.addWidget(self.port_input)
        self.input_layout.addWidget(self.user_label)
        self.input_layout.addWidget(self.user_input)
        self.input_layout.addWidget(self.private_key_label)
        self.input_layout.addWidget(self.private_key_input)
        self.input_layout.addWidget(self.save_button)
        
        input_container = QtWidgets.QWidget()
        input_container.setLayout(self.input_layout)
        
        main_layout.addWidget(self.list_widget, 0, 0)
        main_layout.addWidget(input_container, 0, 1)        
        
        main_layout.setColumnStretch(0, 1)
        main_layout.setColumnStretch(1, 2)
        
    def load(self):
        home = QtCore.QDir.homePath()
        with open(f"{home}/.ssh/config") as f:
            print(f.read())
            return f.read()
        
    def parse(self, config):
        """Parse the SSH config file and populate the list widget"""
        hosts = {}
        