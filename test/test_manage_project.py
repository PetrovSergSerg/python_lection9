from model.project import Project


def test_add_project(app, orm, data_projects):
    project = data_projects

    old_projects = orm.get_project_list()
    app.project.create(project)

    new_projects = orm.get_project_list()

    old_projects.append(project)
    assert sorted(old_projects) == sorted(new_projects)


def test_delete_any_project(app, orm):
    if len(orm.get_project_list()) == 0:
        project = Project().set_all_fields_to_random_values()
        app.project.create(project)
    old_projects = orm.get_project_list()

    removed_project_id = app.project.delete_any_project()

    # expected list = old list without removed element
    expected_project_list = list(filter(lambda p: p.id != removed_project_id, old_projects))

    new_projects = orm.get_project_list()

    assert sorted(expected_project_list) == sorted(new_projects)


def test_edit_any_project(app, orm):
    if len(orm.get_project_list()) == 0:
        project = Project().set_all_fields_to_random_values()
        app.project.create(project)
    old_projects = orm.get_project_list()

    project_new_state = Project().set_random_values_to_random_fields()
    # TODO method edit(self, to)
    project_id = app.project.edit(project_new_state)

    edited_project = next((p for p in old_projects if p.id == project_id), None)
    index = old_projects.index(edited_project)
    project_new_state.id = project_id
    old_projects[index].update(project_new_state)

    new_projects = orm.get_project_list()

    assert sorted(old_projects) == sorted(new_projects)
