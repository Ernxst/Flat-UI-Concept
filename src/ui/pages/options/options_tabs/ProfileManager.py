from ui.pages.options.options_tabs.OptionsTab import OptionsTab


class ProfileManager(OptionsTab):
    def __init__(self, master, name, icon, model):
        search_terms = ['icon', 'avi', 'profile', 'profile picture', 'picture',
                        'name', 'display name', 'bio', 'status']
        super().__init__(master, 'Profile', 'Manage your profile.', search_terms)
        self._name = name
        self._icon = icon
        self._model = model

    def _config_grid(self):
        pass

    def _show(self):
        self._show_icon()
        self._show_name()
        self._show_options()

    def _show_icon(self):
        pass

    def _show_name(self):
        pass

    def _show_options(self):
        pass

    def update_tab_data(self):
        pass