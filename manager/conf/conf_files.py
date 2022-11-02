ui_path = "C:/Users/tanku/Documents/Projects/pipeline_first/manager/ui/qt/window.ui"

project_path_pattern = 'C:/Users/tanku/Documents/mini_films'

projects = {
    "mini_film_1": "MMOVIE"
}

apps = {
    "maya": ["ma", "mb"], "houdini": ["hipnc"], "cache": ["abc", "json"]
}

assets_pattern_path = 'assets/*/{name}/{task}/{version}/{name}{state}.{ext}'
shots_pattern_path = 'shots/*/*/*/*/{name}{state}.{ext}'

lucid_patters = {
    "assets": 'assets/{cat}/{name}/{task}/{version}/{name}__{state}.{ext}',
    "shots": 'shots/{seq}/{shot}/{task}/{version}/{name}__{state}.{ext}',
    "cache": 'assets/{cat}/{name}/{task}/{version}/{name}.{ext}'
}
