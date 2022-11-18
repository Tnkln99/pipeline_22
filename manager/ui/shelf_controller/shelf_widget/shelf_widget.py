from PySide2 import QtCore
from PySide2.QtWidgets import QWidget, QLabel, QListWidget, QHBoxLayout, QBoxLayout, QPushButton, QListWidgetItem


class ShelfWidget(QWidget):

    def __init__(self, label, parent_layout, button_list, entities, is_active=False):
        super(ShelfWidget, self).__init__()
        self.is_active = is_active

        self.parent_layout = parent_layout

        self.layout = QHBoxLayout()
        self.layout.setDirection(QBoxLayout.TopToBottom)

        self.label = QLabel(label, self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.list = QListWidget(self)
        self.buttons = []

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.list)

        self.init_buttons(button_list)

        if self.is_active:
            parent_layout.addLayout(self.layout)
            self.build(entities)

    def init_buttons(self, button_list):
        for button_name in button_list:
            self.add_button(button_name)

    def set_active(self, state):
        if state:
            self.parent_layout.addLayout(self.layout)
            self.is_active = True
        else:
            self.layout.setParent(None)
            self.is_active = False

    def add_button(self, button_name):
        button = QPushButton(button_name, self)
        button.setObjectName(button_name)

        self.buttons.append(button)

        self.layout.addWidget(button)

    def get_label(self):
        return self.label

    def build(self, entities):
        lables = []
        for i in entities:
            if i[self.label] not in lables:
                lables.append(i[self.label])

                item = QListWidgetItem()
                item.setData(self.userRole, i[0])
                item.setText(i[self.label])
                self.list.addItem(item)

