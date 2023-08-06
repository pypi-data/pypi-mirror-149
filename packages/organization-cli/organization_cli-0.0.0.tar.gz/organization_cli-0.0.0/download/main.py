import sys
import yaml
import os
import click
from pathlib import Path
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QLabel, QDialog
)
RESOURCES_DIR = Path(__file__).parent / 'resources'

class TestApp(QDialog):
    def __init__(self, data):
        super().__init__()
        self.app = QApplication([])
        self.window = QWidget()
        self.layout = QVBoxLayout(self.window)
        self._data = data
        self.full_employees_dict = {}
        self.tw = QTreeWidget()
        self.iconName = "icon.png"
        self.left = 800
        self.top = 300
        self.width = 800
        self.height = 300
        self.label = QLabel()
        self.vbox = QVBoxLayout()
        self.setup_ui()
        #self.tw.itemClicked.connect(self.handle_tree_item_clicked)


        self.run()

    def setup_ui(self):
        self.window.setWindowTitle("Organization Records")
        #QtGui.QIcon.addFile("icon.png")
        scriptDir = os.path.dirname(os.path.realpath('../icon.png'))
        self.window.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'icon.png'))
        self.window.setGeometry(self.left, self.top, self.width, self.height)
        self.tw.setHeaderLabels(['Team', 'First Name', 'Last Name', 'Role'])
        self.tw.setAlternatingRowColors(True)
        self.tw.setColumnWidth(0, 200)

    def run(self):
        self.display_data()
        self.layout.addWidget(self.tw)
        self.window.show()
        self.app.exec_()


    def display_data(self):
        num_deps = len(self._data[0])
        for i in range(num_deps):
            display_name = self._data[0][i]['display_name']
            employees = self._data[0][i]['employees']
            department = QTreeWidgetItem(self.tw, [display_name, None, None, None])
            for person in employees:
                name = person['first_name'] + person['last_name']       # making a person lookup dictionary so I can get the department name from a person name later on
                self.full_employees_dict[name] = display_name
                QTreeWidgetItem(department,[None,person['first_name'], person['last_name'], person['role']])

        self.tw.itemClicked.connect(self.handle_tree_item_clicked)


    def handle_tree_item_clicked(self, it, col):
        first_name = it.text(col+1)
        last_name = it.text(col+2)
        role = it.text(col+3)
        name = first_name + last_name
        team_name = self.full_employees_dict[name]
        self.label.setText(f"Team: {team_name} |  Name: {first_name} {last_name}  |  Role: {role} ")

        self.label.setFont(QtGui.QFont("Sanserif", 15))
        self.label.setStyleSheet('color:blue')
        self.label.setAlignment(Qt.AlignBottom)
        self.vbox.addWidget(self.label)
        self.tw.setLayout(self.vbox)

@click.command()
@click.argument('file_path')
def download(file_path):
    with open(file_path) as file:
        read_data = yaml.load(file, Loader=yaml.FullLoader)
    return read_data


def main(file_path):


    read_data = download(file_path)

    App = QApplication(sys.argv)
    test = TestApp(read_data)
    sys.exit(App.exec())


if __name__ == '__main__':
    main()