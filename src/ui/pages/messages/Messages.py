from tkinter import Frame
from tkinter.ttk import Separator

from Labels.TkLabels import TkMessage
from Util.tkUtilities import error_msg, get_widget_dimensions
from src.ui.pages.MenuPage import MenuPage
from src.ui.pages.messages.ChatPreview import ChatPreview
from src.util.constants import APP_FONT, APP_BG, PROFILE_BG, GREEN, LIGHT_GREEN, GREY
from src.util.widgets.buttons.TkButton import TkButton
from src.util.widgets.entries.AppEntry import AppEntry
from src.util.widgets.frames.ScrolledFrame import ScrolledFrame


class Messages(MenuPage):
    def __init__(self, master, model):
        super().__init__(master, 'Messages', 'View your instant-messaging conversations.',
                         model)
        self._chat_frame = Frame(self._content.interior_frame, bg=GREY, highlightthickness=0)
        self._contact_frame = Frame(self._content.interior_frame, bg='red', highlightthickness=0)
        self._chat_preview_frame = ScrolledFrame(self._contact_frame, scrollbar_bg=APP_BG,
                                                 bg=PROFILE_BG)
        self._chat_data = self._model.get_chats()
        self._btns = {}
        self._entry = AppEntry(self._contact_frame, default_text='Search your messages...',
                               font=(APP_FONT, 10), justify='left', has_label=False)

    def _update_page_data(self):
        self._chat_data = self._model.get_chats()
        # update ui

    def disable_resize(self):
        super().disable_resize()
        self._chat_preview_frame.disable_resize()

    def enable_resize(self):
        super().enable_resize()
        self._chat_preview_frame.enable_resize()

    def _config_grid(self):
        self._content.interior_frame.rowconfigure(0, weight=1)
        self._content.interior_frame.columnconfigure(1, weight=5, uniform='msg')
        self._contact_frame.rowconfigure(1, weight=1)
        self._contact_frame.columnconfigure(0, weight=1)
        self._chat_preview_frame.interior_frame.columnconfigure(0, weight=1)

    def _show(self):
        self._show_chat()
        self._show_chat_preview()
        width = (get_widget_dimensions(self._content.canvas))[0]
        self._content.canvas.itemconfig(self._content.id_, width=width)

    def _show_chat_preview(self):
        self._contact_frame.grid(row=0, column=0, sticky='nesw', padx=(20, 0), pady=(10, 20))
        self._show_entry()
        self._show_contacts(self._chat_data)
        TkButton(self._contact_frame, text='New Chat', command=self.new_chat,
                 font=(APP_FONT, 12, 'bold'), bg=LIGHT_GREEN, activebackground=GREEN
                 ).grid(row=2, column=0, sticky='nesw', ipady=5)

    def _show_contacts(self, chat_data):  # make sure all icons are the same size
        self._chat_preview_frame.grid(row=1, column=0, sticky='nesw', scrollpady=0)
        for (username, data) in chat_data.items():
            name, icon, last_msg, date_sent = data
            self._btns[username] = ChatPreview(self._chat_preview_frame.interior_frame, name,
                                               icon, last_msg, date_sent,
                                               lambda user=username: self.open_chat(user))
            self._btns[username].grid(column=0, sticky='nesw')
            Separator(self._chat_preview_frame.interior_frame, orient='horizontal'
                      ).grid(column=0, sticky='nesw', padx=10, pady=5)

    def _show_entry(self):
        self._entry.grid(row=0, column=0, sticky='nesw')
        self._entry.bind('<Return>', lambda event: self.search(self._entry.get()))

    def _select_chat(self, username):
        [btn.disable() for btn in self._btns.values()]
        active_button = self._btns[username]
        active_button.enable()
        self._scroll_to_chat(active_button)
        self.open_chat(username)

    def _scroll_to_chat(self, active_button):
        index = list(self._btns.values()).index(active_button)
        fraction = float(index / len(self._content.interior_frame.winfo_children()))
        self._content.canvas.yview_moveto(fraction)

    def search(self, search_term):
        self._entry.delete()
        if search_term == '':
            return
        for username, data in self._chat_data.items():
            if any(search_term.lower() in string for string in [x.lower() for x in data]):
                self._select_chat(username)
                return
        error_msg('Not found', 'Could not find "{}" on this page. '
                               'Please try searching another page.'.format(search_term))

    def _show_chat(self):
        self._chat_frame.grid(row=0, column=1, sticky='nesw', padx=(0, 20), pady=(10, 20))
        self._chat_frame.rowconfigure(0, weight=1)
        self._chat_frame.columnconfigure(0, weight=1)
        TkMessage(self._chat_frame, text='Click a contact in the tab to the left to open the chat',
                  justify='center', anchor='center', font=(APP_FONT, 12, 'bold'), fg='black'
                  ).grid(row=0, column=0, sticky='')

    def open_chat(self, username):
        [btn.disable() for btn in self._btns.values()]
        self._btns[username].enable()

    def new_chat(self):
        pass
