# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.login.SecretFriendsInfoPanel
from pandac.PandaModules import *
from otp.otpbase.OTPGlobals import *
from direct.gui.DirectGui import *
from MultiPageTextFrame import *
from otp.otpbase import OTPLocalizer
from otp.otpgui import OTPDialog

class SecretFriendsInfoPanel(getGlobalDialogClass()):
    __module__ = __name__

    def __init__(self, doneEvent, hidePageNum=0, pageChangeCallback=None):
        dialogClass = getGlobalDialogClass()
        dialogClass.__init__(self, parent=aspect2d, dialogName='secretFriendsInfoDialog', doneEvent=doneEvent, okButtonText=OTPLocalizer.SecretFriendsInfoPanelClose, style=OTPDialog.Acknowledge, text='', topPad=1.5, sidePad=1.2, pos=(0,
                                                                                                                                                                                                                                          0,
                                                                                                                                                                                                                                          0.1), scale=0.9)
        self.textPanel = MultiPageTextFrame(parent=self, textList=OTPLocalizer.SecretFriendsInfoPanelText, hidePageNum=hidePageNum, pageChangeCallback=pageChangeCallback)
        self['image'] = self['image']
        self['image_pos'] = (0, 0, -0.1)
        self['image_scale'] = (2, 1, 1.3)
        closeButton = self.getChild(0)
        closeButton.setZ(-0.56)