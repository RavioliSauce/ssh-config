from PySide6 import QtWidgets, QtCore, QtGui
from pprint import pprint

def load():
    home = QtCore.QDir.homePath()
    with open(f"{home}/.ssh/config", 'r') as f:
        config = f.read()
        return config

def parse(config: str) -> dict:
    """Parse the SSH config file and populate the list widget"""
    hosts = {}
    current_host = None
    lines = config.splitlines()
    for line in lines:
        line = line.strip()
        if line.startswith("#") or not line:
            continue
        if line.startswith("Host "):
            current_host = line.split()[1]
            hosts[current_host] = {}
        elif current_host:
            key, value = line.split(None, 1)
            hosts[current_host][key] = value
    return hosts

class SSHConfig(QtWidgets.QDialog):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SSH Config")
        self.setMinimumHeight(100)
        self.setMinimumWidth(400)
        
        config_file = load()
        self.config = parse(config_file)
        
        main_layout = QtWidgets.QGridLayout(self)
        
        self.list_layout = QtWidgets.QVBoxLayout()
        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.addItems(self.config.keys())
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)
        self.list_widget.clicked.connect(self.load_host_config)
        self.list_widget.itemSelectionChanged.connect(self.load_host_config)
        self.list_widget.itemChanged.connect(self.rename_host)
        
        self.new_button = QtWidgets.QPushButton("New")
        self.new_button.clicked.connect(self.add_new_host)
        
        self.list_layout.addWidget(self.list_widget)
        self.list_layout.addWidget(self.new_button)
        
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
        self.input_layout.addWidget(self.keepalive_label)
        self.input_layout.addWidget(self.keepalive_input)
        self.input_layout.addWidget(self.save_button)
        
        input_container = QtWidgets.QWidget()
        input_container.setLayout(self.input_layout)
        
        list_container = QtWidgets.QWidget()
        list_container.setLayout(self.list_layout)
        
        main_layout.addWidget(list_container, 0, 0)
        main_layout.addWidget(input_container, 0, 1)        
        
        main_layout.setColumnStretch(0, 1)
        main_layout.setColumnStretch(1, 2)
        
        # get the QModelIndex of the first item in the list widget
        self.load_host_config(self.list_widget.indexFromItem(self.list_widget.item(0)))
        
    def rename_host(self, item: QtWidgets.QListWidgetItem):
        """Rename the host in the config dictionary"""
        index_as_int = self.list_widget.indexFromItem(item).row()
        old_name = list(self.config.keys())[index_as_int]
        new_name = item.text()
        if old_name and old_name in self.config:
            self.config[new_name] = self.config.pop(old_name)
        pprint(self.config)
        
    def load_host_config(self, current: QtCore.QModelIndex = None):
        """Load the selected host's configuration into the input fields"""
        if current:
            host = current.data()
            self.hostname_input.setText(self.config[host].get("HostName", ""))
            self.port_input.setText(self.config[host].get("Port", ""))
            self.user_input.setText(self.config[host].get("User", ""))
            self.private_key_input.setText(self.config[host].get("IdentityFile", ""))
            self.keepalive_input.setText(self.config[host].get("ServerAliveInterval", ""))
            
    def add_new_host(self):
        """Add a new host to the list widget"""
        new_host_name = "NewHost"
        new_item = QtWidgets.QListWidgetItem(new_host_name)
        new_item.setFlags(new_item.flags() | QtCore.Qt.ItemIsEditable)
        self.list_widget.addItem(new_item)
        self.config[new_host_name] = {
            "HostName": "",
            "Port": "",
            "User": "",
            "IdentityFile": "",
            "ServerAliveInterval": ""
        }
        self.list_widget.setCurrentItem(new_item)
            
    
if __name__ == "__main__":
    config = load()
    parsed_config = parse(config)
    pprint(parsed_config)
        