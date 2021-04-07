from pony.orm import *
from model.project import Project
from model.project_status import ProjectStatus as ps
from model.view_status import ViewStatus as view


class ORMFixture:
    db = Database()

    class ORMProject(db.Entity):
        _table_ = 'mantis_project_table'
        id = PrimaryKey(int, column='id')
        name = Required(str, column='name')
        status = Optional(int, column='status')
        enabled = Optional(int, column='enabled')
        view_state = Optional(int, column='view_state')
        access_min = Optional(int, column='access_min')
        file_path = Optional(str, column='file_path')
        description = Optional(str, column='description')
        category_id = Optional(int, column='category_id')
        inherit_global = Optional(int, column='inherit_global')

    def __init__(self, host, name, user, password):
        self.db.bind('mysql', host=host, database=name, user=user, password=password)
        self.db.generate_mapping()
        sql_debug(True)

    def convert_project_to_model(self, projects):
        def convert(p: ORMFixture.ORMProject):
            return Project(id=str(p.id), name=p.name, status=ps.get_projectstatus_by_id(p.status),
                           view_status=view.get_viewstatus_by_id(p.view_state), description=p.description)
        return list(map(convert, projects))

    @db_session
    def get_project_list(self):
        return self.convert_project_to_model(select(p for p in ORMFixture.ORMProject))
