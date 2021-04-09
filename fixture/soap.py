from zeep import Client
from model.project import Project
from model.project_status import ProjectStatus as ps
from model.view_status import ViewStatus as view


class SoapHelper:
    def __init__(self, app):
        self.app = app
        self.config = app.config

    def get_project_list_for_user(self, username, password):
        client = Client(self.config['soap']['wsdl'])

        def convert(p):
            return Project(id=str(p.id), name=p.name, status=ps.get_projectstatus_by_id(p.status.id),
                           view_status=view.get_viewstatus_by_id(p.view_state.id),
                           description="" if p.description is None else p.description)

        project_data_array = client.service.mc_projects_get_user_accessible(username=username, password=password)
        project_list = list(map(convert, project_data_array))
        return project_list

