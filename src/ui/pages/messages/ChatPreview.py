from Labels.TkLabels import TkMessage
from util.constants import APP_FONT, MAX_MSG_PREVIEW_LENGTH, Colours, BLANK
from util.widgets.buttons.FrameButton import FrameButton
from util.widgets.labels.ImageLabel import ImageLabel


class ChatPreview(FrameButton):
    def __init__(self, master, name, icon, last_msg, date_sent, cmd):
        super().__init__(master, cmd=cmd, bg=master['bg'], activeborder=Colours.GREY)
        self._name, self._icon, self._cmd = name, icon, cmd
        self._last_msg, self._date_sent = last_msg, date_sent
        self._icon_label = ImageLabel(self, icon)
        self._name_lbl = TkMessage(self, text=name, font=(APP_FONT, 12, 'bold'),
                                   anchor='w', justify='left')
        self._msg = TkMessage(self, text=self._get_msg(last_msg), font=(APP_FONT, 10),
                              anchor='w')
        self._date_lbl = TkMessage(self, text=date_sent, font=(APP_FONT, 8),
                                   anchor='e', justify='right')

    def _get_msg(self, msg):
        length = len(msg)
        if length > MAX_MSG_PREVIEW_LENGTH:
            msg = msg[:MAX_MSG_PREVIEW_LENGTH - 8] + ' ...'
        return msg.ljust(MAX_MSG_PREVIEW_LENGTH, BLANK)

    def _config_grid(self):
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=2, uniform='chat')

    def _show(self):
        self._name_lbl.grid(row=0, column=1, columnspan=2, sticky='nesw', pady=(5, 0))
        self._msg.grid(row=1, column=1, columnspan=2, sticky='nesw')
        self._date_lbl.grid(row=2, column=2, sticky='nesw')
        self._icon_label.grid(row=0, column=0, sticky='nesw', rowspan=3, padx=10)

    def _on_click(self):
        self.enable()
        super()._on_click()