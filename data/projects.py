from model.project import Project
from model.project_status import ProjectStatus as ps
from model.view_status import ViewStatus as vs
from model.utils import random_string, get_random_word, randint
import data.constants as c

testdata = [
    Project(name="name" + get_random_word(c.SYMBOLS, randint(1, 10)),
            status=status,
            is_inherit=is_inherit,
            view_status=view_status,
            description="" if description else random_string("description", 50)
            )
    for description in [True, False]
    for status in list(ps)
    for is_inherit in [True, False]
    for view_status in list(vs)
]
