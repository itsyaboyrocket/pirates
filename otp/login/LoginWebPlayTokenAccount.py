# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.login.LoginWebPlayTokenAccount
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
import LoginTTAccount

class LoginWebPlayTokenAccount(LoginTTAccount.LoginTTAccount):
    __module__ = __name__
    notify = DirectNotifyGlobal.directNotify.newCategory('LoginWebPlayTokenAccount')

    def supportsRelogin(self):
        return 0

    def createAccount(self, loginName, password, data):
        pass

    def authorize(self, loginName, password):
        self.playToken = password
        self.playTokenIsEncrypted = 1
        self.freeTimeExpires = -1
        self.cr.freeTimeExpiresAt = self.freeTimeExpires

    def createBilling(self, loginName, password, data):
        pass

    def setParentPassword(self, loginName, password, parentPassword):
        pass

    def supportsParentPassword(self):
        return 1

    def changePassword(self, loginName, password, newPassword):
        pass

    def requestPwdReminder(self, email=None, acctName=None):
        pass

    def cancelAccount(self, loginName, password):
        pass

    def getAccountData(self, loginName, password):
        pass

    def getErrorCode(self):
        if not self.has_key('response'):
            return 0
        return self.response.getInt('errorCode', 0)

    def needToSetParentPassword(self):
        return 0