# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.StatRowHeadingGui
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from pirates.piratesgui import StatRowGui
from pirates.piratesgui import PiratesGuiGlobals

class StatRowHeadingGui(StatRowGui.StatRowGui):
    __module__ = __name__

    def __init__(self, item, columnHeadings, parent=None, textScale=None, itemHeight=None, itemWidths=[], **kw):
        StatRowGui.StatRowGui.__init__(self, item, columnHeadings, parent, textScale, itemHeight, **kw)
        self.initialiseoptions(StatRowHeadingGui)
        self.columnWidths = itemWidths
        self.headings = []

    def destroy(self):
        self._destroyIface()
        DirectFrame.destroy(self)
        self.ignoreAll()

    def _createIface(self):
        textFg = PiratesGuiGlobals.TextFG1
        self.headings = []
        currColWidth = 0.4
        if len(self.columnWidths) > 0:
            currColWidth = self.columnWidths.pop(0)
        currValueX = currColWidth / 2.0
        for currValueItem in self.item:
            self.headings.append(DirectLabel(parent=self, relief=None, text=str(currValueItem), text_align=TextNode.ACenter, text_scale=self.textScale, text_fg=textFg, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=1, pos=(currValueX, 0, self.getHeight() / 2)))
            currValueX += currColWidth / 2.0
            if len(self.columnWidths) > 0:
                currColWidth = self.columnWidths.pop(0)
            currValueX += currColWidth / 2.0

        return

    def _destroyIface(self):
        StatRowGui.StatRowGui._destroyIface(self)
        for currHeadingText in self.headings:
            currHeadingText.destroy()

        self.headings = []