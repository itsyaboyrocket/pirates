# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesgui.CrewMatchInvitee
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from otp.otpbase import OTPGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.piratesbase import PiratesGlobals
from pirates.piratesbase import PLocalizer
from pirates.band import BandConstance
from pirates.piratesgui.RequestButton import RequestButton

class CrewMatchInviteeButton(RequestButton):
    __module__ = __name__

    def __init__(self, text, command):
        RequestButton.__init__(self, text, command)
        self.initialiseoptions(CrewMatchInviteeButton)


class CrewMatchInvitee(DirectFrame):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('CrewMatchInvitee')

    def __init__(self, avId, avName, location, initialRequest=False, crewType=1):
        guiMain = loader.loadModel('models/gui/gui_main')
        DirectFrame.__init__(self, relief=None, pos=(-0.6, 0, 0.47), image=guiMain.find('**/general_frame_e'), image_pos=(0.25,
                                                                                                                          0,
                                                                                                                          0.275), image_scale=0.25)
        self.initialiseoptions(CrewMatchInvitee)
        self.avId = avId
        self.avName = avName
        self.initialRequest = initialRequest
        self.location = location
        self.crewType = crewType
        self.title = DirectLabel(parent=self, relief=None, text=PLocalizer.CrewMatchCrewLookout, text_scale=PiratesGuiGlobals.TextScaleExtraLarge, text_align=TextNode.ACenter, text_fg=PiratesGuiGlobals.TextFG2, text_shadow=PiratesGuiGlobals.TextShadow, text_font=PiratesGlobals.getPirateOutlineFont(), pos=(0.25,
                                                                                                                                                                                                                                                                                                                   0,
                                                                                                                                                                                                                                                                                                                   0.42), image=None, image_scale=0.25)
        nameArray = (
         '\x01CPOrangeHEAD\x01' + self.avName + '\x02', '\x01CPOrangeHEAD\x01' + self.avName + '\x02', '\x01CPOrangeOVER\x01' + self.avName + '\x02', '\x01CPOrangeHEAD\x01' + self.avName + '\x02')
        nameButton = DirectButton(parent=NodePath(), relief=None, text=nameArray, text_align=TextNode.ALeft, text_shadow=PiratesGuiGlobals.TextShadow, textMayChange=0, command=self.handleAvatarPress, extraArgs=[avId, avName])
        left, right, bottom, top = nameButton.getBounds()
        nameGFX = TextGraphic(nameButton, left, right, 0, 1)
        buttonName = '\x05' + self.avName + '\x05'
        if location != '':
            buttonText = PLocalizer.CrewMatchInviteeInvitation % (buttonName, self.location)
        else:
            buttonText = PLocalizer.CrewMatchInviteeInvitationNoLocation % buttonName
        tpMgr = TextPropertiesManager.getGlobalPtr()
        tpMgr.setGraphic(self.avName, nameGFX)
        del tpMgr
        textRender = TextNode('textRender')
        textRender.setFont(PiratesGlobals.getInterfaceFont())
        textRender.setTextColor(PiratesGuiGlobals.TextFG2)
        textRender.setAlign(TextNode.ACenter)
        textRender.setShadowColor(PiratesGuiGlobals.TextShadow)
        textRender.setWordwrap(11)
        textRender.setTabWidth(1.0)
        textRender.setShadow(0.08, 0.08)
        textRender.setText(buttonText)
        textNode = self.attachNewNode(textRender.generate())
        textNode.setScale(PiratesGuiGlobals.TextScaleLarge)
        textNode.setPos(0.25, 0, 0.325)
        self.bOk = CrewMatchInviteeButton(text=PLocalizer.CrewInviteeOK, command=self.__handleOk)
        self.bOk.reparentTo(self)
        self.bOk.setPos(0.1, 0, 0.05)
        self.bNo = CrewMatchInviteeButton(text=PLocalizer.CrewInviteeNo, command=self.__handleNo)
        self.bNo.reparentTo(self)
        self.bNo.setPos(0.3, 0, 0.05)
        self.accept('clientLogout', self.destroy)
        self.accept('destroyCrewMatchInvite', self.destroy)
        return

    def destroy(self):
        if hasattr(self, 'destroyed'):
            return
        self.destroyed = 1
        self.ignore('Esc')
        DirectFrame.destroy(self)

    def __handleOk(self):
        if self.initialRequest:
            base.cr.crewMatchManager.acceptInitialInviteGUI()
        else:
            base.cr.crewMatchManager.acceptInvite()
            base.cr.crewMatchManager.offerCurrentlyOnScreen = False
        self.destroy()

    def __handleNo(self):
        if self.initialRequest:
            base.cr.crewMatchManager.initialAvatarAddResponse(2)
        else:
            base.cr.crewMatchManager.offerCurrentlyOnScreen = False
            base.cr.crewMatchManager.checkOfferCache()
        self.destroy()

    def __handleCancelFromAbove(self):
        self.destroy()

    def handleAvatarPress(self, avId, avName):
        if (hasattr(base, 'localAvatar') and base).localAvatar.guiMgr:
            base.localAvatar.guiMgr.handleAvatarDetails(avId, avName)