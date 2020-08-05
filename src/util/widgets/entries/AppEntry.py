from Entries.TkEntry import TkEntry
from util.colour_constants import Colours
from util.constants import APP_FONT


class AppEntry(TkEntry):
    def __init__(self, parent, title='', default_text='', font=(APP_FONT, 10),
                 has_label=True, fg='black', justify='center', insertbackground=Colours.TITLE_BG, **kwargs):
        super().__init__(parent, title, default_text, font, has_label, fg, justify,
                         insertbackground=insertbackground, **kwargs)

    def activate(self):
        self.entry.config(highlightcolor=Colours.TITLE_BG)
        self.entry.focus_set()

    def reset(self):
        if len(self.get(False)) == 0:
            self.entry.config(fg='grey', highlightcolor=self.master['bg'])
            self.entry.insert(0, self.default_text)