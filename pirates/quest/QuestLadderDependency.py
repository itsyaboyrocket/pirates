# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.quest.QuestLadderDependency
from direct.directnotify import DirectNotifyGlobal
from pirates.quest import QuestLadder
from pirates.quest import QuestLadderDB
from pirates.quest import QuestDB

class QuestLadderDependency:
    __module__ = __name__

    def __init__(self):
        self.idDependencyMap = {}
        self.intDependencyMap = {}
        self.populateMap()

    def populateMap(self):
        self.idDependencyMap['test'] = 99999
        self.intDependencyMap[99999] = 99999

    def findIdDependency(self, questId):
        if self.idDependencyMap.has_key(questId):
            return self.idDependencyMap[questId]
        return 0

    def findIntDependency(self, questInt):
        if self.idDependencyMap.has_key(questId):
            return self.intDependencyMap[questId]
        return 0

    def checkDependency(self, quest, ladder, isId):
        dependency = 0
        if isId:
            dependency = self.findIdDependency(quest)
        else:
            dependency = self.findIntDependency(quest)
        if dependency == 0:
            return True
        if ladder.count(dependency):
            return True
        else:
            return False