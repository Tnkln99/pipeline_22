from shotgun_api3 import shotgun
from manager import conf
from pprint import pprint

sg = None


def get_shot_gun(project_name):
    global sg

    if not sg:
        sg = shotgun.Shotgun(conf.projects[project_name]["server"],
                             conf.projects[project_name]["script_name"],
                             conf.projects[project_name]["api_key"])
    return sg



def get_from_shotgun(**kwargs):
    project_name = kwargs.get("project_name")
    type_req = kwargs.get("type_req")
    del kwargs["type_req"]
    del kwargs["project_name"]

    sg = get_shot_gun(project_name)

    fields = []
    filters = [
        ["project", "is", {"type": "Project", "id": conf.projects[project_name]["id"]}],
    ]

    for key in kwargs:
        value = kwargs[key]
        fields.append(key)
        if value != "*" and key != "content":
            filters.append([key, "is", value])

    assets = sg.find(type_req, filters, fields)

    if "content" in kwargs.keys():
        fields = ["content", "code"]
        new_filter = [
            ["project", "is", {"type": "Project", "id": conf.projects[project_name]["id"]}],
            ["content", "is", kwargs.get("content")]
        ]
        for i in assets:
            pprint(i)
            new_filter.append(
                ["entity.Asset.id", "is", i.get('id')]
            )

        assets = sg.find("Task", new_filter, fields)

    return assets


if __name__ == '__main__':
    # sg_asset_type = cat / code = name
    pprint(get_from_shotgun(project_name="mini_film_1", type_req="Asset", sg_asset_type="*", code="sword_01",
                            content="Cloth"))
