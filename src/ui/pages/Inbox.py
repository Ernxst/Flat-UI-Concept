from ui.pages.MenuPage import MenuPage


class Inbox(MenuPage):
    def _update_page_data(self):
        pass

    def _config_grid(self):
        pass

    def _show(self):
        pass

    def search(self, search_term):
        pass

    def __init__(self, master, model):
        super().__init__(master, 'Inbox', model=model)