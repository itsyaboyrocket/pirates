# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.chat.PWhiteList
import os
from pandac.PandaModules import *
from direct.showbase import AppRunnerGlobal
from otp.chat.WhiteList import WhiteList
from pirates.piratesbase.PLocalizer import enumeratePirateNameTokensLower

class PWhiteList(WhiteList):
    __module__ = __name__

    def __init__(self):
        vfs = VirtualFileSystem.getGlobalPtr()
        filename = Filename('pwhitelist.txt')
        searchPath = DSearchPath()
        if AppRunnerGlobal.appRunner:
            searchPath.appendDirectory(Filename.expandFrom('$POTCO_WL_ROOT/etc'))
        else:
            searchPath.appendDirectory(Filename('.'))
            searchPath.appendDirectory(Filename('etc'))
            searchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('$PIRATES/src/chat')))
            searchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('pirates/src/chat')))
            searchPath.appendDirectory(Filename.fromOsSpecific(os.path.expandvars('pirates/chat')))
        found = vfs.resolveFilename(filename, searchPath)
        if not found:
            message = 'pwhitelist.txt file not found on %s' % searchPath
            raise IOError, message
        data = vfs.readFile(filename, 1)
        lines = data.split('\n')
        for token in enumeratePirateNameTokensLower():
            lines.append(token)

        WhiteList.__init__(self, lines)