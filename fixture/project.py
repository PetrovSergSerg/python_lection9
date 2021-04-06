from model.project import Project
from selenium.webdriver.support.ui import Select
from random import choice


class ProjectHelper:
    def __init__(self, app):
        self.app = app
        self.menu = app.menu

    def create(self, project: Project):
        wd = self.app.wd
        self.menu.manage_projects()

        button_new_project = wd.find_element_by_xpath("//input[@type='submit'][@value='Create New Project']")
        button_new_project.click()

        self.fill(project)
        button_save = wd.find_element_by_xpath("//input[@type='submit'][@value='Add Project']")
        button_save.click()

        self.menu.manage_projects()

    # TODO
    def edit(self, to: Project):
        pass

    def delete_any_project(self):
        wd = self.app.wd
        self.menu.manage_projects()

        rows = wd.find_elements_by_xpath("//table[3]//tr")
        rows.pop(0)
        rows.pop(0)
        assert len(rows) > 0

        row = choice(rows)
        link_name = row.find_element_by_xpath(".//a")
        project_id = link_name.get_attribute("href")
        project_id = project_id[project_id.find("=")+1:]
        link_name.click()

        button_delete = wd.find_element_by_xpath("//input[@type='submit'][@value='Delete Project']")
        button_delete.click()

        button_confirm = wd.find_element_by_xpath("//input[@type='submit'][@value='Delete Project']")
        button_confirm.click()

        self.menu.manage_projects()

        return project_id

    def fill(self, project: Project):
        self.type_in_field("name", project.name)
        self.select_in_field_by_name("status", project.status.description)
        self.set_checkbox("inherit", project.is_inherit)
        self.select_in_field_by_name("view_state", project.view_status.description)
        self.type_in_field("description", project.description)

    def type_in_field(self, field_name:str, value:str):
        wd = self.app.wd
        if value is not None:
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(value)

    def select_in_field_by_name(self, selector_name:str, value:str):
        wd = self.app.wd
        if value is not None:
            selector = Select(wd.find_element_by_name(selector_name))
            selector.select_by_visible_text(value)

    def set_checkbox(self, checkbox_name:str, value:bool):
        wd = self.app.wd
        checkbox = wd.find_element_by_xpath("//input[@type='checkbox']")
        checkbox.click()
