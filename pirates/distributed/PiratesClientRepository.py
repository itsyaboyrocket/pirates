# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.distributed.PiratesClientRepository
import types, random, gc, time, __builtin__
base.loadingScreen.beginStep('PCR', 20, 15)
from direct.showbase.ShowBaseGlobal import *
base.loadingScreen.tick()
from direct.distributed.ClockDelta import *
base.loadingScreen.tick()
from direct.gui.DirectGui import *
base.loadingScreen.tick()
from pandac.PandaModules import *
base.loadingScreen.tick()
from libotp import NametagGlobals
base.loadingScreen.tick()
from direct.interval.IntervalGlobal import *
base.loadingScreen.tick()
from direct.showbase.EventGroup import EventGroup
base.loadingScreen.tick()
from direct.showbase.PythonUtil import report
base.loadingScreen.tick()
from pirates.piratesbase.PiratesGlobals import *
base.loadingScreen.tick()
from PiratesMsgTypes import *
base.loadingScreen.tick()
from direct.directnotify.DirectNotifyGlobal import directNotify
base.loadingScreen.tick()
from direct.fsm import ClassicFSM
base.loadingScreen.tick()
from direct.fsm import State
base.loadingScreen.tick()
from direct.task import Task
base.loadingScreen.tick()
from direct.distributed.PyDatagram import PyDatagram
base.loadingScreen.tick()
from direct.distributed.PyDatagramIterator import PyDatagramIterator
base.loadingScreen.tick()
from direct.distributed import DistributedSmoothNode
base.loadingScreen.tick()
from direct.distributed.InterestWatcher import InterestWatcher
base.loadingScreen.tick()
from direct.distributed import DoInterestManager
from direct.distributed.ClientRepositoryBase import ClientRepositoryBase
from otp.distributed.OTPClientRepository import OTPClientRepository
from otp.distributed import PotentialShard
from otp.distributed.PotentialAvatar import PotentialAvatar
from otp.distributed import DistributedDistrict
from otp.distributed import OtpDoGlobals
from otp.otpbase import OTPGlobals
from otp.friends import FriendSecret
from otp.uberdog.AccountDetailRecord import AccountDetailRecord, SubDetailRecord
from otp.otpgui import OTPDialog
from pirates.login.AvatarChooser import AvatarChooser
from pirates.makeapirate.MakeAPirate import MakeAPirate
from pirates.pirate import HumanDNA
from pirates.pirate import MasterHuman, Human
from pirates.pirate import AvatarTypes
from pirates.pirate.LocalPirate import LocalPirate
from pirates.pirate import DistributedPlayerPirate
from pirates.piratesbase import PLocalizer
from pirates.world import WorldGlobals
from pirates.world.DistributedGameArea import DistributedGameArea
from pirates.battle import BattleManager
from pirates.battle import DistributedBattleNPC
from pirates.battle import CombatAnimations
from pirates.band import DistributedBandMember
from pirates.cutscene import Cutscene
import PlayGame
from ShardFSM import ShardFSM
from pirates.piratesbase import PiratesGlobals
from pirates.battle import DistributedBattleNPC
from pirates.ship import DistributedSimpleShip
from pirates.interact import InteractionManager
from pirates.piratesbase import UniqueIdManager
from pirates.piratesgui.DialMeter import DialMeter
from pirates.piratesgui import PiratesGuiGlobals
from pirates.uberdog.UberDogGlobals import InventoryType
from pirates.reputation import ReputationGlobals
from pirates.piratesbase import PLocalizer
from pirates.piratesbase import LoadingScreen
from pirates.ai import NewsManager
from pirates.makeapirate import PCPickANamePattern
from pirates.coderedemption.CodeRedemption import CodeRedemption
from pirates.minigame import PotionGlobals
from pirates.battle.WeaponConstants import *
base.loadingScreen.endStep('PCR')
from pirates.quest import QuestLadderDynMap
from pirates.quest.QuestLadderDependency import QuestLadderDependency
from pirates.quest.QuestChoiceDynMap import QuestChoiceDynMap
from pirates.npc import NPCManager
from pirates.audio import SoundGlobals
from pirates.audio.SoundGlobals import loadSfx

class bp:
    __module__ = __name__
    loginCfg = bpdb.bpGroup(iff=True, cfg='loginCfg', static=1)


