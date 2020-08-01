from tkinter import Frame, Label
from tkinter.ttk import Separator

from models.Model import get_model
from ui.pages.planner.EventsButton import EventsButton
from util.constants import GREY, APP_FONT
from util.widgets.frames.ScrolledFrame import ScrolledFrame


class EventsDisplay(Frame):
    def __init__(self, master):
        super().__init__(master, bg=GREY, highlightthickness=0)
        self._model = get_model()
        self._upcoming_events = self._model.get_events()
        self._content = ScrolledFrame(self)
        self._popup = None
        self._event_btns = {}

    def update_events(self):
        self._model.update_events()
        self._upcoming_events = self._model.get_events()
        print('upcoming:', self._upcoming_events)

    def _config_grid(self):
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self._content.interior_frame.columnconfigure(0, weight=1)
        # self._content.interior_frame.rowconfigure(tuple(range(len(self._events))),
        #                                           weight=1, uniform='events')

    def grid(self, **kwargs):
        super().grid(**kwargs)
        self._config_grid()
        self._show()

    def _show(self):
        Label(self, text='Upcoming Events', fg='black', font=(APP_FONT, 12, 'bold'),
              padx=5, pady=5, bg=self['bg']).grid(row=0, column=0, sticky='nesw')
        self._content.grid(row=1, column=0, sticky='nesw', padx=10, pady=(0, 10), scrollpady=0)
        self._show_events()

    def _show_events(self):
        for (id_, (month, day, title, description, time, location)) in self._upcoming_events.items():
            self._event_btns[id_] = EventsButton(self._content.interior_frame, month, day,
                                                 title, description, time, location, lambda
                                                 event_id=id_: self._open_event(event_id))
            self._event_btns[id_].grid(column=0, sticky='nesw')
            Separator(self._content.interior_frame, orient='horizontal'
                      ).grid(column=0, sticky='nesw', pady=10)

    def _open_event(self, id_):
        event_data = self._upcoming_events[id_]
        # show in popup

    def _edit_event(self, id_):
        event_data = self._upcoming_events[id_]
        # show in popup

    def _delete_event(self, id_):
        pass
