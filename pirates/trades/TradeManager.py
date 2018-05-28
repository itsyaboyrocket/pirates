# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.trades.TradeManager
from direct.distributed.ClockDelta import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObject import DistributedObject
from pirates.uberdog.UberDogGlobals import *

class TradeManager(DistributedObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('TradeManager')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.cr.tradeManager = self

    def delete(self):
        self.ignoreAll()
        if self.cr.tradeManager == self:
            self.cr.tradeManager = None
        DistributedObject.delete(self)
        return

    def sendRequestCreateTrade(self, otherAvatarId):
        self.sendUpdate('requestCreateTrade', [otherAvatarId])

    def rejectCreateTrade(self, otherAvatarId, reasonCode):
        messenger.send('rejectCreateTrade-%s' % (otherAvatarId,), [reasonCode])

    def createTradeResponse(self, otherAvatarId, tradeId):
        self.addInterest(tradeId)