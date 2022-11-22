from PySide2 import QtCore
from PySide2.QtWidgets import QCheckBox, QPushButton

import Qt
from Qt.QtWidgets import QMainWindow
from Qt import QtWidgets, QtCompat

from manager.conf import ui_path, apps, projects
from manager.core.data_api.data import get_entities
from manager.engine import *
from manager.ui.shelf_controller.shelf_controller import ShelfController


class Window(QMainWindow):
    def __init__(self):
        self.engine = get()
        print(self.engine)

        # this lists will contain the filter parameters
        self.extensions = []
        self.states = []

        self.userRole = QtCore.Qt.UserRole

        super(Window, self).__init__()
        QtCompat.loadUi(str(ui_path), self)

        self.apps_cbx = []
        self.buttons = []

        self.load_buttons()
        self.load_check_boxs()
        self.load_combo_boxs()

        self.project_name = self.combo_box_projects.currentText()
        self.pattern_name = self.combo_box_pattern.currentText()

        self.projects_entities = []
        self.shelves = None

        self.init_shelves()

        self.cbx_work.setChecked(True)

        for cbx in self.apps_cbx:
            cbx.setChecked(True)

        self.connect()

        self.cbx_publish.setChecked(True)

    def connect(self):
        self.combo_box_projects.currentIndexChanged.connect(self.init_shelves)
        self.combo_box_pattern.currentIndexChanged.connect(self.init_shelves)

        self.cbx_publish.stateChanged.connect(self.refresh_filter)
        self.cbx_work.stateChanged.connect(self.refresh_filter)

        for cbx in self.apps_cbx:
            cbx.stateChanged.connect(self.refresh_filter)

        for button in self.buttons:
            button.clicked.connect(self.button_clicked)

        self.shelves.connect(self.states, self.extensions)

    def refresh_filter(self):
        self.states.clear()
        self.extensions.clear()

        for cbx in self.apps_cbx:
            if cbx.objectName() == "cbx_houdini" and cbx.isChecked():
                self.extensions.extend(apps["houdini"])
            if cbx.objectName() == "cbx_maya" and cbx.isChecked():
                self.extensions.extend(apps["maya"])
            if cbx.objectName() == "cbx_cache" and cbx.isChecked():
                self.extensions.extend(apps["cache"])
                # to find caches we need an empty state because cache don't have a state
                self.states.append("")

        if self.cbx_publish.isChecked():
            self.states.append("-publish")
        if self.cbx_work.isChecked():
            self.states.append("-work")

        self.shelves.refresh(self.project_name, self.pattern_name, self.states, self.extensions)

    def load_combo_boxs(self):
        for project in projects.keys():
            self.combo_box_projects.addItem(project)

        self.combo_box_pattern.addItem("Asset")
        self.combo_box_pattern.addItem("Shot")

    def load_buttons(self):
        for i in self.engine.implementations:
            button = QPushButton(i, self)
            button.setObjectName(i)
            self.button_layout.addWidget(button)
            self.buttons.append(button)

    def load_check_boxs(self):
        for i in apps.keys():
            checkbox = QCheckBox(i, self)
            checkbox.setObjectName("cbx_" + i)
            self.apps_layout.addWidget(checkbox)
            self.apps_cbx.append(checkbox)

    def init_shelves(self):
        self.project_name = self.combo_box_projects.currentText()
        self.pattern_name = self.combo_box_pattern.currentText()

        if self.pattern_name == "Asset":
            entities_start = get_entities(project_name=self.project_name, type_req=self.pattern_name, cat="*")
        elif self.pattern_name == "Shot":
            entities_start = get_entities(project_name=self.project_name, type_req=self.pattern_name, seq="*")

        if self.shelves is None:
            self.shelves = ShelfController(self.utility_layout, entities_start, self.pattern_name)
        else:
            self.shelves.restart(entities_start, self.pattern_name, self.states, self.extensions)

    def button_clicked(self):
        self.shelves.button_clicked(self.sender().objectName(), self.engine)


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    w = Window()
    w.show()
    app.exec_()
