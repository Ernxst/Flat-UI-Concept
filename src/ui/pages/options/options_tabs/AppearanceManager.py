from ui.pages.options.options_tabs.OptionsTab import OptionsTab


class AppearanceManager(OptionsTab):
    def __init__(self, master):
        search_terms = ['resolution', 'window size', 'dark mode', 'theme']
        super().__init__(master, 'Appearance', 'Adjust the window appearance', search_terms)

    def _config_grid(self):
        pass

    def _show(self):
        pass

    def update_tab_data(self):
        pass