from functools import partial

from PySide2 import QtGui
from PySide2.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView, QCheckBox, QPushButton, QTableWidgetItem

import Qt
from Qt.QtWidgets import QMainWindow
from Qt import QtWidgets, QtCompat


from manager.conf import ui_path, apps
from manager.core.fm.file_search import get_all_filtered
from manager.engine import *
from manager.engine.base_engine import BaseEngine


class Window(QMainWindow):
    def __init__(self):
        self.engine = get()
        print(self.engine)

        self.apps_cbx = []
        self.buttons = []

        self.projects = get_all_filtered("mini_film_1")

        super(Window, self).__init__()
        QtCompat.loadUi(str(ui_path), self)

        self.load_buttons()
        self.load_check_boxs()

        self.cbx_publish.setChecked(True)
        self.cbx_work.setChecked(True)

        for cbx in self.apps_cbx:
            cbx.setChecked(True)
            cbx.setChecked(True)

        self.connect()

        cpt = 0
        for i in self.projects:
            self.list_view.insertRow(cpt)
            self.list_view.setItem(0, cpt, QTableWidgetItem(str(i)))
            cpt = cpt + 1

    def connect(self):
        self.cbx_publish.stateChanged.connect(self.refresh_filter)
        self.cbx_work.stateChanged.connect(self.refresh_filter)

        for button in self.buttons:
            button.clicked.connect(self.button_clicked)

        for cbx in self.apps_cbx:
            cbx.stateChanged.connect(self.refresh_filter)

    def refresh_filter(self):
        self.list_widget.clear()

        states = [""]
        extensions = []

        if self.cbx_publish.isChecked():
            states.append("publish")
        if self.cbx_work.isChecked():
            states.append("work")

        for cbx in self.apps_cbx:
            if cbx.objectName() == "cbx_houdini" and cbx.isChecked():
                extensions.extend(apps["houdini"])
            if cbx.objectName() == "cbx_maya" and cbx.isChecked():
                extensions.extend(apps["maya"])
            if cbx.objectName() == "cbx_cache" and cbx.isChecked():
                extensions.extend(apps["cache"])

        self.projects = get_all_filtered("mini_film_1", states=states, extensions=extensions)

        for i in self.projects:
            self.list_widget.addItem(str(i))

    def load_buttons(self):
        for i in self.engine.implementations:
            button = QPushButton(i, self)
            button.setObjectName(i)
            self.button_layout.addWidget(button)
            self.buttons.append(button)

    def load_check_boxs(self):
        for i in apps.keys():
            checkbox = QCheckBox(i, self)
            checkbox.setObjectName("cbx_"+i)
            self.apps_layout.addWidget(checkbox)
            self.apps_cbx.append(checkbox)

    def button_clicked(self):
        file_name = self.list_widget.currentItem().text()

        output_function = getattr(BaseEngine, self.sender().objectName())
        output_function(self.engine, self.list_widget.currentItem().text())


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    w = Window()
    w.show()
    app.exec_()
