from functools import partial

from PySide2 import QtGui
from PySide2.QtWidgets import QCheckBox, QPushButton, QTableWidgetItem, QHeaderView

import Qt
from Qt.QtWidgets import QMainWindow
from Qt import QtWidgets, QtCompat


from manager.conf import ui_path, apps
from manager.core.fm.file_search import get_all_filtered
from manager.core.resolver import get_entities, entity_to_path
from manager.engine import *
from manager.engine.base_engine import BaseEngine


class Window(QMainWindow):
    def __init__(self):
        self.engine = get()
        print(self.engine)

        self.apps_cbx = []
        self.buttons = []

        self.projects_entities = get_entities("mini_film_1")

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

        self.list_view.setRowCount(len(self.projects_entities))
        self.list_view.setColumnCount(4)

        self.load_table()

        self.list_view.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)

    def connect(self):
        self.cbx_publish.stateChanged.connect(self.refresh_filter)
        self.cbx_work.stateChanged.connect(self.refresh_filter)

        for button in self.buttons:
            button.clicked.connect(self.button_clicked)

        for cbx in self.apps_cbx:
            cbx.stateChanged.connect(self.refresh_filter)

    def refresh_filter(self):
        self.list_view.clearContents()

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

        self.projects_entities = get_entities("mini_film_1", states=states, extensions=extensions)

        self.load_table()

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

    def load_table(self):
        self.list_view.setRowCount(len(self.projects_entities))
        self.list_view.setColumnCount(3)

        for i, entity_dic in enumerate(self.projects_entities):
            self.list_view.setItem(i, 0, QTableWidgetItem(entity_dic['state']))
            self.list_view.setItem(i, 1, QTableWidgetItem(entity_dic['ext']))
            self.list_view.setItem(i, 2, QTableWidgetItem(entity_to_path("mini_film_1", entity_dic)))

    def button_clicked(self):
        file_name = self.list_widget.currentItem().text()

        output_function = getattr(BaseEngine, self.sender().objectName())
        output_function(self.engine, self.list_widget.currentItem().text())


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    w = Window()
    w.show()
    app.exec_()
