from PySide2 import QtGui
from PySide2.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView, QCheckBox

import Qt
from Qt.QtWidgets import QMainWindow
from Qt import QtWidgets, QtCompat


from manager.conf import ui_path, apps
from manager.core.fm.file_search import get_all_filtered


class Window(QMainWindow):
    def __init__(self):
        self.projects = get_all_filtered("mini_film_1")

        super(Window, self).__init__()
        QtCompat.loadUi(str(ui_path), self)

        self.apps_cbx = []
        for i in apps.keys():
            checkbox = QCheckBox(i, self)
            checkbox.setObjectName("cbx_"+i)
            self.apps_layout.addWidget(checkbox)
            self.apps_cbx.append(checkbox)

        self.cbx_publish.setChecked(True)
        self.cbx_work.setChecked(True)

        for cbx in self.apps_cbx:
            cbx.setChecked(True)
            cbx.setChecked(True)

        self.connect()

        for i in self.projects:
            self.list_widget.addItem(str(i))

    def connect(self):
        self.cbx_publish.stateChanged.connect(self.refresh_filter)
        self.cbx_work.stateChanged.connect(self.refresh_filter)

        for cbx in self.apps_cbx:
            cbx.stateChanged.connect(self.refresh_filter)

        self.btn_find.clicked.connect(self.do_find)

    def refresh_filter(self):
        self.list_widget.clear()

        states = []
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

    def do_find(self):
        print(self.list_widget.currentItem().text())


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    w = Window()
    w.show()
    app.exec_()
