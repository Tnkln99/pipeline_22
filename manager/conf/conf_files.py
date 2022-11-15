ui_path = "C:/Users/tanku/Documents/Projects/pipeline_first/manager/ui/qt/window.ui"

project_path_pattern = 'C:/Users/tanku/Documents/mini_films'

projects = {
    "mini_film_1": "MMOVIE"
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

