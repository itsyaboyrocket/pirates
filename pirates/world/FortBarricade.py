# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.world.FortBarricade
from pandac.PandaModules import NodePath, Point3
from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import rad2Deg, Vec3, GeomVertexFormat, GeomVertexData, GeomVertexWriter, Geom, GeomTriangles, GeomNode, CollisionNode, CollisionPolygon
import math
from pirates.piratesbase import PiratesGlobals

class FortBarricade:
    __module__ = __name__
    notify = directNotify.newCategory('FortBarricade')

    def __init__(self, island, barricadeIds):
        self.island = island
        self.barricadeIds = barricadeIds
        self.colNP = []
        self.loadBarricade()

    def unload(self):
        for coll in self.colNP:
            coll.removeNode()

        self.colNP = []

    def loadBarricade(self):
        colNP1 = self.island.find('**/' + self.barricadeIds[0])
        colNP2 = self.island.find('**/' + self.barricadeIds[1])
        self.colNP = [colNP1, colNP2]

    def disableCollisions(self):
        for coll in self.colNP:
            coll.stash()

    def enableCollisions(self):
        for coll in self.colNP:
            coll.unstash()