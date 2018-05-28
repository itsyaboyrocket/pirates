# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.npc.PotionInstructionPanel
from pirates.piratesgui.GuiPanel import *
from pirates.piratesgui.RequestButton import RequestButton
from pirates.piratesbase import PLocalizer

class PotionInstructionPanel(GuiPanel):
    __module__ = __name__

    def __init__(self):
        GuiPanel.__init__(self, PLocalizer.GypsyPotionCraftingTitle, 1, 0.4, showClose=False, titleSize=1.5)
        self.setPos((-0.5, 0, 0))
        self.bQuit = RequestButton(text=PLocalizer.GypsyPotionCraftingClose, command=self.quit)
        self.bQuit.reparentTo(self)
        self.bQuit.setPos(0.45, 0, 0.03)
        self.message = None
        self.callBack = None
        return

    def show(self, onInstructionsComplete):
        if self.message is not None:
            self.message.removeNode()
        self.callBack = onInstructionsComplete
        self.messageText = PLocalizer.GypsyPotionCraftingMessage
        self.message = DirectLabel(parent=self, relief=None, text=self.messageText, text_scale=PiratesGuiGlobals.TextScaleLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_wordwrap=22, pos=(0.5,
                                                                                                                                                                                                                                                                  0,
                                                                                                                                                                                                                                                                  0.27), textMayChange=0)
        self.unstash()
        localAvatar.motionFSM.off()
        return

    def quit(self):
        localAvatar.motionFSM.on()
        self.stash()
        if self.callBack is not None:
            self.callBack()
        return