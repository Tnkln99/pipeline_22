from PySide2 import QtCore
from PySide2.QtWidgets import QCheckBox, QPushButton, QListWidget, QListWidgetItem

import Qt
from Qt.QtWidgets import QMainWindow
from Qt import QtWidgets, QtCompat

from manager.conf import ui_path, apps, projects
from manager.core.data_api.data import get_entities
from manager.core.fm.file_search import entity_to_path
from manager.engine import *
from manager.engine.base_engine import BaseEngine
from pprint import pprint


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

        self.list_A = QListWidget()
        self.list_B = QListWidget()
        self.list_C = QListWidget()
        self.list_D = QListWidget()
        self.list_E = QListWidget()

        self.utility_layout.addWidget(self.list_A)

        self.cbx_work.setChecked(True)

        for cbx in self.apps_cbx:
            cbx.setChecked(True)

        self.connect()

        self.cbx_publish.setChecked(True)

        self.project_name = self.combo_box_projects.currentText()
        self.pattern_name = self.combo_box_pattern.currentText()

        self.projects_entities = []

        self.build_a()

    def connect(self):
        self.cbx_publish.stateChanged.connect(self.refresh_filter)
        self.cbx_work.stateChanged.connect(self.refresh_filter)

        # filter change will trigger the construction of list A
        # other lists contents will get deleted to restart exploration
        self.combo_box_pattern.currentTextChanged.connect(self.build_a)

        # changes in A will trigger B -> C -> D -> E
        self.list_A.currentItemChanged.connect(self.build_b)
        self.list_B.currentItemChanged.connect(self.build_c)
        self.list_C.currentItemChanged.connect(self.build_d)
        self.list_D.currentItemChanged.connect(self.build_e)

        for cbx in self.apps_cbx:
            cbx.stateChanged.connect(self.refresh_filter)

        for button in self.buttons:
            button.clicked.connect(self.button_clicked)

    # changing the global filters (states and used applications)
    # At the end we are building the  A list to start selection of the user
    # If user changes the global filter we clear all and restart the process with building only the list A again.
    def refresh_filter(self):
        self.project_name = self.combo_box_projects.currentText()
        self.pattern_name = self.combo_box_pattern.currentText()

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

        self.list_B.setParent(None)
        self.list_C.setParent(None)
        self.list_D.setParent(None)
        self.list_E.setParent(None)

    def load_combo_boxs(self):
        for project in projects.keys():
            self.combo_box_projects.addItem(project)

        self.combo_box_pattern.addItem("assets")
        self.combo_box_pattern.addItem("shots")

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

    def build_a(self):
        self.list_A.clear()
        self.projects_entities = []
        self.project_name = self.combo_box_projects.currentText()
        self.pattern_name = self.combo_box_pattern.currentText()

        if self.pattern_name == "assets":
            self.projects_entities = get_entities(project_name=self.project_name, cat="*")

            names = []
            for i in self.projects_entities:
                if i[0]['cat'] not in names:
                    names.append(i[0]['cat'])
            for i in names:
                self.list_A.addItem(i)

        if self.pattern_name == "shots":
            self.projects_entities = get_entities(project_name=self.project_name, seq="*")
            seq_l = []
            for i in self.projects_entities:
                if i[0]['seq'] not in seq_l:
                    seq_l.append(i[0]['seq'])
            for i in seq_l:
                self.list_A.addItem(i)

    def build_b(self):
        self.list_B.clear()
        self.list_C.setParent(None)
        self.list_D.setParent(None)
        self.list_E.setParent(None)
        self.projects_entities = []

        if self.list_A.currentItem() is None:
            return

        self.utility_layout.addWidget(self.list_B)

        content_list_a = self.list_A.currentItem().text()
        if self.pattern_name == "assets":
            self.projects_entities = get_entities(project_name=self.project_name, cat=content_list_a, name="*")

            names = []
            for i in self.projects_entities:
                if i[0]['name'] not in names:
                    names.append(i[0]['name'])
            for i in names:
                self.list_B.addItem(i)

        if self.pattern_name == "shots":
            self.projects_entities = get_entities(project_name=self.project_name, seq=content_list_a, shot="*")
            shots = []
            for i in self.projects_entities:
                if i[0]['shot'] not in shots:
                    shots.append(i[0]['shot'])
            for i in shots:
                self.list_B.addItem(i)

    def build_c(self):
        self.list_C.clear()
        self.list_D.setParent(None)
        self.list_E.setParent(None)
        self.projects_entities = []

        if self.list_A.currentItem() is None or self.list_B.currentItem() is None:
            return

        self.utility_layout.addWidget(self.list_C)

        content_list_a = self.list_A.currentItem().text()
        content_list_b = self.list_B.currentItem().text()

        if self.pattern_name == "assets":
            self.projects_entities = get_entities(project_name=self.project_name, cat=content_list_a,
                                                  name=content_list_b, task="*")
        if self.pattern_name == "shots":
            self.projects_entities = get_entities(project_name=self.project_name, seq=content_list_a,
                                                  shot=content_list_b, task="*")

        tasks = []
        for i in self.projects_entities:
            if i[0]['task'] not in tasks:
                tasks.append(i[0]['task'])
        for i in tasks:
            self.list_C.addItem(i)

    def build_d(self):
        self.list_D.clear()
        self.list_E.setParent(None)
        if self.list_A.currentItem() is None or self.list_B.currentItem() is None or self.list_C.currentItem() is None:
            return

        self.utility_layout.addWidget(self.list_D)

        self.projects_entities.clear()

        content_list_a = self.list_A.currentItem().text()
        content_list_b = self.list_B.currentItem().text()
        content_list_c = self.list_C.currentItem().text()

        if self.pattern_name == "assets":
            self.projects_entities = get_entities(project_name=self.project_name, cat=content_list_a,
                                                  name=content_list_b,
                                                  task=content_list_c, version="*")

        if self.pattern_name == "shots":
            self.projects_entities = get_entities(project_name=self.project_name, seq=content_list_a,
                                                  shot=content_list_b,
                                                  task=content_list_c, version="*")
        versions = []
        for i in self.projects_entities:
            version = i[0]['version']
            if version not in versions:
                versions.append(version)
        for i in versions:
            self.list_D.addItem(i)

    def build_e(self):
        self.list_E.clear()
        self.projects_entities = []

        if self.list_A.currentItem() is None or self.list_B.currentItem() is None or self.list_C.currentItem() is None \
                or self.list_D.currentItem() is None:
            return

        self.utility_layout.addWidget(self.list_E)

        content_list_a = self.list_A.currentItem().text()
        content_list_b = self.list_B.currentItem().text()
        content_list_c = self.list_C.currentItem().text()
        content_list_d = self.list_D.currentItem().text()

        if self.pattern_name == "assets":
            for state in self.states:
                for ext in self.extensions:
                    self.projects_entities = self.projects_entities + get_entities(project_name=self.project_name,
                                                                                   cat=content_list_a,
                                                                                   name=content_list_b,
                                                                                   task=content_list_c,
                                                                                   version=content_list_d, state=state,
                                                                                   name_s=content_list_b,
                                                                                   ext=ext)
        if self.pattern_name == "shots":
            for state in self.states:
                for ext in self.extensions:
                    self.projects_entities = self.projects_entities + get_entities(project_name=self.project_name,
                                                                                   seq=content_list_a,
                                                                                   shot=content_list_b,
                                                                                   task=content_list_c,
                                                                                   version=content_list_d,
                                                                                   name_s="movie",
                                                                                   state=state,
                                                                                   ext=ext)
        pprint(self.projects_entities)
        scenes = []
        item = QListWidgetItem()
        for i in self.projects_entities:
            item.setData(self.userRole, i[0])
            scene_name = f"{i[0].get('state') or '__'}/{i[0]['name']}/.{i[0]['ext']}"
            if scene_name not in scenes:
                scenes.append(scene_name)
        for i in scenes:
            item.setText(i)
            self.list_E.addItem(item)

    def button_clicked(self):
        if self.list_E.currentItem() is None:
            return
        file_name = entity_to_path(self.project_name, self.list_E.currentItem().data(self.userRole))

        output_function = getattr(BaseEngine, self.sender().objectName())
        output_function(self.engine, file_name)


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    w = Window()
    w.show()
    app.exec_()
