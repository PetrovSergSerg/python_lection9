from model.project import Project


def test_add_project(app, orm, data_projects):
    project = data_projects

    old_projects = orm.get_project_list()
    app.project.create(project)

    # if new list length is correct, then we can compare lists.
    # so we can get new list
    new_projects = orm.get_project_list()

    # built expected list for equalizing NEW and EXPECTED
    # expected = old_list + new_list. And sort()
    # sort() will use method __lt__, which was overridden
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
