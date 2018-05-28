# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.npc.Townfolk
from pandac.PandaModules import *
from pirates.piratesbase import PiratesGlobals
from pirates.pirate import Biped
from pirates.pirate import Human
from pirates.pirate import AvatarTypes
AnimDict = {}

class Townfolk(Human.Human):
    __module__ = __name__

    def __init__(self):
        Human.Human.__init__(self)
        self.avatarType = AvatarTypes.Townfolk
        self.castDnaId = None
        self.animDict = {}
        self.wantsActive = 0
        return

    def loadCast(self, dnaId):
        if not self.loaded:
            self.setGeomNode(self.find('**/actorGeom'))
            self.loadModel(dnaId)
            self.mixingEnabled = False
            modelName = dnaId.split('_2000')[0]
            modelName = modelName.split('_zero')[0]
            animList = Human.CastAnimDict[modelName]
            for anim in animList:
                self.animDict[anim[0]] = 'models/char/' + anim[1]

            if 'jg_' not in dnaId:
                self.tutorialCharacter = 1
            self.loadAnims(self.animDict)
            self.forceLoadAnimDict()
            self.loaded = 1
            self.castDnaId = dnaId

            def getWeaponJoints():
                self.deleteWeaponJoints()
                self.rightHandNode = NodePath('rightHand')
                self.leftHandNode = NodePath('leftHand')
                handLocator = self.find('**/*weapon_right')
                if not handLocator.isEmpty():
                    self.rightHandNode.reparentTo(handLocator)
                handLocator = self.find('**/*weapon_left')
                if not handLocator.isEmpty():
                    self.leftHandNode.reparentTo(handLocator)

            getWeaponJoints()
        self.faceAwayFromViewer()
        self.headNode = self.find('**/def_head01')
        self.initializeMiscNodes()
        self.loop('idle')

    def unloadCast(self):
        self.stop(None)
        if self.castDnaId:
            modelName = self.castDnaId.split('_2000')[0]
            modelName = modelName.split('_zero')[0]
            animList = Human.CastAnimDict[modelName]
            for anim in animList:
                AnimDict[anim[0]] = 'models/char/' + anim[1]

            self.unloadAnims(AnimDict)
            self.castDnaId = None
            self.flush()
            self.loaded = 0
        else:
            if self.loaded:
                self.cleanupHuman()
        return

    def forceLOD(self, level):
        lodNode = self.find('**/+LODNode')
        if not lodNode.isEmpty():
            lodNode.node().forceSwitch(level)

    def resetLOD(self):
        lodNode = self.find('**/+LODNode')
        if not lodNode.isEmpty():
            lodNode.node().clearForceSwitch()