ui_path = "C:/Users/tanku/Documents/Projects/pipeline_first/manager/ui/qt/window.ui"

project_path_pattern = 'C:/Users/tanku/Documents/mini_films'

projects = {
    "mini_film_1": "MMOVIE"
}

apps = {
    "maya": ["ma", "mb"], "houdini": ["hipnc"], "cache": ["abc"]
}

global_pattern_path = '{type}/*/*/{task}/v*/*_{state}.{ext}'
cache_pattern_path = '{type}/*/*/{task}/v*/*.{ext}'

assets_pattern_lucid = 'assets/{cat}/{name}/{task}/{version}/{name}_{state}.{ext}'
shots_pattern_lucid = 'shots/{seq}/{shot}/{name}/{version}/{name}_{state}.{ext}'
cache_pattern_lucid = 'assets/{cat}/{name}/{task}/{version}/{name}.{ext}'

