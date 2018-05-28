# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.pvp.SiegeManagerBase
from pirates.piratesbase import PLocalizer

class SiegeManagerBase:
    __module__ = __name__
    ANNOUNCER_ZONE = 555

    def __init__(self):
        self._useIslandRegen = False
        self._useRepairSpots = False
        self._useRepairKit = False

    def setUseIslandRegen(self, useIslandRegen):
        if self._useIslandRegen:
            not useIslandRegen and self._disableUseIslandRegen()
        else:
            if not self._useIslandRegen and useIslandRegen:
                self._enableUseIslandRegen()
        self._useIslandRegen = useIslandRegen

    def _enableUseIslandRegen(self):
        messenger.send(self.getUseIslandRegenEvent(), [True])

    def _disableUseIslandRegen(self):
        messenger.send(self.getUseIslandRegenEvent(), [False])

    def getUseIslandRegenEvent(self):
        return 'useIslandRegen-%s' % self.doId

    def getUseIslandRegen(self):
        return self._useIslandRegen

    def setUseRepairSpots(self, useRepairSpots):
        if self._useRepairSpots:
            not useRepairSpots and self._disableRepairSpots()
        else:
            if not self._useRepairSpots and useRepairSpots:
                self._enableRepairSpots()
        self._useRepairSpots = useRepairSpots

    def _enableRepairSpots(self):
        messenger.send(self.getUseRepairSpotsEvent(), [True])

    def _disableRepairSpots(self):
        messenger.send(self.getUseRepairSpotsEvent(), [False])

    def getUseRepairSpotsEvent(self):
        return 'useRepairSpots-%s' % self.doId

    def getUseRepairSpots(self):
        return self._useRepairSpots

    def setUseRepairKit(self, useRepairKit):
        if self._useRepairKit:
            not useRepairKit and self._disableRepairKit()
        else:
            if not self._useRepairKit and useRepairKit:
                self._enableRepairKit()
        self._useRepairKit = useRepairKit

    def _enableRepairKit(self):
        messenger.send(self.getUseRepairKitEvent(), [True])

    def _disableRepairKit(self):
        messenger.send(self.getUseRepairKitEvent(), [False])

    def getUseRepairKitEvent(self):
        return 'useRepairKit-%s' % self.doId

    def getUseRepairKit(self):
        return self._useRepairKit