ui_path = "C:/Users/tanku/Documents/Projects/pipeline_first/manager/ui/qt/window.ui"

project_path_pattern = 'C:/Users/tanku/Documents/mini_films'

projects = {
    "mini_film_1": {
        "name": "MMOVIE",
        "coupe": 5
        }
}

hierarchy_descendant = {
    "seq": "shot",
    "shot": "task",
    "cat": "name",
    "name": "task",
    "task": "version",
    "version": "scene"
}

translate_shotgun = {
    "shot": "code",
    "seq": "code",
    "cat": "sg_asset_type",
    "name": "code",
    "task": "content"
}

translate_fs = {
    "entity.Asset.code": "name",
    "entity.Shot.code": "name",
    "entity.Asset.sg_asset_type": "cat",
    "sg_asset_type": "cat",
    "code": "name",
    "content": "task"
}


apps = {
    "maya": ["ma", "mb"], "houdini": ["hipnc"], "cache": ["abc", "json"]
}


assets_pattern_path = '{project_name}/assets/{cat}/{name}/{task}/{version}/{name_s}{state}.{ext}'
shots_pattern_path = '{project_name}/shots/{seq}/{shot}/{task}/{version}/{name_s}{state}.{ext}'

lucid_patters = {
    "assets": {
        'Ext': '{project_name}/assets/{cat}/{name}/{task}/{version}/{name}-{state}.{ext}',
        "Cache": '{project_name}/assets/{cat}/{name}/{task}/{version}/{name}.{ext}',
        'State': '{project_name}/assets/{cat}/{name}/{task}/{version}/{state}',
        'Version': '{project_name}/assets/{cat}/{name}/{task}/{version}',
        'Task': '{project_name}/assets/{cat}/{name}/{task}',
        'Name': '{project_name}/assets/{cat}/{name}',
        'Cat': '{project_name}/assets/{cat}'
    },
    "shots": {
        'Ext': '{project_name}/shots/{seq}/{shot}/{task}/{version}/{name}-{state}.{ext}',
        'State': '{project_name}/shots/{seq}/{shot}/{task}/{version}/{state}',
        'Version': '{project_name}/shots/{seq}/{shot}/{task}/{version}',
        'Task': '{project_name}/shots/{seq}/{shot}/{task}',
        'Shot': '{project_name}/shots/{seq}/{shot}',
        'Seq': '{project_name}/shots/{seq}'
    },
    "render": 'assets{cat}/{name}/{task}/{version}/render/{name}.jpg',
}

