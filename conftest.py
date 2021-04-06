import pytest
import json
import os.path
import importlib
import jsonpickle
import ftputil
from fixture.application import Application
from fixture.orm import ORMFixture

fixture = None
config_object = None


def load_config(file):
    global config_object
    if config_object is None:
        conf_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(conf_file_path) as config_file:
            config_object = json.load(config_file)
    return config_object


@pytest.fixture(scope="session")
def config(request):
    return load_config(request.config.getoption("--config"))


@pytest.fixture
def app(request, config):
    global fixture
    browser = request.config.getoption("--browser")
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, config=config)

    fixture.session.ensure_login(name=config["webadmin"]["login"], pwd=config["webadmin"]["password"])

    return fixture


@pytest.fixture(scope="session")
def orm(request):
    db_config = load_config(request.config.getoption("--config"))["db"]

    dbfixture = ORMFixture(host=db_config["host"],
                           name=db_config["name"],
                           user=db_config["user"],
                           password=db_config["password"])

    return dbfixture


# @pytest.fixture(scope="session", autouse=True)
def ftp(request, config):
    install_server_configuration(config['ftp']['host'], config['ftp']['user'], config['ftp']['password'])

    def finalizer():
        restore_server_configuration(config['ftp']['host'], config['ftp']['user'], config['ftp']['password'])

    request.addfinalizer(finalizer)


def install_server_configuration(host, user, password):
    with ftputil.FTPHost(host, user, password) as remote:
        if remote.path.isfile("config_inc.php.back"):
            remote.remove("config_inc.php.back")

        if remote.path.isfile("config_inc.php"):
            remote.rename("config_inc.php", "config_inc.php.back")

        remote.upload(os.path.join(os.path.dirname(__file__), "resources/config_inc.php"), "config_inc.php")


def restore_server_configuration(host, user, password):
    with ftputil.FTPHost(host, user, password) as remote:
        if remote.path.isfile("config_inc.php.back"):
            if remote.path.isfile("config_inc.php"):
                remote.remove("config_inc.php")
            remote.rename("config_inc.php.back", "config_inc.php")


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    global fixture

    def finalizer():
        fixture.session.ensure_logout()
        fixture.destroy()

    request.addfinalizer(finalizer)


@pytest.fixture()
def check_ui(request):
    return request.config.getoption("--check_ui")


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--config", action="store", default="config.json")
    parser.addoption("--check_ui", action="store")


def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            testdata = load_from_module(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[repr(p) for p in testdata])
        elif fixture.startswith("json_"):
            testdata = load_from_json(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids=[repr(g) for g in testdata])


def load_from_module(module):
    obj = importlib.import_module(f'data.{module}')
    return obj.testdata


def load_from_json(jsonfile):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f'data/{jsonfile}.json')) as file:
        return jsonpickle.decode(file.read())
