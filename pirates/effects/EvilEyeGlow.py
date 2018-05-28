# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.EvilEyeGlow
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui.GameOptions import Options
from PooledEffect import PooledEffect
from EffectController import EffectController

class EvilEyeGlow(PooledEffect, EffectController):
    __module__ = __name__

    def __init__(self, effectParent=None, billboardOffset=1.0):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        if effectParent:
            self.reparentTo(effectParent)
        self.glow = loader.loadModel('models/effects/lanternGlow')
        self.glow.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne), 5)
        self.glow.setHpr(90, 90, 0)
        self.glow.setLightOff()
        self.glow.setFogOff()
        self.glow.reparentTo(self)
        self.glow.setScale(1.5)
        self.glow.setPos(Vec3(0, 0, 0))
        self.glow.setDepthWrite(0, 2)
        self.glow.setTransparency(1)
        self.fadeIval = None
        self.scaleIval = None
        return

    def createTrack(self, lod=None):
        scaleUpHalo = self.glow.scaleInterval(0.15, 1.0, startScale=0.9, blendType='easeInOut')
        scaleDownHalo = self.glow.scaleInterval(0.15, 0.9, startScale=1.0, blendType='easeInOut')
        self.scaleIval = Sequence(scaleDownHalo, scaleUpHalo)
        self.startEffect = Sequence(Func(self.scaleIval.loop))
        self.endEffect = Sequence(Func(self.scaleIval.finish))
        self.track = Sequence(self.startEffect, Wait(2.0), self.endEffect)

    def enableEffect(self):
        if self.scaleIval:
            self.scaleIval.loop()

    def disableEffect(self):
        if self.scaleIval:
            self.scaleIval.pause()

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        self.glow.removeNode()
        EffectController.destroy(self)
        PooledEffect.destroy(self)