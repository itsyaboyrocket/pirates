# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.creature.Crab
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from pirates.creature.Creature import Creature
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx

class Crab(Creature):
    __module__ = __name__
    ModelInfo = ('models/char/crab_hi', 'models/char/crab_')
    SfxNames = dict(Creature.SfxNames)
    SfxNames.update({'pain': SoundGlobals.SFX_MONSTER_CRAB_PAIN, 'death': SoundGlobals.SFX_MONSTER_CRAB_DEATH})
    sfx = {}
    AnimList = (
     ('idle', 'idle'), ('walk', 'walk'), ('attack_left', 'attack_left'), ('attack_right', 'attack_right'), ('attack_both', 'attack_both'), ('pain', 'pain'), ('death', 'death'))

    class AnimationMixer(Creature.AnimationMixer):
        __module__ = __name__
        notify = DirectNotifyGlobal.directNotify.newCategory('CrabAnimationMixer')
        LOOP = Creature.AnimationMixer.LOOP
        ACTION = Creature.AnimationMixer.ACTION
        AnimRankings = {'idle': (LOOP['LOOP'],), 'walk': (LOOP['LOOP'],), 'attack_left': (ACTION['ACTION'],), 'attack_right': (ACTION['ACTION'],), 'attack_both': (ACTION['ACTION'],), 'pain': (ACTION['ACTION'],), 'death': (ACTION['MOVIE'],)}

    @classmethod
    def setupAnimInfo(cls):
        cls.setupAnimInfoState('LandRoam', (('idle', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', -1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('idle', 1.0), ('idle', 1.0)))
        cls.setupAnimInfoState('WaterRoam', (('idle', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', -1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('walk', 1.0), ('idle', 1.0), ('idle', 1.0)))

    def __init__(self):
        Creature.__init__(self)
        if not Crab.sfx:
            for name in Crab.SfxNames:
                Crab.sfx[name] = loadSfx(Crab.SfxNames[name])

        self.nametagOffset = 1.6
        self.generateCreature()
        self.headNode = self.find('**/def_root')