from tkinter import Frame
from tkinter.ttk import Separator

from Labels.TkLabels import TkMessage
from Util.tkUtilities import get_widget_dimensions
from models.Model import get_model
from ui.pages.MenuPage import MenuPage
from ui.pages.messages.ChatPreview import ChatPreview
from util.constants import APP_FONT, APP_BG, PROFILE_BG, GREEN, LIGHT_GREEN, GREY
from util.widgets.entries.AppEntry import AppEntry
from util.widgets.frames.ScrolledFrame import ScrolledFrame
from util.widgets.buttons.TkButton import TkButton


class Messages(MenuPage):
    def search(self, search_term):
        pass

    def __init__(self, master, name):
        super().__init__(master, 'Messages', 'View your instant-messaging conversations.')
        self._name = name
        self._chat_frame = Frame(self._content.interior_frame, bg=GREY, highlightthickness=0)
        self._contact_frame = Frame(self._content.interior_frame, bg=PROFILE_BG, highlightthickness=0)
        self._chat_preview_frame = ScrolledFrame(self._contact_frame, scrollbar_bg=APP_BG,
                                                 bg=PROFILE_BG)
        self._model = get_model()
        self._chat_data = self._model.get_chats()
        self._btns = {}

    def _update_page_data(self):
        self._chat_data = self._model.get_chats()
        # update ui

    def _config_grid(self):
        self._content.interior_frame.rowconfigure(1, weight=1)
        self._content.interior_frame.columnconfigure(0, weight=2, uniform='msg')
        self._content.interior_frame.columnconfigure(1, weight=5, uniform='msg')
        self._contact_frame.rowconfigure(1, weight=1)
        self._contact_frame.columnconfigure(0, weight=1)
        self._chat_preview_frame.interior_frame.columnconfigure(0, weight=1)

    def _show(self):
        self._show_chat()
        self._show_chat_preview()
        self._default_size()

    def _default_size(self):  # fix sizing and resize
        width, height = get_widget_dimensions(self._content)
        title_frame = self._content.interior_frame.winfo_children()[0]
        h = height - get_widget_dimensions(title_frame)[1] - 30
        self._chat_frame.config(height=h)
        self._contact_frame.config(height=h)
        self._chat_preview_frame.canvas.config(height=h)
        self._chat_preview_frame.interior_frame.config(height=h)

    def _show_chat_preview(self):
        self._contact_frame.grid(row=1, column=0, sticky='nesw', padx=(20, 0), pady=(10, 20))
        self._show_entry()
        self._show_contacts(self._chat_data)
        TkButton(self._contact_frame, text='New Chat', command=self.new_chat,
                 font=(APP_FONT, 12, 'bold'), bg=LIGHT_GREEN, activebackground=GREEN
                 ).grid(row=2, column=0, sticky='nesw', ipady=5)

    def _show_contacts(self, chat_data):  # make sure all icons are the same size
        self._chat_preview_frame.grid(row=1, column=0, sticky='nesw', scrollpady=0)
        for row, (username, data) in enumerate(chat_data.items()):
            name, icon, last_msg, date_sent = data
            self._btns[username] = ChatPreview(self._chat_preview_frame.interior_frame, name,
                                               icon, last_msg, date_sent,
                                               lambda user=username: self.open_chat(user))
            self._btns[username].grid(column=0, sticky='nesw')
            Separator(self._chat_preview_frame.interior_frame, orient='horizontal'
                      ).grid(column=0, sticky='nesw', padx=10, pady=5)
            row += 1

    def _show_entry(self):
        entry = AppEntry(self._contact_frame, default_text='Search your messages...',
                         font=(APP_FONT, 10), justify='left', has_label=False)
        entry.grid(row=0, column=0, sticky='nesw')
        entry.bind('<Return>', lambda event: self._search(entry.get()))

    def _search(self, search_term):
        print(search_term)

    def _show_chat(self):
        self._chat_frame.grid(row=1, column=1, sticky='nesw', padx=(0, 20), pady=(10, 20))
        self._chat_frame.rowconfigure(0, weight=1)
        self._chat_frame.columnconfigure(0, weight=1)
        TkMessage(self._chat_frame, text='Click a contact in the tab to the left to open the chat',
                  font=(APP_FONT, 12, 'bold'), fg='black').grid(row=0, column=0, sticky='')

    def open_chat(self, username):
        [btn.disable() for btn in self._btns.values()]
        self._btns[username].enable()

    def new_chat(self):
        pass