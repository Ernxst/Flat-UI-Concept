from Labels.TkLabels import TkMessage
from util.constants import BLANK, MAX_EVENT_DESC_LENGTH, APP_FONT, GREEN, LIGHT_GREEN, NAVBAR_BG
from util.widgets.buttons.FrameButton import FrameButton
from util.widgets.buttons.TkButton import TkButton


class EventsButton(FrameButton):
    def __init__(self, master, month, day, title, description, time, location, cmd, edit_cmd=None):
        super().__init__(master, cmd=cmd, bg=NAVBAR_BG)
        self._edit_cmd = edit_cmd
        self._title_lbl = TkMessage(self, text=title, font=(APP_FONT, 12, 'bold'), anchor='w',
                                    justify='left', bg=self['bg'])
        self._msg = TkMessage(self, text=self._get_msg(description),
                              font=(APP_FONT, 10), anchor='w', justify='left')
        self._month_lbl = TkMessage(self, text=month, font=(APP_FONT, 9), anchor='n')
        self._day_lbl = TkMessage(self, text=day, font=(APP_FONT, 11, 'bold'),
                                  anchor='s')
        self._time_lbl = TkMessage(self, text=time, font=(APP_FONT, 8), anchor='w',
                                   justify='left')
        self._location_lbl = TkMessage(self, text=location, font=(APP_FONT, 8), anchor='e',
                                       justify='right')

    def _get_msg(self, msg):
        length = len(msg)
        if length > MAX_EVENT_DESC_LENGTH:
            msg = msg[:MAX_EVENT_DESC_LENGTH - 8] + ' ...'
        return msg.ljust(MAX_EVENT_DESC_LENGTH, BLANK)

    def _config_grid(self):
        self.columnconfigure((0, 1), weight=1, uniform='cols')
        self.rowconfigure((0, 1, 2, 3), weight=1, uniform='rows')

    def _show(self):
        self._day_lbl.grid(row=0, column=0, rowspan=2, sticky='nesw')
        self._month_lbl.grid(row=2, column=0, sticky='nesw', rowspan=2)
        self._title_lbl.grid(row=0, column=1, columnspan=2, sticky='nesw')
        self._msg.grid(row=1, column=1, columnspan=2, rowspan=2, sticky='nesw')
        self._time_lbl.grid(row=3, column=1, sticky='nesw')
        self._location_lbl.grid(row=3, column=2, sticky='nesw')
        TkButton(self, text='EDIT', bg=LIGHT_GREEN, activebackground=GREEN,
                 command=self._edit_cmd).grid(row=0, column=3, sticky='nesw', rowspan=4)

    def _bind_events(self):
        super()._bind_events()
        self._children.pop(-1)
