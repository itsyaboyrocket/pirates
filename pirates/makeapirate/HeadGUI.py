# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.makeapirate.HeadGUI
from direct.directnotify import DirectNotifyGlobal
from direct.showbase.ShowBaseGlobal import *
from direct.showbase import DirectObject
import Shape, Mouth, Eyes, Nose, Ear

class HeadGUI(DirectObject.DirectObject):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('HeadGUI')

    def __init__(self, main=None):
        self.main = main
        self.parent = main.bookModel
        self.avatar = main.avatar
        self.mode = None
        self.load()
        return

    def load(self):
        self.shape = Shape.Shape(self)
        self.mouth = Mouth.Mouth(self)
        self.eyes = Eyes.Eyes(self)
        self.nose = Nose.Nose(self)
        self.ear = Ear.Ear(self)

    def unload(self):
        self.shape.unload()
        self.mouth.unload()
        self.eyes.unload()
        self.nose.unload()
        self.ear.unload()
        del self.shape
        del self.mouth
        del self.eyes
        del self.nose
        del self.ear
        del self.main
        del self.parent
        del self.avatar

    def assignAvatar(self, avatar):
        self.avatar = avatar
        self.shape.avatar = avatar
        self.mouth.avatar = avatar
        self.eyes.avatar = avatar
        self.nose.avatar = avatar
        self.ear.avatar = avatar

    def restore(self):
        self.notify.debug('restoring dna')
        self.shape.restore()
        self.mouth.restore()
        self.eyes.restore()
        self.nose.restore()
        self.ear.restore()
        self.shape.loadExtraArgs()
        self.mouth.loadExtraArgs()
        self.eyes.loadExtraArgs()
        self.nose.loadExtraArgs()
        self.ear.loadExtraArgs()

    def save(self):
        self.shape.saveDNA()
        self.mouth.saveDNA()
        self.eyes.saveDNA()
        self.nose.saveDNA()
        self.ear.saveDNA()