# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.effects.ShockwaveRing
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from PooledEffect import PooledEffect
from EffectController import EffectController
import random

class ShockwaveRing(PooledEffect, EffectController):
    __module__ = __name__

    def __init__(self):
        PooledEffect.__init__(self)
        EffectController.__init__(self)
        self.speed = 0.4
        self.size = 40
        self.explosionSequence = 0
        self.explosion = loader.loadModel('models/effects/shockwaveRing')
        self.explosion.setDepthTest(0)
        self.explosion.node().setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd, ColorBlendAttrib.OIncomingAlpha, ColorBlendAttrib.OOne))
        self.explosion.setFogOff()
        self.explosion.setLightOff()
        self.explosion.setHpr(0, -90, 0)
        self.explosion.reparentTo(self)
        self.hide()
        self.explosion.setBin('shadow', 0)
        self.explosion.setTransparency(TransparencyAttrib.MAlpha)
        self.explosion.setDepthWrite(0)

    def createTrack(self, rate=1):
        self.explosion.setScale(1)
        self.explosion.setColorScale(1, 1, 1, 1)
        fadeBlast = self.explosion.colorScaleInterval(self.speed, Vec4(0, 0, 0, 0))
        scaleBlast = self.explosion.scaleInterval(self.speed, self.size, blendType='easeIn', other=render)
        self.track = Sequence(Func(self.show), Parallel(scaleBlast, fadeBlast), Wait(self.speed), Func(self.hide), Func(self.cleanUpEffect))

    def cleanUpEffect(self):
        EffectController.cleanUpEffect(self)
        self.checkInEffect(self)

    def destroy(self):
        EffectController.destroy(self)
        PooledEffect.destroy(self)