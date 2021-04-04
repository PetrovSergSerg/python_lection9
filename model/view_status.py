from enum import Enum


class ViewStatus(Enum):
    PUBLIC = (10, 'public')
    PRIVATE = (50, 'private')

    def __init__(self, id: int, description: str):
        self.id = id
        self.description = description

    def get_viewstatus_by_id(id):
        for p in ViewStatus:
            if p.id == id:
                return p
        return None

    def get_viewstatus_by_description(description):
        for p in ViewStatus:
            if p.description == description:
                return p
        return None