class PiratesClientRepository(OTPClientRepository):
    __module__ = __name__
    notify = directNotify.newCategory('PiratesClientRepository')
    SupportTutorial = 0
    GameGlobalsId = OTP_DO_ID_PIRATES
    StopVisibilityEvent = 'pirates-stop-visibility'

    def __init__(self, serverVersion, launcher=None):
        self.loadingScreen = base.loadingScreen
        self.loadingScreen.parent = self
        self.accept('connectionIssue', self.loadingScreen.hide)
        self.accept('connectionRetrying', self.loadingScreen.show)
        OTPClientRepository.__init__(self, serverVersion, launcher, playGame=PlayGame.PlayGame)
        self.createAvatarClass = DistributedPlayerPirate.DistributedPlayerPirate
        self.tradeManager = None
        self.pvpManager = None
        self.avatarManager = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_PIRATES_AVATAR_MANAGER, 'DistributedAvatarManager')
        self.chatManager = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_CHAT_MANAGER, 'DistributedChatManager')
        self.crewMatchManager = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_PIRATES_CREW_MATCH_MANAGER, 'DistributedCrewMatchManager')
        self.avatarFriendsManager = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_AVATAR_FRIENDS_MANAGER, 'PCAvatarFriendsManager')
        self.playerFriendsManager = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_PLAYER_FRIENDS_MANAGER, 'PCPlayerFriendsManager')
        self.guildManager = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_PIRATES_GUILD_MANAGER, 'PCGuildManager')
        self.speedchatRelay = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_PIRATES_SPEEDCHAT_RELAY, 'PiratesSpeedchatRelay')
        self.shipLoader = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_PIRATES_SHIP_MANAGER, 'DistributedShipLoader')
        self.travelAgent = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_PIRATES_TRAVEL_AGENT, 'DistributedTravelAgent')
        base.loadingScreen.tick()
        self.matchMaker = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_PIRATES_MATCH_MAKER, 'DistributedMatchMaker')
        base.loadingScreen.tick()
        self.codeRedemption = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_PIRATES_CODE_REDEMPTION, 'CodeRedemption')
        base.loadingScreen.tick()
        self.settingsMgr = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_PIRATES_SETTINGS_MANAGER, 'PiratesSettingsMgr')
        self.statusDatabase = self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_STATUS_DATABASE, 'StatusDatabase')
        self.wantSeapatch = base.config.GetBool('want-seapatch', 1)
        self.wantSpecialEffects = base.config.GetBool('want-special-effects', 1)
        self.wantMakeAPirate = base.config.GetBool('wantMakeAPirate', 0)
        self.forceTutorial = base.config.GetBool('force-tutorial', 0)
        self.skipTutorial = base.config.GetBool('skip-tutorial', 0)
        self.tutorialObject = None
        self.avChoiceDoneEvent = None
        self.avChoice = None
        self.avCreate = None
        self.currentCutscene = None
        self.activeWorld = None
        self.teleportMgr = None
        self.treasureMap = None
        self.newsManager = None
        self.distributedDistrict = None
        self.district = None
        self.profileMgr = None
        self.battleMgr = BattleManager.BattleManager(self)
        self.combatAnims = CombatAnimations.CombatAnimations()
        self.interactionMgr = InteractionManager.InteractionManager()
        self.currCamParent = None
        self.uidMgr = UniqueIdManager.UniqueIdManager(self)
        self.fakeMSP = None
        self.questDynMap = QuestLadderDynMap.QuestLadderDynMap()
        self.questDependency = QuestLadderDependency()
        self.questChoiceSibsMap = QuestChoiceDynMap()
        base.loadingScreen.beginStep('MasterHumans', 52, 45)
        self.humanHigh = [MasterHuman.MasterHuman(), MasterHuman.MasterHuman()]
        self.humanHigh[0].billboardNode.removeNode()
        self.humanHigh[1].billboardNode.removeNode()
        self.humanHigh[0].style = HumanDNA.HumanDNA('m')
        self.humanHigh[1].style = HumanDNA.HumanDNA('f')
        self.humanHigh[0].generateHuman('m')
        base.loadingScreen.tick()
        self.humanHigh[1].generateHuman('f')
        base.loadingScreen.tick()
        self.humanHigh[0].ignoreAll()
        self.humanHigh[1].ignoreAll()
        self.humanHigh[0].stopBlink()
        self.humanHigh[1].stopBlink()
        self.humanLow = [
         MasterHuman.MasterHuman(), MasterHuman.MasterHuman()]
        self.humanLow[0].billboardNode.removeNode()
        self.humanLow[1].billboardNode.removeNode()
        self.humanLow[0].style = HumanDNA.HumanDNA('m')
        self.humanLow[1].style = HumanDNA.HumanDNA('f')
        self.humanLow[0].generateHuman('m')
        base.loadingScreen.tick()
        self.humanLow[1].generateHuman('f')
        base.loadingScreen.tick()
        base.loadingScreen.endStep('MasterHumans')
        self.humanLow[0].ignoreAll()
        self.humanLow[1].ignoreAll()
        self.humanLow[0].stopBlink()
        self.humanLow[1].stopBlink()
        for i in range(2):
            self.humanLow[i]._Actor__sortedLODNames = [
             '500']
            del self.humanLow[i]._Actor__partBundleDict['2000']
            del self.humanLow[i]._Actor__partBundleDict['1000']
            self.humanLow[i].getLOD('2000').detachNode()
            self.humanLow[i].getLOD('1000').detachNode()
            self.humanLow[i].getLODNode().clearSwitches()
            self.humanLow[i].getLODNode().addSwitch(10000, 0)

        if base.options.getCharacterDetailSetting() == 0:
            self.human = self.humanLow
        else:
            self.human = self.humanHigh
        A = AvatarTypes
        del A
        self.preloadedCutscenes = {}
        self.defaultShard = 0
        NametagGlobals.setMasterArrowsOn(0)
        self._tagsToInterests = {}
        self._interestsToTags = {}
        self._worldStack = []
        if __dev__:
            __builtin__.go = self.getDo
            __builtin__.gov = self.getOwnerView
            import pdb
            __builtin__.trace = pdb.set_trace
            __builtin__.pm = pdb.pm
            self.effectTypes = {'damageSmoke': ['BlackSmoke'], 'damageFire': ['Fire'], 'cannonDeckFire': ['CannonSmokeSimple', 'CannonBlastSmoke'], 'cannonBSFire': ['MuzzleFlameBS', 'CannonSmokeSimpleBS', 'CannonBlastSmokeBS', 'GrapeshotEffectBS'], 'cannonHit': ['SimpleSmokeCloud', 'ExplosionFlip'], 'cannonSplash': ['CannonSplash']}
            self.effectToggles = {}
        self.cannonballCollisionDebug = 1
        self.npcManager = NPCManager.NPCManager()
        PotionGlobals.updatePotionBuffDuration(C_SUMMON_CHICKEN, config.GetInt('summon-duration-chicken', 300))
        PotionGlobals.updatePotionBuffDuration(C_SUMMON_MONKEY, config.GetInt('summon-duration-monkey', 300))
        PotionGlobals.updatePotionBuffDuration(C_SUMMON_WASP, config.GetInt('summon-duration-wasp', 300))
        PotionGlobals.updatePotionBuffDuration(C_SUMMON_DOG, config.GetInt('summon-duration-dog', 300))
        return

    def __repr__(self):
        return 'PiratesClientRepository'

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def gotoFirstScreen(self):
        base.loadingScreen.beginStep('PrepLogin', 9, 0.14)
        self.startReaderPollTask()
        self.startHeartbeat()
        base.loadingScreen.tick()
        self.loginFSM.request('login')
        base.loadingScreen.tick()
        base.loadingScreen.endStep('PrepLogin')

    def getActiveWorld(self):
        return self.activeWorld

    def preloadCutscene(self, name):
        if name not in self.preloadedCutscenes:
            newCutscene = Cutscene.Cutscene(self, name)
            self.preloadedCutscenes[name] = newCutscene

    def getPreloadedCutsceneInfo(self, name):
        return self.preloadedCutscenes.get(name)

    def cleanupPreloadedCutscene(self, name):
        plCutscene = self.preloadedCutscenes.get(name)
        if plCutscene:
            if not plCutscene.isEmpty():
                plCutscene.destroy()
            del self.preloadedCutscenes[name]

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def setActiveWorld(self, world):
        self.activeWorld = world

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def clearActiveWorld(self, world):
        if self.activeWorld and (world is self.activeWorld or self.activeWorld.isEmpty()):
            self.activeWorld = None
        return

    def getWaterHeight(self, node):
        if self.wantSeapatch:
            if self.activeWorld:
                water = self.activeWorld.getWater()
                return water and water.calcHeight(node=node)
        else:
            return 0.0

    def isOceanEnabled(self):
        if self.wantSeapatch and self.activeWorld and self.activeWorld.hasWater():
            return self.activeWorld.getWater().enabled
        return 0

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def enterChooseAvatar(self, avList):
        base.loadingScreen.beginStep('AvChooser', 14, 10)
        self.sendSetAvatarIdMsg(0)
        self.handler = self.handleMessageType
        if __dev__:
            bp.loginCfg()
            config_slot = base.config.GetInt('login-pirate-slot', -1)
            if config_slot >= 0:
                if len(avList) > 0:
                    config_subId = base.config.GetInt('login-pirate-subId', avList.keys()[0])
                    slots = avList.get(config_subId, [])
                    if config_slot in range(len(slots)):
                        potAv = slots[config_slot]
                        isinstance(potAv, PotentialAvatar) and base.cr.loadingScreen.hide()
                        ConfigVariableInt('login-pirate-slot').setValue(-1)
                        base.loadingScreen.endStep('AvChooser')
                        base.cr.avatarManager.sendRequestPlayAvatar(potAv.id, config_subId)
                        self.handleAvatarChoice('chose', config_subId, config_slot)
                        return
        self.avChoiceDoneEvent = 'avatarChooserDone'
        self.avChoice = AvatarChooser(self.loginFSM, self.avChoiceDoneEvent)
        base.loadingScreen.tick()
        self.avChoice.load()
        base.loadingScreen.tick()
        self.avChoice.enter()
        base.loadingScreen.tick()
        self.accept(self.avChoiceDoneEvent, self.__handleAvatarChooserDone)
        base.loadingScreen.endStep('AvChooser')
        base.cr.loadingScreen.hide()

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def __handleAvatarChooserDone(self, doneStatus):
        done = doneStatus['mode']
        if done == 'exit':
            self.notify.info('handleAvatarChooserDone: shutting down')
            self.loginFSM.request('shutdown')
            return
        subId, slot = self.avChoice.getChoice()
        self.avChoice.exit()
        self.handleAvatarChoice(done, subId, slot)

    def handleAvatarChoice(self, done, subId, slot):
        access = self.accountDetailRecord.subDetails[subId].subAccess
        base.setEmbeddedFrameMode(access)
        if done == 'chose':
            av = self.avList[subId][slot]
            if av.dna.getTutorial() < 3:
                self.tutorial = self.skipTutorial == 0 and 1
            else:
                self.tutorial = 0
            self.loadingScreen.beginStep('waitForAv')
            self.loginFSM.request('waitForSetAvatarResponse', [av])
        else:
            if done == 'create':
                self.loginFSM.request('createAvatar', [self.avList[subId], slot, subId])

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def exitChooseAvatar(self):
        self.handler = None
        if self.avChoice:
            self.avChoice.exit()
            self.avChoice.unload()
            self.avChoice = None
        if self.avChoiceDoneEvent:
            self.ignore(self.avChoiceDoneEvent)
            self.avChoiceDoneEvent = None
        return

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def enterCreateAvatar(self, avList, index, subId):
        self.handler = self.handleCreateAvatar
        if self.skipTutorial:
            self.tutorial = 0
            self.avCreate = MakeAPirate(avList, 'makeAPirateComplete', subId, index, self.isPaid())
            self.avCreate.load()
            self.avCreate.enter()
            self.accept('makeAPirateComplete', self.__handleMakeAPirate)
            self.accept('nameShopCreateAvatar', self.sendCreateAvatarMsg)
        else:
            self.tutorial = 1
            dna = HumanDNA.HumanDNA()
            newPotAv = PotentialAvatar(0, ['dbp', '', '', ''], dna, index, 0)
            self.avatarManager.sendRequestCreateAvatar(subId)
            self.accept('createdNewAvatar', self.handleAvatarCreated, [newPotAv])

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def handleAvatarCreated(self, newPotAv, avatarId, subId):
        newPotAv.id = avatarId
        self.loginFSM.request('waitForSetAvatarResponse', [newPotAv])

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def __handleMakeAPirate(self):
        done = self.avCreate.getDoneStatus()
        if done == 'cancel':
            self.avCreate.exit()
            self.loginFSM.request('chooseAvatar', [self.avList])
        else:
            if done == 'created':
                self.handleAvatarCreated(self.avCreate.newPotAv, self.avCreate.avId, self.avCreate.subId)
            else:
                self.notify.error('Invalid doneStatus from MakeAPirate: ' + str(done))

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def exitCreateAvatar(self):
        if self.skipTutorial:
            self.ignore('makeAPirateComplete')
            self.ignore('nameShopPost')
            self.ignore('nameShopCreateAvatar')
            self.avCreate.exit()
            self.avCreate.unload()
            self.avCreate = None
            self.handler = None
        self.ignore('createdNewAvatar')
        return

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def handleCreateAvatar(self, msgType, di):
        if msgType == CLIENT_CREATE_AVATAR_RESP:
            self.handleCreateAvatarResponseMsg(di)
        else:
            self.handleMessageType(msgType, di)

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def handleCreateAvatarResponseMsg(self, di):
        echoContext = di.getUint16()
        returnCode = di.getUint8()
        if returnCode == 0:
            self.avId = di.getUint32()
            newPotAv = PotentialAvatar(self.avId, [
             self.newName, '', '', ''], self.newDNA, self.newPosition, 1)
            self.loginFSM.request('waitForSetAvatarResponse', [newPotAv])
        else:
            self.notify.error('name rejected')

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def sendGetAvatarsMsg(self):
        self.accept('avatarListFailed', self.avatarListFailed)
        self.accept('avatarList', self.avatarList)
        self.avatarManager.sendRequestAvatarList()
        self.defaultShard = 0

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def avatarListFailed(self, reason):
        self.ignore('avatarListFailed')
        self.ignore('avatarList')
        dialogClass = OTPGlobals.getGlobalDialogClass()
        self.avatarListFailedBox = dialogClass(message=PLocalizer.CRAvatarListFailed, doneEvent='avatarListFailedAck', text_wordwrap=18, style=OTPDialog.Acknowledge)
        self.avatarListFailedBox.show()
        self.acceptOnce('avatarListFailedAck', self.__handleAvatarListFailedAck)

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def __handleAvatarListFailedAck(self):
        self.ignore('avatarListFailedAck')
        self.avatarListFailedBox.cleanup()
        self.loginFSM.request('shutdown')

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def avatarList(self, avatars):
        self.ignore('avatarListFailed')
        self.ignore('avatarList')
        self.avList = {}
        for subId, avData in avatars.items():
            data = []
            self.avList[subId] = data
            for av in avData:
                if av == OTPGlobals.AvatarSlotAvailable:
                    data.append(OTPGlobals.AvatarSlotAvailable)
                elif av == OTPGlobals.AvatarSlotUnavailable:
                    data.append(OTPGlobals.AvatarSlotUnavailable)
                elif av == OTPGlobals.AvatarPendingCreate:
                    data.append(OTPGlobals.AvatarPendingCreate)
                else:
                    avNames = [
                     av['name'], av['wishName'], '', '']
                    aName = 0
                    pa = PotentialAvatar(av['id'], avNames, av['dna'], av['slot'], aName, av['creator'] == self.accountDetailRecord.playerAccountId, av['shared'], av['online'], wishState=av['wishState'], wishName=av['wishName'], defaultShard=av['defaultShard'], lastLogout=av['lastLogout'])
                    data.append(pa)

        if self.loginFSM.getCurrentState().getName() == 'chooseAvatar':
            self.avChoice.updateAvatarList()
        else:
            self.loginFSM.request('chooseAvatar', [self.avList])

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def handleGetAvatarsRespMsg(self, di):
        pass

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def handleGetAvatarsResp2Msg(self, di):
        pass

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def handleAvatarResponseMsg(self, di):
        self.loadingScreen.endStep('waitForAv')
        avatarId = di.getUint32()
        returnCode = di.getUint8()
        if returnCode == 0:
            self.loadingScreen.show(waitForLocation=True, expectedLoadScale=4)
            self.loadingScreen.beginStep('LocalAvatar', 36, 120)
            localAvatar = LocalPirate(self)
            localAvatar.dclass = self.dclassesByName['DistributedPlayerPirate']
            localAvatar.doId = avatarId
            self.localAvatarDoId = avatarId
            self.doId2do[avatarId] = localAvatar
            localAvatar.setLocation(parentId=None, zoneId=None)
            localAvatar.generate()
            localAvatar.updateAllRequiredFields(localAvatar.dclass, di)
            self.loadingScreen.endStep('LocalAvatar')
            self.loginFSM.request('playingGame')
        else:
            self.notify.error('Bad avatar: return code %d' % returnCode)
        return

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def enterWaitForDeleteAvatarResponse(self, potentialAvatar):
        raise StandardError, 'This should be handled within AvatarChooser.py'

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def exitWaitForDeleteAvatarResponse(self):
        raise StandardError, 'This should be handled within AvatarChooser.py'

    @report(types=['args', 'deltaStamp', 'module'], dConfigParam='teleport')
    def enterPlayingGame(self):
        OTPClientRepository.enterPlayingGame(self)
        self.doDetectLeaks = False
        self.shardFSM = ShardFSM(self)
        if localAvatar.style.getTutorial() < PiratesGlobals.TUT_MET_JOLLY_ROGER:
            not self.skipTutorial and self.travelAgent.d_requestTutorialTeleport()
        else:
            if localAvatar.onWelcomeWorld:
                not self.defaultShard and self.travelAgent.d_requestWelcomeWorldTeleport()
            else:
                if self.defaultShard:
                    self.travelAgent.d_requestLoginTeleport(self.defaultShard)
                else:
                    if self.avPlayedRecently:
                        self.travelAgent.d_requestLoginTeleport(localAvatar.defaultShard)
                    else:
                        self.travelAgent.d_requestLoginTeleport()

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def playingGameLocReceived(self, shardId, zoneId):
        self.gameFSM.request('waitOnEnterResponses', [
         shardId, zoneId, zoneId, -1])

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def exitPlayingGame(self):
        self.shardFSM.request('Off')
        ivalMgr.interrupt()
        base.ambientMgr.delete()
        base.musicMgr.delete()
        messenger.send('clientLogout')
        for doId, obj in self.doId2do.items():
            if not isinstance(obj, LocalPirate):
                if not isinstance(obj, DistributedDistrict.DistributedDistrict):
                    hasattr(self, 'disableObject') and self.disableObject(doId)

        camera.reparentTo(render)
        camera.setPos(0, 0, 0)
        camera.setHpr(0, 0, 0)
        base.transitions.noTransitions()
        OTPClientRepository.exitPlayingGame(self)
        self.detectLeaks(okTasks=['physics-avatar', 'memory-monitor-task', 'multitexFlatten'], okEvents=['destroy-ToontownLoadingScreenTitle', 'destroy-ToontownLoadingScreenTip', 'destroy-ToontownLoadingScreenWaitBar', PiratesGlobals.LogoutHotkey, PiratesGlobals.HideGuiHotkey, PiratesGlobals.OptionsHotkey, 'close_main_window', 'open_main_window', 'texture_state_changed', 'connectionIssue', 'connectionRetrying', self.getConnectedEvent()])

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def enterTutorialQuestion(self, hoodId, zoneId, avId):
        self.__requestTutorial(hoodId, zoneId, avId)

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def handleTutorialQuestion(self, msgType, di):
        if msgType == CLIENT_CREATE_OBJECT_REQUIRED:
            self.handleGenerateWithRequired(di)
        else:
            if msgType == CLIENT_CREATE_OBJECT_REQUIRED_OTHER:
                self.handleGenerateWithRequiredOther(di)
            else:
                if msgType == CLIENT_OBJECT_UPDATE_FIELD:
                    self.handleUpdateField(di)
                else:
                    if msgType == CLIENT_OBJECT_DISABLE:
                        self.handleDisable(di)
                    else:
                        if msgType == CLIENT_OBJECT_DISABLE_OWNER:
                            self.handleDisableOwner(di)
                        else:
                            if msgType == CLIENT_OBJECT_DELETE_RESP:
                                self.handleDelete(di)
                            else:
                                if msgType == CLIENT_GET_AVATAR_DETAILS_RESP:
                                    self.handleGetAvatarDetailsResp(di)
                                else:
                                    self.handleUnexpectedMsgType(msgType, di)

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def exitTutorialQuestion(self):
        self.handler = None
        self.handlerArgs = None
        self.ignore('startTutorial')
        taskMgr.remove('waitingForTutorial')
        return

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def __requestTutorial(self, hoodId, zoneId, avId):
        self.acceptOnce('startTutorial', self.__handleStartTutorial, [
         avId])
        messenger.send('requestTutorial')

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def __handleStartTutorial(self, avId, zoneId):
        self.gameFSM.request('playGame', [Tutorial, zoneId, avId])

    @report(types=['args', 'deltaStamp', 'module'], dConfigParam='teleport')
    def enterWaitOnEnterResponses(self, shardId, hoodId, zoneId, avId):
        self.cleanGameExit = False
        self.handler = self.handleWaitOnEnterResponses
        self.handlerArgs = {'hoodId': hoodId, 'zoneId': zoneId, 'avId': avId}
        self.distributedDistrict = self.activeDistrictMap.get(shardId)
        self.waitForDatabaseTimeout(requestName='WaitOnEnterResponses')
        self.handleSetShardComplete()

    @report(types=['args', 'deltaStamp', 'module'], dConfigParam='teleport')
    def handleSetShardComplete(self):
        hoodId = self.handlerArgs['hoodId']
        zoneId = self.handlerArgs['zoneId']
        avId = self.handlerArgs['avId']
        self.uberZoneInterest = self.addInterest(base.localAvatar.getDefaultShard(), OTPGlobals.UberZone, 'uberZone', 'uberZoneInterestComplete')
        self.acceptOnce('uberZoneInterestComplete', self.uberZoneInterestComplete)
        self.waitForDatabaseTimeout(20, requestName='waitingForUberZone')

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def gotTimeSync(self):
        self.notify.info('gotTimeSync')
        self.ignore('gotTimeSync')
        self.__gotTimeSync = 1
        self.moveOnFromUberZone()

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def moveOnFromUberZone(self):
        if not self.__gotTimeSync:
            self.notify.info('Waiting for time sync.')
            return
        hoodId = self.handlerArgs['hoodId']
        zoneId = self.handlerArgs['zoneId']
        avId = self.handlerArgs['avId']

    def enterGameOff(self):
        pass

    def exitGameOff(self):
        pass

    def getFriendFlags(self, doId):
        return 0

    def isFriend(self, doId):
        return self.avatarFriendsManager.isFriend(doId) or self.playerFriendsManager.isFriend(doId)

    def isFriendOnline(self, doId):
        info = self.identifyFriend(doId)
        if info:
            return info.isOnline()
        else:
            return False

    def findPlayerIdForAvId(self, avId):
        playerId = None
        playerId = self.playerFriendsManager.findPlayerIdFromAvId(avId)
        if not playerId:
            info = self.avatarFriendsManager.getFriendInfo(avId)
            if info:
                playerId = info.playerId
        if not playerId:
            avatar = self.doId2do.get(avId)
            if avatar:
                playerId = avatar.DISLid
        return playerId

    def identifyFriend(self, doId):
        pfm = self.playerFriendsManager
        afm = self.avatarFriendsManager
        pId = pfm.findPlayerIdFromAvId(doId)
        if pfm.isFriend(pId) or afm.isFriend(doId):
            return pfm.getFriendInfo(pId) or afm.getFriendInfo(doId)

    def identifyAvatar--- This code section failed: ---

