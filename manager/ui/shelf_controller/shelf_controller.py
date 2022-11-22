from PySide2 import QtCore

from manager import conf
from manager.core.data_api import data
from manager.ui.shelf_controller.shelf_widget.shelf_widget import ShelfWidget


class ShelfController:
    def __init__(self, parent_layout, entities, type_req):
        self.type_req = type_req
        self.userRole = QtCore.Qt.UserRole
        self.parent_layout = parent_layout
        self.entities = entities
        if self.type_req == "Asset":
            self.shelves = [ShelfWidget("cat", self.parent_layout, ["add"], entities, self.userRole, True)]
        if self.type_req == "Shot":
            self.shelves = [ShelfWidget("seq", self.parent_layout, ["add"], entities, self.userRole, True)]

    def connect(self, states, extensions):
        if self.type_req == "Asset":
            self.shelves[0].list.currentItemChanged.connect(lambda: self.open_next_shelf("name", states, extensions))
        if self.type_req == "Shot":
            self.shelves[0].list.currentItemChanged.connect(lambda: self.open_next_shelf("shot", states, extensions))

    def update_entities(self, project_name, type_req, states, extensions):
        entity = {"project_name": project_name, "type_req": type_req}
        for shelf in self.shelves:
            entity.update({shelf.label.text(): shelf.list.currentItem().text()})
        # shelf is the last shelf that, for loop, got
        next_shelf_label = conf.hierarchy_descendant.get(shelf.get_label().text())

        if next_shelf_label == "scene":
            self.entities = []
            for state in states:
                for ext in extensions:
                    entity.update({"state": state, "name_s": self.content_with_label("name"), "ext": ext})
                    add_entity = data.get_entities(**entity)
                    self.entities = self.entities + add_entity
        elif next_shelf_label is not None:
            entity.update({next_shelf_label: "*"})
            self.entities = data.get_entities(**entity)
        else:
            return

    def content_with_label(self, label):
        for shelf in self.shelves:
            if shelf.label.text() == label and shelf.is_active:
                return shelf.list.currentItem().text()
        return False

    def open_next_shelf(self, label, states, extensions):
        self.close_shelves_after_label(label)
        self.update_entities("mini_film_1", self.type_req, states, extensions)
        shelf_widget = ShelfWidget(label, self.parent_layout, ["add"], self.entities, self.userRole,
                                   True)
        self.shelves.append(shelf_widget)

        shelf_label_next = conf.hierarchy_descendant.get(label)
        if shelf_label_next is not None:
            shelf_widget.list.currentItemChanged.connect(lambda: self.open_next_shelf(shelf_label_next, states,
                                                                                      extensions))

    def close_shelves_after_label(self, label):
        self.close_shelve(label)
        while conf.hierarchy_descendant.get(label) is not None:
            label = conf.hierarchy_descendant.get(label)
            self.close_shelve(label)

    def close_shelve(self, label):
        for shelf in self.shelves:
            if shelf.label.text() == label:
                self.shelves.remove(shelf)
                shelf.deleteLater()

    def refresh(self, project_name, type_req, states, extensions):
        for shelf in self.shelves:
            if shelf.label.text() == "scene":
                self.close_shelve("scene")
                self.update_entities(project_name, type_req, states, extensions)
                return
        self.connect(states, extensions)

    def restart(self, entities, type_req, states, extensions):
        self.type_req = type_req

        for shelf in self.shelves:
            shelf.deleteLater()
        self.shelves.clear()

        if self.type_req == "Asset":
            self.shelves = [ShelfWidget("cat", self.parent_layout, ["add"], entities, self.userRole, True)]
        if self.type_req == "Shot":
            self.shelves = [ShelfWidget("seq", self.parent_layout, ["add"], entities, self.userRole, True)]

        self.connect(states, extensions)

    def button_clicked(self, button_name, engine):
        for shelf in self.shelves:
            if shelf.label.text() == "scene":
                file_data = shelf.list.currentItem().data(self.userRole)

                output_function = getattr(type(engine), button_name)
                output_function(engine, file_data)

