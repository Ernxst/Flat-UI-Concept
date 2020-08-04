from Labels.TkLabels import TkMessage
from models.Model import get_model
from util.constants import APP_FONT, RED, DARK_RED
from util.widgets.buttons.FrameButton import FrameButton
from util.widgets.buttons.TkButton import TkButton
from util.widgets.labels.ImageLabel import ImageLabel


class NotificationButton(FrameButton):
    def __init__(self, master, id_, name, icon, title, msg, date_sent,
                 cmd=None, clear_cmd=None, bg=None):
        bg = bg if bg else master['bg']
        super().__init__(master, bg=bg, cmd=cmd)
        self._id_ = id_
        self._clear_cmd = clear_cmd
        self._cmd = cmd

        self._icon_label = ImageLabel(self, icon)
        self._name_lbl = TkMessage(self, text=name, font=(APP_FONT, 10, 'bold'), anchor='e',
                                   justify='left',  bg=self['bg'])
        self._title_lbl = TkMessage(self, text=title, font=(APP_FONT, 12, 'bold'), anchor='w',
                                    justify='left', bg=self['bg'])
        self._msg = TkMessage(self, text=msg, font=(APP_FONT, 10), anchor='w', justify='left')
        self._date_lbl = TkMessage(self, text=date_sent, font=(APP_FONT, 8), bg=self['bg'],
                                   anchor='e', justify='right')

    def _config_grid(self):
        self.rowconfigure((0, 1, 2), weight=1, uniform='rows')
        self.columnconfigure(1, weight=1, uniform='cols')
        
    def _bind_events(self):
        super()._bind_events()
        self._children.pop(-1)

    def _show(self):
        self._title_lbl.grid(row=0, column=1, sticky='nesw', pady=(5, 0))
        self._name_lbl.grid(row=0, column=2, sticky='nesw', pady=(5, 0))
        self._msg.grid(row=1, column=1, columnspan=2, sticky='nesw')
        self._date_lbl.grid(row=2, column=1, columnspan=2, sticky='nesw')
        self._icon_label.grid(row=0, column=0, sticky='nesw', rowspan=3, padx=10)
        TkButton(self, text='X', font=(APP_FONT, 10, 'bold'), command=self._clear_notification,
                 bg=RED, activebackground=DARK_RED).grid(row=0, column=3, rowspan=3, sticky='nesw')

    def _clear_notification(self):
        get_model().clear_notification(self._id_)
        if self._clear_cmd is not None:
            self._clear_cmd()
        if self._cmd is not None:
            self._cmd()
        self.destroy()
