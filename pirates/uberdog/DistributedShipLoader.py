# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.uberdog.DistributedShipLoader
from direct.distributed.ClockDelta import *
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from cPickle import loads, dumps
from pirates.uberdog.UberDogGlobals import *

class DistributedShipLoader(DistributedObject.DistributedObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedShipLoader')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.ships = {}
        self.notify.warning('ShipLoader going online')

    def delete(self):
        self.ignoreAll()
        self.notify.warning('ShipLoader going offline')
        self.cr.shipLoader = None
        DistributedObject.DistributedObject.delete(self)
        return