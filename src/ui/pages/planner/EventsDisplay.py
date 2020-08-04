from tkinter import Frame, Label

from Labels.TkLabels import TkMessage
from ui.pages.planner.EventsButton import EventsButton
from util.constants import GREY, APP_FONT, LIGHT_GREEN, GREEN
from util.widgets.buttons.TkButton import TkButton
from util.widgets.frames.LazyScrolledFrame import LazyScrolledFrame


class EventsDisplay(Frame):
    def __init__(self, master, model):
        super().__init__(master, bg=GREY, highlightthickness=0)
        self._model = model
        self._upcoming_events = self._model.get_events()
        self._content = LazyScrolledFrame(self)
        self._popup = None
        self._event_btns = {}
        self._subtitle = TkMessage(self, text='You have no upcoming events scheduled.',
                                   fg='black', anchor='center')

    def update_events(self):
        self._model.update_events()
        self._upcoming_events = self._model.get_events()
        if len(self._upcoming_events) > 0:
            self._subtitle.grid_forget()
        else:
            self._subtitle.grid(row=1, column=0, sticky='', padx=20)
        # update ui

    def _config_grid(self):
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self._content.interior_frame.columnconfigure(0, weight=1)

    def grid(self, **kwargs):
        super().grid(**kwargs)
        self._config_grid()
        self._show()

    def _show(self):
        Label(self, text='Upcoming Events', fg='black', font=(APP_FONT, 16, 'bold'), padx=20,
              anchor='w', bg=self['bg']).grid(row=0, column=0, sticky='nesw', pady=(20, 10))
        if len(self._upcoming_events) == 0:
            self._subtitle.grid(row=1, column=0, sticky='', padx=20)
        else:
            self._show_events()
            self._content.grid(row=1, column=0, sticky='nesw', padx=10, pady=(0, 10), scrollpady=0)
        TkButton(self, text='New Event', font=(APP_FONT, 10, 'bold'), bg=LIGHT_GREEN,
                 activebackground=GREEN).grid(row=2, column=0, sticky='nesw', ipady=5)

    def _show_events(self):
        for row, (id_, data) in enumerate(self._upcoming_events.items()):
            (month, day, year, title, description, time, location) = data
            self._event_btns[id_] = EventsButton(self._content.interior_frame, month, day,
                                                 year, title, description, time, location,
                                                 lambda evt_id=id_: self._open_event(evt_id))
            self._content.add(self._event_btns[id_], row=row, column=0, sticky='nesw', pady=1)

    def _open_event(self, id_):
        event_data = self._upcoming_events[id_]
        # show in popup

    def _edit_event(self, id_):
        event_data = self._upcoming_events[id_]
        # show in popup

    def _delete_event(self, id_):
        pass

    def _add_event(self):
        pass

    def search(self, search_term):
        for (id_, data) in self._upcoming_events.items():
            month, day, year, *args = data
            if any(search_term.lower() in string for string in [str(x).lower() for x in data]):
                return id_, month, day, year
        return None, None, None, None

    def select_event(self, id_):
        [btn.disable() for btn in self._event_btns.values()]
        active_button = self._event_btns[id_]
        active_button.enable()
        self._scroll_to_event(active_button)

    def _scroll_to_event(self, active_button):
        index = list(self._event_btns.values()).index(active_button)
        fraction = float(index / len(self._content.interior_frame.winfo_children()))
        self._content.canvas.yview_moveto(fraction)
