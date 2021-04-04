from pony.orm import *
from datetime import datetime
from model.project import Project
from model.project_status import ProjectStatus as ps
from model.view_status import ViewStatus as view

from random import shuffle


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
                           enabled=p.enabled, view_status=view.get_viewstatus_by_id(p.view_state),
                           is_inherit=False if p.inherit_global < 1 else True,
                           description=p.description)
        return list(map(convert, projects))
    #
    # def convert_contacts_to_model(self, contacts):
    #     def convert(c: Contact):
    #         return Contact(id=str(c.id), firstname=c.firstname, lastname=c.lastname, address=c.address,
    #                        email_main=c.email_main, email_secondary=c.email_secondary, email_other=c.email_other,
    #                        phone_work=c.phone_work, phone_home=c.phone_home, phone_secondary=c.phone_secondary,
    #                        mobile=c.mobile
    #                        )
    #     return list(map(convert, contacts))

    @db_session
    def get_project_list(self):
        return self.convert_project_to_model(select(p for p in ORMFixture.ORMProject))

    # @db_session
    # def get_contact_list(self):
    #     return self.convert_contacts_to_model(select(c for c in ORMFixture.ORMContact if c.deprecated is None))
    #
    # @db_session
    # def get_contacts_in_group(self, group):
    #     orm_group = list(select(g for g in ORMFixture.ORMGroup if g.id == group.id))[0]
    #     return self.convert_contacts_to_model(orm_group.contacts)
    #
    # @db_session
    # def get_contacts_not_in_group(self, group):
    #     orm_group = list(select(g for g in ORMFixture.ORMGroup if g.id == group.id))[0]
    #     orm_contacts = select(c for c in ORMFixture.ORMContact
    #                                if c.deprecated is None and
    #                                orm_group not in c.groups)
    #     return self.convert_contacts_to_model(orm_contacts)

    # def get_random_group_and_contacts_not_in_bind(self):
    #     group = Group()
    #     contact_list = []
    #     group_list = self.get_group_list()
    #     shuffle(group_list)
    #
    #     for g in group_list:
    #         contact_list = self.get_contacts_not_in_group(g)
    #         if len(contact_list) > 0:
    #             group = g
    #             break
    #
    #     return group, contact_list
    #
    # def get_random_group_and_contacts_in_bind(self):
    #     group = Group()
    #     contact_list = []
    #     group_list = self.get_group_list()
    #     shuffle(group_list)
    #
    #     for g in group_list:
    #         contact_list = self.get_contacts_in_group(g)
    #         if len(contact_list) > 0:
    #             group = g
    #             break
    #
    #     return group, contact_list