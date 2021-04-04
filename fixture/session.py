class SessionHelper:
    def __init__(self, app):
        self.app = app

    def login(self, name: str, pwd: str):
        wd = self.app.wd
        self.app.open_login_page()
        wd.find_element_by_name("username").clear()
        wd.find_element_by_name("username").send_keys(name)
        wd.find_element_by_name("password").clear()
        wd.find_element_by_name("password").send_keys(pwd)
        wd.find_element_by_xpath("//input[@type='submit']").click()

    def ensure_login(self, name: str, pwd: str):
        if self.is_logged_in():
            if self.is_logged_in_as(name):
                return
            else:
                self.logout()
        self.login(name, pwd)

    def logout(self):
        wd = self.app.wd
        wd.find_element_by_link_text("Logout").click()
        wd.find_element_by_name("username")

    def ensure_logout(self):
        if self.is_logged_in():
            self.logout()

    def is_logged_in(self):
        wd = self.app.wd
        return len(wd.find_elements_by_link_text("Logout")) > 0

    def is_logged_in_as(self, name: str):
        return self.get_logged_user() == name

    def get_logged_user(self):
        wd = self.app.wd
        return wd.find_element_by_css_selector("td.login-info-left span").text

    def authenticate(self, pwd: str):
        wd = self.app.wd
        wd.find_element_by_name("password").clear()
        wd.find_element_by_name("password").send_keys(pwd)
        wd.find_element_by_xpath("//input[@type='submit']").click()
