import model.utils as utils
from random import randint, getrandbits, choice
import data.constants as c
from model.project_status import ProjectStatus
from model.view_status import ViewStatus


class Project:
    def __init__(self, id=None, name=None, status=None,
                 is_inherit=None, view_status=None, description=None,
                 enabled=None):
        self.id = id
        self.name = name if name is not None else "name" + utils.get_random_word(c.SYMBOLS, randint(3, 10))
        self.status = status
        self.is_inherit = is_inherit
        self.view_status = view_status
        self.description = description
        self.enabled = True if enabled is None else enabled

    def set_all_fields_to_random_values(self):
        self.name = "name" + utils.get_random_word(c.SYMBOLS, randint(3, 10))
        self.status = choice(list(ProjectStatus))
        self.is_inherit = bool(getrandbits(1))
        self.view_status = choice(list(ViewStatus))
        self.description = utils.get_random_word(c.SYMBOLS, randint(3, 50))
        self.enabled = bool(getrandbits(1))
        return self

    def set_random_values_to_random_fields(self):
        if bool(getrandbits(1)):
            self.name = "name" + utils.get_random_word(c.SYMBOLS, randint(3, 10))
        if bool(getrandbits(1)):
            self.status = choice(list(ProjectStatus))
        if bool(getrandbits(1)):
            self.is_inherit = bool(getrandbits(1))
        if bool(getrandbits(1)):
            self.view_status = choice(list(ViewStatus))
        if bool(getrandbits(1)):
            self.description = utils.get_random_word(c.SYMBOLS, randint(3, 50))
        if bool(getrandbits(1)):
            self.enabled = bool(getrandbits(1))
        return self

    def update(self, to):
        if to.name is not None:
            self.name = to.name
        if to.status is not None:
            self.status = to.status
        if to.is_inherit is not None:
            self.is_inherit = to.is_inherit
        if to.view_status is not None:
            self.view_status = to.view_status
        if to.description is not None:
            self.description = to.description
        if to.enabled is not None:
            self.enabled = to.enabled

    def __eq__(self, other):
        return (self.id is None
                or other.id is None
                or self.id == other.id) \
               and self.name == other.name
               # and utils.remove_spaces(self.name) == utils.remove_spaces(other.name)

    def __lt__(self, other):
        # None >> any integer
        # self.id = None => return False (left bigger)
        # other.id is None => return True (right is bigger)
        # else compare int(self.id) <> int(other.id), because type(Group.id) = str, but it's a number!
        return self.id is not None \
               and (other.id is None
                    or int(self.id) < int(other.id))

    def __repr__(self):
        return f'Project({"id=" + self.id + ", " if self.id is not None else ""}' \
               f'name="{self.name}", status="{self.status.description}", view_status="{self.view_status.description}")'