1143       0  LOAD_FAST             0  'self'
           3  LOAD_ATTR             1  'doId2do'
           6  LOAD_ATTR             2  'get'
           9  LOAD_FAST             1  'doId'
          12  CALL_FUNCTION_1       1  None
          15  JUMP_IF_TRUE        155  'to 173'
          18  POP_TOP          
          19  LOAD_FAST             0  'self'
          22  LOAD_ATTR             4  'avatarFriendsManager'
          25  LOAD_ATTR             5  'getFriendInfo'
          28  LOAD_FAST             1  'doId'
          31  CALL_FUNCTION_1       1  None
          34  JUMP_IF_TRUE        136  'to 173'
          37  POP_TOP          
          38  LOAD_FAST             0  'self'
          41  LOAD_ATTR             6  'playerFriendsManager'
          44  LOAD_ATTR             7  'findPlayerInfoFromAvId'
          47  LOAD_FAST             1  'doId'
          50  CALL_FUNCTION_1       1  None
          53  JUMP_IF_TRUE        117  'to 173'
          56  POP_TOP          
          57  LOAD_FAST             0  'self'
          60  LOAD_ATTR             8  'guildManager'
          63  LOAD_ATTR             9  'getMemberInfo'
          66  LOAD_FAST             1  'doId'
          69  CALL_FUNCTION_1       1  None
          72  JUMP_IF_TRUE         98  'to 173'
          75  POP_TOP          
          76  LOAD_GLOBAL          10  'DistributedBandMember'
          79  LOAD_ATTR            10  'DistributedBandMember'
          82  LOAD_ATTR            11  'areSameCrew'
          85  LOAD_GLOBAL          12  'localAvatar'
          88  LOAD_ATTR             3  'doId'
          91  LOAD_FAST             1  'doId'
          94  CALL_FUNCTION_2       2  None
          97  JUMP_IF_FALSE        19  'to 119'
         100  POP_TOP          
         101  LOAD_GLOBAL          10  'DistributedBandMember'
         104  LOAD_ATTR            10  'DistributedBandMember'
         107  LOAD_ATTR            13  'getBandMember'
         110  LOAD_FAST             1  'doId'
         113  CALL_FUNCTION_1       1  None
       116_0  COME_FROM            97  '97'
         116  JUMP_IF_TRUE         54  'to 173'
         119  POP_TOP          
         120  LOAD_FAST             0  'self'
         123  LOAD_ATTR             8  'guildManager'
         126  LOAD_ATTR             9  'getMemberInfo'
         129  LOAD_FAST             1  'doId'
         132  CALL_FUNCTION_1       1  None
         135  JUMP_IF_TRUE         35  'to 173'
         138  POP_TOP          
         139  LOAD_GLOBAL          14  'base'
         142  LOAD_ATTR            15  'talkAssistant'
         145  LOAD_ATTR            16  'getHandle'
         148  LOAD_FAST             1  'doId'
         151  CALL_FUNCTION_1       1  None
         154  JUMP_IF_TRUE         16  'to 173'
         157  POP_TOP          
         158  LOAD_FAST             0  'self'
         161  LOAD_ATTR            17  'crewMatchManager'
         164  LOAD_ATTR            16  'getHandle'
         167  LOAD_FAST             1  'doId'
         170  CALL_FUNCTION_1       1  None
       173_0  COME_FROM           154  '154'
       173_1  COME_FROM           135  '135'
       173_2  COME_FROM           116  '116'
       173_3  COME_FROM            72  '72'
       173_4  COME_FROM            53  '53'
       173_5  COME_FROM            34  '34'
       173_6  COME_FROM            15  '15'
         173  RETURN_VALUE     
         174  JUMP_FORWARD        153  'to 330'
         177  POP_TOP          

