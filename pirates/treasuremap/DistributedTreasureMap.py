# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.treasuremap.DistributedTreasureMap
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from pirates.uberdog.DistributedInventory import DistributedInventory
from pirates.quest.QuestHolder import QuestHolder
from pirates.piratesbase import PiratesGlobals
from pirates.piratesgui import PiratesGuiGlobals
from pirates.world import GameTypeGlobals

class DistributedTreasureMap(DistributedObject.DistributedObject, DistributedInventory, QuestHolder):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('TreasureMapManager')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        DistributedInventory.__init__(self, cr)
        QuestHolder.__init__(self)
        self.mapId = None
        self.__enabled = 1
        self.quests = []
        self.tmName = 'treasureMapCove'
        return

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        self.addInterest(2, self.uniqueName('TreasureMap'))
        GameTypeGlobals.GameTypes[PiratesGlobals.GAME_TYPE_TM]['hidden'] = False
        messenger.send(localAvatar.guiMgr.lookoutPage.getItemChangeMsg())

    def delete(self):
        DistributedObject.DistributedObject.delete(self)

    def requestTreasureMapGo(self, quick=True):
        if quick:

            def teleportConfirm(confirmed):
                if confirmed:
                    if base.localAvatar.guiMgr.crewHUD.crew:
                        base.localAvatar.guiMgr.crewHUD.leaveCrew()
                    self.teleportStarted()

            localAvatar.confirmTeleport(teleportConfirm, feedback=True)
        else:
            localAvatar.guiMgr.showLookoutPanel()
            localAvatar.guiMgr.lookoutPage.displayLookout(gameStyle=self.mapId, inviteOptions=[PiratesGlobals.LOOKOUT_INVITE_CREW], additionalOptions=[[str(GameTypeGlobals.GAME_OPTION_TM_ID), str(self.getDoId())]])

    def teleportStarted(self):
        base.cr.loadingScreen.showTarget()
        self.sendRequestStart()

    def sendRequestStart(self):
        self.sendUpdate('requestStart', [5])

    def setObjectiveIds(self, questIds):
        self.quests = questIds

    def getOptions(self):
        tmInfo = PiratesGlobals.DYNAMIC_GAME_STYLE_PROPS[PiratesGlobals.GAME_TYPE_TM].get(self.mapId)
        numPlayersList = []
        numPlayers = tmInfo.get('NumPlayers')
        if numPlayers:
            for currPlayer in range(numPlayers[0], numPlayers[1] + 1):
                numPlayersList.append(str(currPlayer))

        if numPlayersList:
            return {'options': {GameTypeGlobals.GAME_OPTION_MIN_PLAYERS: [PiratesGuiGlobals.UIItemType_ListItem, numPlayersList]}}
        else:
            return {'options': {}}

    def setMapId(self, mapId):
        self.mapId = mapId

    def setIsEnabled(self, enabled):
        self.__enabled = enabled

    def getIsEnabled(self):
        return self.__enabled