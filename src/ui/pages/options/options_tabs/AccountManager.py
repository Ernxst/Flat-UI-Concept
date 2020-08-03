from ui.pages.options.options_tabs.OptionsTab import OptionsTab


class AccountManager(OptionsTab):
    def __init__(self, master, model, logout):
        search_terms = ['username', 'password', 'logout', 'sign out', 'log out', 'signout']
        super().__init__(master, 'Account', 'Manage your account.', search_terms)
        self._model = model
        self._logout = logout

    def _config_grid(self):
        pass

    def _show(self):
        pass

    def update_tab_data(self):
        pass

    def logout(self):
        self._logout()