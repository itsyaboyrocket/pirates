# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.creature.Rooster
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from pirates.creature.Animal import Animal

class Rooster(Animal):
    __module__ = __name__
    ModelInfo = ('models/char/rooster_hi', 'models/char/rooster_')
    SfxNames = dict(Animal.SfxNames)
    SfxNames.update({})
    AnimList = (
     ('idle', 'idle'), ('walk', 'walk'), ('run', 'run'), ('fly', 'fly'), ('crow', 'crow'), ('peck', 'peck'))

    class AnimationMixer(Animal.AnimationMixer):
        __module__ = __name__
        notify = DirectNotifyGlobal.directNotify.newCategory('RoosterAnimationMixer')
        LOOP = Animal.AnimationMixer.LOOP
        ACTION = Animal.AnimationMixer.ACTION
        AnimRankings = {'idle': (LOOP['LOOP'],), 'walk': (LOOP['LOOP'],), 'run': (LOOP['LOOP'],), 'fly': (LOOP['LOOP'],), 'crow': (ACTION['ACTION'],), 'peck': (ACTION['ACTION'],)}

    @classmethod
    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam', (('idle', 1.0), ('walk', 1.0), ('run', 1.0), ('walk', -1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('fly', 1.0), ('fly', 1.0)))
        cls.setupAnimInfoState('WaterRoam', (('idle', 1.0), ('walk', 1.0), ('run', 1.0), ('walk', -1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('run', 1.0), ('fly', 1.0), ('fly', 1.0)))

    def __init__(self):
        Animal.__init__(self)
        if not Rooster.sfx:
            for name in Rooster.SfxNames:
                Rooster.sfx[name] = loadSfx(Rooster.SfxNames[name])

        self.generateCreature()