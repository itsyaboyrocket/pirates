# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.instance.DistributedInstanceWorld
from pirates.instance.DistributedInstanceBase import DistributedInstanceBase
from pandac.PandaModules import NodePath

class DistributedInstanceWorld(DistributedInstanceBase, NodePath):
    __module__ = __name__

    def __init__(self, cr):
        DistributedInstanceBase.__init__(self, cr)
        self.jailContext = None
        return

    def delete(self):
        del self.jailContext
        DistributedInstanceBase.delete(self)

    def getInstanceNodePath(self):
        return self

    def localAvEnterDeath(self, av):
        DistributedInstanceBase.localAvEnterDeath(self, av)
        if av.isLocal():
            self.d_localAvatarDied()

    def localAvExitDeath(self, av):
        DistributedInstanceBase.localAvExitDeath(self, av)