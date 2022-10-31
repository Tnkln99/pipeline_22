from PySide2.QtWidgets import QCheckBox, QPushButton, QListWidget

import Qt
from Qt.QtWidgets import QMainWindow
from Qt import QtWidgets, QtCompat


from manager.conf import ui_path, apps, projects
from manager.core.resolver import get_entities, entity_to_path
from manager.engine import *
from manager.engine.base_engine import BaseEngine


class Window(QMainWindow):
    def __init__(self):
        self.engine = get()
        print(self.engine)

        self.apps_cbx = []
        self.buttons = []

        super(Window, self).__init__()
        QtCompat.loadUi(str(ui_path), self)

        self.load_buttons()
        self.load_check_boxs()
        self.load_combo_boxs()

        self.project_name = self.combo_box_projects.currentText()
        self.pattern_name = self.combo_box_pattern.currentText()
        self.projects_entities = get_entities(self.project_name)

        self.cbx_publish.setChecked(True)
        self.cbx_work.setChecked(True)

        for cbx in self.apps_cbx:
            cbx.setChecked(True)

        self.list_A = QListWidget()
        self.utility_layout.addWidget(self.list_A)

        self.list_B = QListWidget()
        self.utility_layout.addWidget(self.list_B)

        self.list_C = QListWidget()
        self.utility_layout.addWidget(self.list_C)

        self.list_D = QListWidget()
        self.utility_layout.addWidget(self.list_D)

        self.connect()

        self.refresh_list()

    def connect(self):
        self.cbx_publish.stateChanged.connect(self.refresh_filter)
        self.cbx_work.stateChanged.connect(self.refresh_filter)
        self.combo_box_pattern.currentTextChanged.connect(self.refresh_filter)

        for cbx in self.apps_cbx:
            cbx.stateChanged.connect(self.refresh_filter)

        for button in self.buttons:
            button.clicked.connect(self.button_clicked)

    def refresh_filter(self):
        self.project_name = self.combo_box_projects.currentText()
        self.pattern_name = self.combo_box_pattern.currentText()

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

        self.projects_entities = get_entities(self.project_name, states=states, extensions=extensions)

        self.refresh_list()

    def load_combo_boxs(self):
        for project in projects.keys():
            self.combo_box_projects.addItem(project)

        self.combo_box_pattern.addItem("shots")
        self.combo_box_pattern.addItem("assets")

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

    def refresh_list(self):
        self.list_A.clear()
        self.list_B.clear()
        self.list_C.clear()
        self.list_D.clear()

        if self.pattern_name == "assets":
            res_ext = []
            res_name = []
            res_version = []
            res_scene = []
            for i in self.projects_entities:
                if i[1].name == 'assets' or i[1].name == 'cache':
                    res_ext.append(i[0]['ext'])
                    res_name.append(i[0]['name'])
                    res_version.append(i[0]['version'])
                    res_scene.append(entity_to_path(self.project_name, i[0]))

            self.fill_list(res_name, res_ext, res_version, res_scene)

        elif self.pattern_name == "shots":
            res_seq = []
            res_shot = []
            res_name = []
            res_scene = []
            for i in self.projects_entities:
                if i[1].name == 'shots':
                    res_seq.append(i[0]['seq'])
                    res_shot.append(i[0]['shot'])
                    res_name.append(i[0]['version'])
                    res_scene.append(entity_to_path(self.project_name, i[0]))

            self.fill_list(res_seq, res_shot, res_name, res_scene)

    def fill_list(self, la, lb, lc, ld):
        for i in la:
            self.list_A.addItem(i)

        for i in lb:
            self.list_B.addItem(i)

        for i in lc:
            self.list_C.addItem(i)

        for i in ld:
            self.list_D.addItem(str(i))

    def button_clicked(self):
        file_name = self.list_widget.currentItem().text()

        output_function = getattr(BaseEngine, self.sender().objectName())
        output_function(self.engine, self.list_widget.currentItem().text())


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    w = Window()
    w.show()
    app.exec_()
