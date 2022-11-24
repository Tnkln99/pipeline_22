from shotgun_api3 import shotgun
from manager.conf.p import private_conf
from manager import conf
from pprint import pprint

sg = None


def get_shot_gun(project_name):
    global sg

    if not sg:
        sg = shotgun.Shotgun(private_conf.projects[project_name]["server"],
                             private_conf.projects[project_name]["script_name"],
                             private_conf.projects[project_name]["api_key"])
    return sg


def get_filters_asset(project_name, **kwargs):
    fields = ["code", "sg_asset_type", "tasks"]
    filters = [
        ["project", "is", {"type": "Project", "id": private_conf.projects[project_name]["id"]}]
    ]

    for key in kwargs:
        value = kwargs[key]
        fields.append(key)
        if value != "*" and key != "content":
            filters.append([key, "is", value])

    return filters, fields


def get_filters_shot(project_name, **kwargs):
    fields = ["code", "assets"]
    filters = [
        ["project", "is", {"type": "Project", "id": private_conf.projects[project_name]["id"]}]
    ]

    for key in kwargs:
        value = kwargs[key]
        fields.append(key)
        if value != "*" and key != "content":
            filters.append([key, "contains", value])

    return filters, fields


def translate_asset_sg_to_entity(list_entity_sg, project_name):
    res = []
    for entity in list_entity_sg:
        keys = []
        for key in entity.keys():
            keys.append(key)
        translated_entity = {'project_name': conf.projects[project_name]["name"]}
        for key in keys:
            if conf.translate_fs.get(key) is not None:
                translated_entity[conf.translate_fs[key]] = entity.get(key)
        res.append(translated_entity)
    return res


def translate_shot_sg_to_entity(list_entity_sg, project_name):
    res = []
    for entity in list_entity_sg:
        keys = []
        for key in entity.keys():
            keys.append(key)
        translated_entity = {'project_name': conf.projects[project_name]["name"]}
        for key in keys:
            if key == "code":
                seq = entity["code"].split("_")[0]
                shot = entity["code"].split("_")[1]
                translated_entity["seq"] = seq
                translated_entity["shot"] = shot
            elif conf.translate_fs.get(key) is not None:
                translated_entity[conf.translate_fs[key]] = entity.pop(key)
        res.append(translated_entity)
    return res


def get_entities(**kwargs):
    project_name = kwargs.get("project_name")
    type_req = kwargs.get("type_req")
    del kwargs["type_req"]
    del kwargs["project_name"]

    sg = get_shot_gun(project_name)

    keys = []
    for key in kwargs.keys():
        keys.append(key)
    for key in keys:
        if conf.translate_shotgun.get(key) is not None:
            kwargs[conf.translate_shotgun[key]] = kwargs.pop(key)

    if type_req == "Shot":
        filters = get_filters_shot(project_name, **kwargs)[0]
        fields = get_filters_shot(project_name, **kwargs)[1]
    elif type_req == "Asset":
        filters = get_filters_asset(project_name, **kwargs)[0]
        fields = get_filters_asset(project_name, **kwargs)[1]

    res = sg.find(type_req, filters, fields)

    if "content" in kwargs.keys():
        fields = ["content", "code", "name", f"entity.{type_req}.sg_asset_type", f"entity.{type_req}.code"]
        new_filter = [
            ["project", "is", {"type": "Project", "id": private_conf.projects[project_name]["id"]}]
        ]

        if kwargs.get("content") != "*":
            new_filter.append(["content", "is", kwargs.get("content")])

        ids = []

        for i in res:
            ids.append(i.get("id"))

        new_filter.append([f"entity.{type_req}.id", "in", ids])

        res = sg.find("Task", new_filter, fields)

    # re translate from shotgun language
    if type_req == "Shot":
        res = translate_shot_sg_to_entity(res, project_name)
    elif type_req == "Asset":
        res = translate_asset_sg_to_entity(res, project_name)

    return res


if __name__ == '__main__':
    pprint(get_entities(project_name='mini_film_1', type_req="Asset", cat="Prop"))
    print("---------------------------------------------------------------------------------------------")
    pprint(get_entities(project_name='mini_film_1', type_req="Asset", cat="Prop", name="nice_car_01"))
    print("---------------------------------------------------------------------------------------------")
    pprint(get_entities(project_name='mini_film_1', type_req="Asset", cat="*", name="*", task="rigging"))

    print("---------------------------------------------------------------------------------------------")
    pprint(get_entities(project_name='mini_film_1', type_req="Shot", seq="*"))
