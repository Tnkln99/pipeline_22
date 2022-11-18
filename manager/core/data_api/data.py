from manager.core.fm import file_search
from manager.core.sg_api import connect_sg
from pprint import pprint
from manager import conf


def get_entities(**kwargs):
    # cat = * name = sword
    coupe = conf.projects.get(kwargs.get("project_name")).get("coupe")
    if len(kwargs.keys()) > coupe:
        return file_search.get_entities(**kwargs)
    elif len(kwargs.keys()) <= coupe:
        return connect_sg.get_entities(**kwargs)


if __name__ == '__main__':
    pprint(get_entities(project_name='mini_film_1', type_req="Shot", seq="sq010", shot="sh010"))

