from selenium import webdriver
from fixture.session import SessionHelper
from fixture.project import ProjectHelper
from fixture.menu import MenuHelper


class Application:
    def __init__(self, browser, config):
        if browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "chrome":
            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            self.wd = webdriver.Chrome(options=options)  # 'C:\\Tools\\chromedriver.exe')
        elif browser == "ie":
            self.wd = webdriver.Ie()
        else:
            raise ValueError(f'Unrecognized browser {browser}\nBrowser should be [firefox|chrome|edge]')
        self.wd.implicitly_wait(0.1)
        self.session = SessionHelper(self)
        self.menu = MenuHelper(self)
        self.config = config
        self.base_url = config["web"]["baseUrl"]
        self.project = ProjectHelper(self)

    def is_valid(self):
        try:
            self.wd.current_url
            return True
        except:
            return False

    def open_login_page(self):
        wd = self.wd
        wd.get(self.base_url)

    def destroy(self):
        self.wd.quit()
