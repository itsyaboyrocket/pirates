# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.avatar.Emote
from otp.otpbase import OTPLocalizer
import types

class Emote:
    __module__ = __name__
    EmoteClear = -1
    EmoteEnableStateChanged = 'EmoteEnableStateChanged'

    def __init__(self):
        self.emoteFunc = None
        return

    def isEnabled(self, index):
        if isinstance(index, types.StringType):
            index = OTPLocalizer.EmoteFuncDict[index]
        if self.emoteFunc == None:
            return 0
        else:
            if self.emoteFunc[index][1] == 0:
                return 1
        return 0


globalEmote = None