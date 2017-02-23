from direct.gui.DirectCheckButton import DirectCheckButton
from direct.gui.DirectGuiGlobals import DISABLED
from direct.gui.DirectLabel import DirectLabel
from panda3d.core import TextNode
from yyagl.engine.gui.page import Page, PageEvent, PageGui
from yyagl.engine.joystick import has_pygame
from direct.gui.DirectButton import DirectButton
import string


class InputEvent(PageEvent):

    def on_back(self):
        settings = game.options['settings']
        settings['keys'] = {
            'forward': self.mdt.gui._forward_btn['text'],
            'rear': self.mdt.gui._rear_btn['text'],
            'left': self.mdt.gui._left_btn['text'],
            'right': self.mdt.gui._right_btn['text'],
            'button': self.mdt.gui._button_btn['text']}
        settings['joystick'] = self.mdt.gui._joypad_cb['indicatorValue']
        game.options.store()


class InputPageGui(PageGui):

    def __init__(self, mdt, menu):
        self._joypad_cb = None
        self._forward_btn = None
        self._rear_btn = None
        self._left_btn = None
        self._right_btn = None
        self._button_btn = None
        PageGui.__init__(self, mdt, menu)

    def build_page(self):
        conf = game.options
        menu_gui = self.menu.gui

        joypad_lab = DirectLabel(
            text=_('Use the joypad when present'), pos=(-.1, 1, .7),
            text_align=TextNode.ARight, **menu_gui.label_args)
        PageGui.transl_text(joypad_lab, 'Use the joypad when present',
                            _('Use the joypad when present'))
        self._joypad_cb = DirectCheckButton(
            pos=(.09, 1, .72), text='',
            indicatorValue=conf['settings']['joystick'],
            indicator_frameColor=(.75, .75, .25, 1),
            **menu_gui.checkbtn_args)
        if not has_pygame():
            self._joypad_cb['state'] = DISABLED

        forward_lab = DirectLabel(
            text=_('Accelerate'), pos=(-.1, 1, .5), text_align=TextNode.ARight,
            **menu_gui.label_args)
        self._forward_btn = DirectButton(
            pos=(.46, 1, .5), text=conf['settings']['keys']['forward'],
            command=self.start_rec, **menu_gui.btn_args)
        self._forward_btn['extraArgs'] = [self._forward_btn]

        rear_lab = DirectLabel(
            text=_('Brake/Reverse'), pos=(-.1, 1, .3),
            text_align=TextNode.ARight, **menu_gui.label_args)
        self._rear_btn = DirectButton(
            pos=(.46, 1, .3), text=conf['settings']['keys']['rear'],
            command=self.start_rec, **menu_gui.btn_args)
        self._rear_btn['extraArgs'] = [self._rear_btn]

        left_lab = DirectLabel(
            text=_('Left'), pos=(-.1, 1, .1), text_align=TextNode.ARight,
            **menu_gui.label_args)
        self._left_btn = DirectButton(
            pos=(.46, 1, .1), text=conf['settings']['keys']['left'],
            command=self.start_rec, **menu_gui.btn_args)
        self._left_btn['extraArgs'] = [self._left_btn]

        right_lab = DirectLabel(
            text=_('Right'), pos=(-.1, 1, -.1), text_align=TextNode.ARight,
            **menu_gui.label_args)
        self._right_btn = DirectButton(
            pos=(.46, 1, -.1), text=conf['settings']['keys']['right'],
            command=self.start_rec, **menu_gui.btn_args)
        self._right_btn['extraArgs'] = [self._right_btn]

        button_lab = DirectLabel(
            text=_('Weapon'), pos=(-.1, 1, -.3), text_align=TextNode.ARight,
            **menu_gui.label_args)
        self._button_btn = DirectButton(
            pos=(.46, 1, -.3), text=conf['settings']['keys']['button'],
            command=self.start_rec, **menu_gui.btn_args)
        self._button_btn['extraArgs'] = [self._button_btn]

        la = menu_gui.label_args.copy()
        del la['scale']
        self.hint_lab = DirectLabel(
            text=_('Press the key to record it'), pos=(0, 1, -.5), scale=.065,
            **la)
        self.hint_lab.hide()

        numbers = [str(n) for n in range(10)]
        self.keys = list(string.ascii_lowercase) + numbers + [
            'backspace', 'insert', 'home', 'page_up', 'num_lock', 'tab',
            'delete', 'end', 'page_down', 'caps_lock', 'enter', 'arrow_left',
            'arrow_up', 'arrow_down', 'arrow_right', 'lshift', 'rshift',
            'lcontrol', 'lalt', 'space', 'ralt', 'rcontrol']
        self.widgets += [
            joypad_lab, self._joypad_cb, forward_lab, self._forward_btn,
            rear_lab, self._rear_btn, left_lab, self._left_btn, right_lab,
            self._right_btn, button_lab, self._button_btn, self.hint_lab]
        PageGui.build_page(self)

    def start_rec(self, btn):
        self.hint_lab.show()
        acc = lambda key: self.mdt.event.accept(key, self.rec, [btn, key])
        map(acc, self.keys)

    def rec(self, btn, val):
        btn['text'] = val
        self.hint_lab.hide()
        map(self.mdt.event.ignore, self.keys)


class InputPage(Page):
    gui_cls = InputPageGui
    event_cls = InputEvent
