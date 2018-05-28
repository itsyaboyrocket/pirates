# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesbase.DistributedTimeOfDayManager
from direct.distributed.DistributedObject import DistributedObject
from direct.distributed.ClockDelta import globalClockDelta
from TimeOfDayManager import TimeOfDayManager
from pirates.piratesbase import TODGlobals
import time

class DistributedTimeOfDayManager(DistributedObject, TimeOfDayManager):
    __module__ = __name__
    from direct.directnotify import DirectNotifyGlobal
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedTimeOfDayManager')

    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        TimeOfDayManager.__init__(self)
        self.skyEnabled = base.config.GetBool('enable-sky', 1)
        self.syncEnabled = True
        self.isPaused = 0
        if not base.win.getGsg().isHardware():
            self.skyEnabled = False
        if not self.skyEnabled:
            self.skyGroup.stash()
        self.clockSyncData = None
        self.accept('gotTimeSync', self.handleClockSync)
        return

    def generate(self):
        self.cr.timeOfDayManager = self
        DistributedObject.generate(self)

    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        self.startTodToggles()

    def disable(self):
        TimeOfDayManager.disable(self)
        DistributedObject.disable(self)
        self.ignoreAll()
        if self.cr.timeOfDayManager == self:
            self.cr.timeOfDayManager = None
        return

    def delete(self):
        TimeOfDayManager.delete(self)
        DistributedObject.delete(self)

    def enableSync(self, value):
        self.syncEnabled = value
        if self.syncEnabled:
            self.sendUpdate('requestSync')

    def setIsPaused(self, isPaused):
        self.isPaused = isPaused

    def setEnvSubs(self, subList):
        for subEntry in subList:
            self.addEnvSub(subEntry[0], subEntry[1], subEntry[2])

    def handleClockSync(self, task=None):
        if self.clockSyncData:
            self.syncTOD(self.clockSyncData[0], self.clockSyncData[1], self.clockSyncData[2], self.clockSyncData[3])

    def syncTOD(self, cycleType, cycleSpeed, startingNetTime, timeOffset):
        self.clockSyncData = (
         cycleType, cycleSpeed, startingNetTime, timeOffset)
        if not self.syncEnabled:
            return
        needMessage = 0
        if self.cycleType != cycleType:
            needMessage = 1
        if self.cycleSpeed != cycleSpeed:
            needMessage = 1
        self.cycleType = cycleType
        self.startingServerTime = globalClockDelta.networkToLocalTime(startingNetTime, bits=32)
        self.timeOffset = timeOffset
        self.cycleSpeed = cycleSpeed
        self.enterInitState()
        if needMessage:
            messenger.send('TOD_CYCLE_CHANGE')
        self.restartTimeOfDayMethod()
        self.processTimeOfDayToggles()

    def setMoonPhaseChange(self, fromCurrent, startPhase, targetPhase, targetTime):
        currentTime = globalClock.getFrameTime()
        timeStamp = globalClockDelta.networkToLocalTime(targetTime, bits=32)
        if timeStamp < currentTime:
            return
        else:
            self.animateMoon(fromCurrent, startPhase, targetPhase, timeStamp - currentTime)

    def setMoonAnimation(self, startTime, keyList):
        currentTime = globalClock.getFrameTime()
        timeStamp = globalClockDelta.networkToLocalTime(targetTime, bits=32)
        relativeStartTime = currentTime - timeStamp

    def setMoonJolly(self, isJolly):
        self.switchJollyMoon(isJolly)