from functools import partial

from manager import conf
from manager.core.data_api import data
from manager.ui.shelf_controller.shelf_widget.shelf_widget import ShelfWidget


class ShelfController:
    def __init__(self, parent_layout, entities):
        self.parent_layout = parent_layout
        self.entities = entities
        self.shelves = [ShelfWidget("cat", self.parent_layout, ["add"], entities, True)]

    def connect(self):
        # todo: get this parameters from init
        self.update_entities("mini_film_01", "Asset")
        for shelf in self.shelves:
            # getting the next shelf label that we want to create from conf.
            shelf_label = conf.hierarchy_descendant_asset(shelf.get_label())
            shelf.currentItemChanged.connect(partial(self.get_shelve_with_label, shelf_label, self.entities))

    # todo: big chance of bug in here
    def update_entities(self, project_name, type_req):
        entity = {"project_name": project_name, "type_req": type_req}
        for shelf in self.shelves:
            entity.update({shelf.label: shelf.list.currentItem})
        # shelf is the last shelf that for loop got
        entity.update({conf.hierarchy_descendant_asset(shelf.get_label()): "*"})
        self.entities = data.get_entities(**entity)

    # if shelf with given name exists it sets it to active if it doesn't exist it creates it and put it next
    # to other shelves
    def get_shelve_with_label(self, label, entities):
        self.shelves.append(ShelfWidget(label, self.parent_layout, ["add"], entities, True))
