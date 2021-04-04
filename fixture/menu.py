class MenuHelper:
    def __init__(self, app):
        self.app = app

    def __manage(self):
        wd = self.app.wd
        manage_list_pages = ['manage_user_page.php',
                             'manage_proj_page.php',
                             'manage_tags_page.php',
                             'manage_custom_field_page.php'
                             'manage_prof_menu_page.php'
                             'manage_plugin_page.php'
                             'adm_config_report.php']

        if wd.current_url[wd.current_url.rfind("/")+1:] not in manage_list_pages:
            wd.find_element_by_link_text("Manage").click()

        if len(wd.find_elements_by_name("reauth_form")) > 0:
            self.app.session.authenticate(self.app.config["webadmin"]["password"])

    def manage_projects(self):
        wd = self.app.wd
        if not wd.current_url.endswith('manage_proj_page.php'):
            self.__manage()
            wd.find_element_by_link_text("Manage Projects").click()