1154     178  LOAD_FAST             1  'doId'
         181  LOAD_FAST             0  'self'
         184  LOAD_ATTR             1  'doId2do'
         187  COMPARE_OP            6  'in'
         190  JUMP_IF_FALSE        15  'to 208'
         193  POP_TOP          

1155     194  LOAD_FAST             0  'self'
         197  LOAD_ATTR             1  'doId2do'
         200  LOAD_FAST             1  'doId'
         203  BINARY_SUBSCR    
         204  RETURN_VALUE     
         205  JUMP_FORWARD        122  'to 330'
       208_0  COME_FROM           190  '190'
         208  POP_TOP          

1156     209  LOAD_FAST             0  'self'
         212  LOAD_ATTR            18  'identifyFriend'
         215  LOAD_FAST             1  'doId'
         218  CALL_FUNCTION_1       1  None
         221  JUMP_IF_FALSE        17  'to 241'
         224  POP_TOP          

1157     225  LOAD_FAST             0  'self'
         228  LOAD_ATTR            18  'identifyFriend'
         231  LOAD_FAST             1  'doId'
         234  CALL_FUNCTION_1       1  None
         237  RETURN_VALUE     
         238  JUMP_FORWARD         89  'to 330'
       241_0  COME_FROM           221  '221'
         241  POP_TOP          

