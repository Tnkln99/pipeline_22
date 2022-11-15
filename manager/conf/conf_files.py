ui_path = "C:/Users/tanku/Documents/Projects/pipeline_first/manager/ui/qt/window.ui"

project_path_pattern = 'C:/Users/tanku/Documents/mini_films'

projects = {
    "mini_film_1": {
        "name": "MMOVIE",
        "server": "https://artfx.shotgunstudio.com",
        "script_name": "test_td",
        "api_key": "uqtcaegzgsqzDf6ttkz%lkgfw",
        "id": 1095,
        "index_data_file": 3
        }
}

conf_server_data = {"shotgun": ["cat", "name", "task"]}

translate_shotgun = {
    "cat": "sg_asset_type",
    "name": "code",
    "task": "content"
}

apps = {
    "maya": ["ma", "mb"], "houdini": ["hipnc"], "cache": ["abc", "json"]
}


assets_pattern_path = 'assets/{cat}/{name}/{task}/{version}/{name_s}{state}.{ext}'
shots_pattern_path = 'shots/{seq}/{shot}/{task}/{version}/{name_s}{state}.{ext}'

lucid_patters = {
    "assets": {
        'Ext': 'assets/{cat}/{name}/{task}/{version}/{name}-{state}.{ext}',
        "Cache": 'assets/{cat}/{name}/{task}/{version}/{name}.{ext}',
        'State': 'assets/{cat}/{name}/{task}/{version}/{state}',
        'Version': 'assets/{cat}/{name}/{task}/{version}',
        'Task': 'assets/{cat}/{name}/{task}',
        'Name': 'assets/{cat}/{name}',
        'Cat': 'assets/{cat}'
    },
    "shots": {
        'Ext': 'shots/{seq}/{shot}/{task}/{version}/{name}-{state}.{ext}',
        'State': 'shots/{seq}/{shot}/{task}/{version}/{state}',
        'Version': 'shots/{seq}/{shot}/{task}/{version}',
        'Task': 'shots/{seq}/{shot}/{task}',
        'Shot': 'shots/{seq}/{shot}',
        'Seq': 'shots/{seq}'
    },
    "render": 'assets{cat}/{name}/{task}/{version}/render/{name}.jpg',
}

