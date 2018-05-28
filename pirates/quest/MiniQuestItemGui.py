# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.quest.MiniQuestItemGui
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import PiratesGuiGlobals

class MiniQuestItemGui(DirectFrame):
    __module__ = __name__
    Width = PiratesGuiGlobals.ObjectivesPanelWidth - PiratesGuiGlobals.GridSize
    Height = 0.1

    def __init__(self, quest, parent=None, **kw):
        optiondefs = (('state', DGG.NORMAL, None), ('frameColor', PiratesGuiGlobals.FrameColor, None), ('borderWidth', PiratesGuiGlobals.BorderWidth, None), ('frameSize', (0.0, MiniQuestItemGui.Width, 0.0, MiniQuestItemGui.Height), None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent)
        self.initialiseoptions(MiniQuestItemGui)
        self.quest = quest
        self._createIface()
        self.accept(self.quest.getChangeEvent(), self.handleQuestChange)
        return

    def destroy(self):
        self._destroyIface()
        DirectFrame.destroy(self)
        del self.quest
        self.ignoreAll()

    def _createIface(self):
        if self.quest.isComplete():
            textFg = (0.1, 0.8, 0.1, 1)
        else:
            textFg = PiratesGuiGlobals.TextFG1
        self.descText = DirectLabel(parent=self, relief=None, text=self.quest.getStatusText(), text_align=TextNode.ALeft, text_scale=PiratesGuiGlobals.TextScaleLarge, text_fg=textFg, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, pos=(0.04,
                                                                                                                                                                                                                                                       0,
                                                                                                                                                                                                                                                       0.05))
        return

    def _destroyIface(self):
        self.descText.destroy()
        del self.descText

    def handleQuestChange(self):
        self._destroyIface()
        self._createIface()