1158     242  LOAD_GLOBAL          10  'DistributedBandMember'
         245  LOAD_ATTR            10  'DistributedBandMember'
         248  LOAD_ATTR            11  'areSameCrew'
         251  LOAD_GLOBAL          12  'localAvatar'
         254  LOAD_ATTR             3  'doId'
         257  LOAD_FAST             1  'doId'
         260  CALL_FUNCTION_2       2  None
         263  JUMP_IF_FALSE        20  'to 286'
         266  POP_TOP          

1159     267  LOAD_GLOBAL          10  'DistributedBandMember'
         270  LOAD_ATTR            10  'DistributedBandMember'
         273  LOAD_ATTR            13  'getBandMember'
         276  LOAD_FAST             1  'doId'
         279  CALL_FUNCTION_1       1  None
         282  RETURN_VALUE     
         283  JUMP_FORWARD         44  'to 330'
       286_0  COME_FROM           263  '263'
         286  POP_TOP          

1160     287  LOAD_FAST             0  'self'
         290  LOAD_ATTR             8  'guildManager'
         293  LOAD_ATTR            19  'isInGuild'
         296  LOAD_FAST             1  'doId'
         299  CALL_FUNCTION_1       1  None
         302  JUMP_IF_FALSE        20  'to 325'
         305  POP_TOP          

