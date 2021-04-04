from enum import Enum


class ProjectStatus(Enum):
    DEVELOPMENT = (10, 'development')
    RELEASE = (30, 'release')
    STABLE = (50, 'stable')
    OBSOLETE = (70, 'obsolete')

    def __init__(self, id: int, description: str):
        self.id = id
        self.description = description

    def get_projectstatus_by_id(id):
        for p in ProjectStatus:
            if p.id == id:
                return p
        return None

    def get_projectstatus_by_description(description):
        for p in ProjectStatus:
            if p.description == description:
                return p
        return None
