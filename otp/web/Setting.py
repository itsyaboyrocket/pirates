# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.web.Setting
from direct.fsm.StatePush import StateVar

class Setting:
    __module__ = __name__

    def __init__(self, name, value):
        self._name = name
        self.setValue(value)

    def getName(self):
        return self._name

    def setValue(self, value):
        self._value = value

    def getValue(self):
        return self._value


class StateVarSetting(Setting, StateVar):
    __module__ = __name__

    def __init__(self, name, value):
        StateVar.__init__(self, value)
        Setting.__init__(self, name, value)

    def setValue(self, value):
        StateVar.set(self, value)

    def getValue(self):
        return StateVar.get(self)