1161     306  LOAD_FAST             0  'self'
         309  LOAD_ATTR             8  'guildManager'
         312  LOAD_ATTR             9  'getMemberInfo'
         315  LOAD_FAST             1  'doId'
         318  CALL_FUNCTION_1       1  None
         321  RETURN_VALUE     
         322  JUMP_FORWARD          5  'to 330'
       325_0  COME_FROM           302  '302'
         325  POP_TOP          

1163     326  LOAD_CONST            0  None
         329  RETURN_VALUE     
       330_0  COME_FROM           322  '322'
       330_1  COME_FROM           283  '283'
       330_2  COME_FROM           238  '238'
       330_3  COME_FROM           205  '205'
       330_4  COME_FROM           174  '174'
         330  LOAD_CONST            0  None
         333  RETURN_VALUE     

Parse error at or near `LOAD_FAST' instruction at offset 178

    def identifyPlayer(self, playerId):
        return self.playerFriendsManager.getFriendInfo(playerId)

    def setViewpoint(self, obj, useOobe=1):
        wasOobe = 0
        try:
            if base.oobeMode is 1:
                wasOobe = 1
                base.oobe()
        except:
            pass
        else:
            obj.setViewpoint()
            if useOobe == 1 or wasOobe == 1:
                base.oobe()

    def getCycleCamTaskName(self):
        return 'cycleCam' + str(id(self))

    def cycleCameraObjects(self, delay, objType, task):
        currParentFound = 0
        newObj = None
        currObj = None
        searches = 0
        while newObj is None and searches < 2:
            for currId in self.doId2do:
                currObj = self.doId2do.get(currId)
                if isinstance(currObj, objType):
                    if self.currCamParent is None:
                        newObj = currObj
                        break
                    elif self.currCamParent == currId:
                        currParentFound = 1
                        continue
                    elif currParentFound:
                        newObj = currObj
                        break

            searches = searches + 1

        if newObj is not None:
            self.currCamParent = newObj.getDoId()
            self.setViewpoint(newObj, 0)
            print 'reparenting camera to object %d' % self.currCamParent
        else:
            print 'problem finding a new camera parent, will try again'
        if task:
            task.delayTime = delay
        return Task.again

    def stopCycleCamera(self):
        taskMgr.remove(self.getCycleCamTaskName())

    def handleObjDelete(self, obj):
        if self.currCamParent == obj.getDoId():
            self.currCamParent = None
        return

    def toggleAutoCamReparent(self, word):
        if taskMgr.hasTaskNamed(self.getCycleCamTaskName()):
            self.stopCycleCamera()
            return
        delay = 10
        args = word.split()
        if len(args) >= 2:
            delay = int(args[1])
        if word == '~ccNPC':
            objType = DistributedBattleNPC.DistributedBattleNPC
        else:
            objType = DistributedSimpleShip.DistributedSimpleShip
        taskMgr.doMethodLater(0.5, self.cycleCameraObjects, self.getCycleCamTaskName(), extraArgs=[delay, objType], appendTask=True)

    def performCamReparent(self, objDoId=None):
        selectedObj = localAvatar.currentTarget
        if objDoId:
            obj = self.doId2do[objDoId]
            if obj:
                if self.currCamParent is not obj:
                    self.setViewpoint(obj)
                    return
            self.currCamParent = selectedObj and self.currCamParent is None and selectedObj.getDoId()
            self.setViewpoint(selectedObj)
        else:
            if self.currCamParent is not None:
                if selectedObj is None or selectedObj.compareTo(camera.getParent()) is 0:
                    camera.reparentTo(base.localAvatar)
                    self.currCamParent = None
                    try:
                        if base.oobeMode is 1:
                            base.oobe()
                    except:
                        pass

                else:
                    self.setViewpoint(selectedObj)
        return

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def enterCloseShard(self, loginState=None):
        if loginState == 'waitForAvatarList':
            self.loadingScreen.showTarget(pickapirate=True)
        else:
            if loginState == 'shutdown':
                self.loadingScreen.showTarget(exit=True)
        self.loadingScreen.show()
        base.disableZoneLODs()
        self._processVisStopIW = InterestWatcher(self, 'stopProcessViz')
        self.acceptOnce(self._processVisStopIW.getDoneEvent(), Functor(self._removeShardObjects, loginState))
        messenger.send(PiratesClientRepository.StopVisibilityEvent)
        self._processVisStopIW.stopCollect()
        OTPClientRepository.enterCloseShard(self, loginState)

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def _removeShardObjects(self, loginState):
        callback = self._deleteLocalAv
        self.cache.turnOff()
        localAvatar.clearInventoryInterest()
        if base.slowCloseShard:
            taskMgr.doMethodLater(base.slowCloseShardDelay * 0.5, Functor(self.removeShardInterest, callback), 'slowCloseShard')
        else:
            self.removeShardInterest(callback)

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def _deleteLocalAv(self):
        self.sendSetAvatarIdMsg(0)
        self.disableDoId(localAvatar.doId)

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def enterNoConnection(self):
        OTPClientRepository.enterNoConnection(self)
        if hasattr(base, 'localAvatar'):
            base.localAvatar.logDefaultShard()

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def isShardInterestOpen(self):
        return False

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def _removeCurrentShardInterest(self, callback):
        parentId2handles = {}
        for handle, state in self._interests.items():
            parentId2handles.setdefault(state.parentId, set())
            parentId2handles[state.parentId].add(handle)

        doId2parentId = {}
        for doId in parentId2handles.keys():
            obj = self.getDo(doId)
            if obj is not None:
                doId2parentId[doId] = obj.parentId

        parentId2childIds = {}
        for doId, parentId in doId2parentId.items():
            parentId2childIds.setdefault(parentId, set())
            parentId2childIds[parentId].add(doId)

        print 'parentId2handles: %s' % parentId2handles
        print 'parentId2childIds: %s' % parentId2childIds
        self.closeShardEGroup = EventGroup('closeShardInterest')
        self.acceptOnce(self.closeShardEGroup.getDoneEvent(), callback)
        for districtId in self.activeDistrictMap.keys():
            self._remInterests(districtId, parentId2childIds, parentId2handles)

        return

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def _remInterests(self, parentId, parentId2childIds, parentId2handles):
        for childId in parentId2childIds.get(parentId, tuple()):
            self._remInterests(childId, parentId2childIds, parentId2handles)

        for handle in parentId2handles.get(parentId, tuple()):
            if not self._interests[handle].isPendingDelete():
                self.removeInterest(DoInterestManager.InterestHandle(handle), self.closeShardEGroup.newEvent('handle-%s' % handle))

    @report(types=['args', 'deltaStamp'], dConfigParam='teleport')
    def exitCloseShard(self):
        self.loadingScreen.hide()
        if hasattr(self, 'closeShardEGroup'):
            self.ignore(self.closeShardEGroup.getDoneEvent())
            del self.closeShardEGroup
        if hasattr(self, '_localAvDisableIW'):
            self.ignore(self._localAvDisableIW.getDoneEvent())
            self._localAvDisableIW.destroy()
            del self._localAvDisableIW
        if hasattr(self, '_processVisStopIW'):
            self.ignore(self._processVisStopIW.getDoneEvent())
            self._processVisStopIW.destroy()
            del self._processVisStopIW
        OTPClientRepository.exitCloseShard(self)

    def startReaderPollTask(self):
        print '########## startReaderPollTask Pirate'
        self.stopReaderPollTask()
        self.accept(CConnectionRepository.getOverflowEventName(), self.handleReaderOverflow)
        taskMgr.add(self.readerPollUntilEmpty, self.uniqueName('readerPollTask'), priority=self.taskPriority, taskChain='net')

    def stopReaderPollTask(self):
        print '########## stopReaderPollTask Pirate'
        self.ignore(CConnectionRepository.getOverflowEventName())
        taskMgr.remove(self.uniqueName('readerPollTask'))

    def taskManagerDoYieldCall(self, frameStartTime, nextScheuledTaksTime):
        Thread.forceYield()

    def handleSystemMessage(self, di):
        message = ClientRepositoryBase.handleSystemMessage(self, di)
        if hasattr(base, 'talkAssistant'):
            hasattr(base, 'localAvatar') and base.talkAssistant.receiveSystemMessage(message)
        else:
            if self.fakeMSP is None:
                from pirates.piratesgui.MessageStackPanel import MessageStackPanel
                self.fakeMSP = MessageStackPanel(parent=base.a2dBottomLeft, relief=None, pos=(1.75,
                                                                                              0,
                                                                                              1.3))
            self.fakeMSP.addTextMessage(message, seconds=20, priority=0, color=(0.5,
                                                                                0,
                                                                                0,
                                                                                1), icon=('admin',
                                                                                          ''))

            def cleanupFakeMSP(task):
                if self.fakeMSP is not None:
                    self.fakeMSP.destroy()
                    self.fakeMSP = None
                return

            taskMgr.remove('cleanupFakeMSP')
            taskMgr.doMethodLater(25.0, cleanupFakeMSP, 'cleanupFakeMSP')
        if not self.systemMessageSfx:
            self.systemMessageSfx = loadSfx(SoundGlobals.SFX_GUI_WHISPER)
        if self.systemMessageSfx:
            base.playSfx(self.systemMessageSfx)
        return

    def getInventoryMgr(self, doId):
        return self.inventoryManager[doId % self.inventoryMgrCount]

    def createInventoryManagers(self, num):
        self.inventoryMgrCount = num
        self.inventoryManager = []
        for i in xrange(num):
            self.inventoryManager.append(self.generateGlobalObject(OtpDoGlobals.OTP_DO_ID_PIRATES_INVENTORY_MANAGER_BASE + i, 'DistributedInventoryManager'))

    @report(types=['args', 'deltaStamp'], dConfigParam='dteleport')
    def setDistrict(self, district):
        self.district = district

    def queryShowEffect(self, effectName=None):
        if effectName == None:
            return base.cr.wantSpecialEffects
        else:
            return self.effectToggles.get(effectName, base.cr.wantSpecialEffects)
        return

    def hasToggledEffects(self):
        return self.effectToggles != {}

    @report(types=['args', 'deltaStamp'], dConfigParam='dteleport')
    def addTaggedInterest(self, parentId, zoneId, mainTag, desc, otherTags=[], event=None):
        tags = set([mainTag] + otherTags)
        description = '%s | %6s' % (desc, (' ').join(tags))
        handle = self.addInterest(parentId, zoneId, description, event)
        if handle:
            for tag in tags:
                self._tagsToInterests.setdefault(tag, []).append(handle)

            self._interestsToTags[handle] = tags
        return handle

    @report(types=['args', 'deltaStamp'], dConfigParam='dteleport')
    def removeTaggedInterest(self, interestHandle, event=None):
        tags = self._interestsToTags.pop(interestHandle, [])
        if tags:
            for tag in tags:
                handles = self._tagsToInterests.get(tag)
                handles.remove(interestHandle)
                if not handles:
                    self._tagsToInterests.pop(tag)

            self.removeInterest(interestHandle, event)
        return tags

    @report(types=['args', 'deltaStamp'], dConfigParam='dteleport')
    def removeInterestTag(self, tag, event=None):
        handles = self._tagsToInterests.get(tag, [])[:]
        if event:
            if not handles:
                messenger.send(event)
                return

            def subInterestClosed(handle, handles=handles):
                handles.remove(handle)
                if not handles:
                    messenger.send(event)

            for x, handle in enumerate(handles):
                subEvent = '%s-%s' % (event, x)
                self.acceptOnce(subEvent, subInterestClosed, extraArgs=[handle])
                tags = self.removeTaggedInterest(handle, event=subEvent)

        for x, handle in enumerate(handles):
            tags = self.removeTaggedInterest(handle)

        return handles

    @report(types=['args', 'deltaStamp'], dConfigParam='dteleport')
    def getInterestTags(self, interestHandle):
        return self._interestsToTags.get(interestHandle, [])

    @report(types=['args', 'deltaStamp'], dConfigParam='dteleport')
    def getInterestHandles(self, tag):
        return self._tagsToInterests.get(tag, set())

    @report(types=['args', 'deltaStamp'], dConfigParam='dteleport')
    def setShardId(self, shardId):
        self._shardId = shardId

    @report(types=['args', 'deltaStamp'], dConfigParam='dteleport')
    def getShardId(self):
        return self._shardId

    @report(types=['args', 'deltaStamp'], dConfigParam='dteleport')
    def pushWorldInterest(self, parentId, zoneId, event=None):
        self._worldStack.append(self.addTaggedInterest(parentId, zoneId, self.ITAG_WORLD, 'world-%s' % (len(self._worldStack),), event=event))
        return self._worldStack[-1]

    @report(types=['args', 'deltaStamp'], dConfigParam='dteleport')
    def popWorldInterest(self, event=None):
        return self.removeTaggedInterest(self._worldStack.pop(-1), event)

    def getWorldStack(self):
        return [ self.getInterestLocations(handle)[0] for handle in self._worldStack ]

    @report(types=['args', 'deltaStamp'], dConfigParam='dteleport')
    def setWorldStack(self, worldLocations, event=None):
        currentLocations = self.getWorldStack()
        matches = [ pair[0] for pair in zip(currentLocations, worldLocations) if pair[0] == pair[1] ]
        for x in range(len(currentLocations) - len(matches)):
            self.popWorldInterest()

        for parentId, zoneId in worldLocations[len(matches):]:
            self.pushWorldInterest(parentId, zoneId, event=event)

        return len(matches)

    @report(types=['args', 'deltaStamp'], dConfigParam='dteleport')
    def closeShard(self):
        self.shardFSM.request('NoShard')

    @report(types=['args', 'deltaStamp'], dConfigParam='dteleport')
    def logout(self):
        localAvatar.b_setLocation(0, 0)
        self.shardFSM.request('Off')

        def allInterestsClosed():
            self._deleteLocalAv()
            self.doDetectLeaks = True
            self.loginFSM.request('waitForAvatarList')

        self.setAllInterestsCompleteCallback(allInterestsClosed)

    def printInterestSets(self):
        print '******************* Interest Sets **************'
        format = '%6s %' + str(40) + 's %11s %11s %8s %8s %8s'
        print format % ('Handle', 'Description', 'ParentId', 'ZoneIdList', 'State',
                        'Context', 'Event')
        for id, state in self._interests.items():
            if len(state.events) == 0:
                event = ''
            else:
                if len(state.events) == 1:
                    event = state.events[0]
                else:
                    event = state.events
            print format % (id, state.desc, state.parentId, state.zoneIdList, state.state, state.context, event)

        print '************************************************'