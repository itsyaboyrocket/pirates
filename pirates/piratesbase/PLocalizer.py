# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesbase.PLocalizer
from pandac.libpandaexpressModules import *
import string, types
try:
    language = getConfigExpress().GetString('language', 'english')
    checkLanguage = getConfigExpress().GetBool('check-language', 1)
except:
    language = simbase.config.GetString('language', 'english')
    checkLanguage = simbase.config.GetBool('check-language', 1)
else:

    def getLanguage():
        return language


    print 'PLocalizer: Running in language: %s' % language
    _languageModule = 'pirates.piratesbase.PLocalizer' + string.capitalize(language)
    _questStringModule = 'pirates.piratesbase.PQuestStrings' + string.capitalize(language)
    _greetingStringModule = 'pirates.piratesbase.PGreetingStrings' + string.capitalize(language)
    _dialogStringModule = 'pirates.piratesbase.PDialogStrings' + string.capitalize(language)
    exec 'from ' + _languageModule + ' import *'
    exec 'from ' + _questStringModule + ' import *'
    exec 'from ' + _greetingStringModule + ' import *'
    exec 'from ' + _dialogStringModule + ' import *'
    if checkLanguage:
        l = {}
        g = {}
        englishModule = __import__('pirates.piratesbase.PLocalizerEnglish', g, l)
        foreignModule = __import__(_languageModule, g, l)
        for key, val in englishModule.__dict__.items():
            if not foreignModule.__dict__.has_key(key):
                print 'WARNING: Foreign module: %s missing key: %s' % (_languageModule, key)
                locals()[key] = val
            elif isinstance(val, types.DictType):
                fval = foreignModule.__dict__.get(key)
                for dkey, dval in val.items():
                    if not fval.has_key(dkey):
                        print 'WARNING: Foreign module: %s missing key: %s.%s' % (_languageModule, key, dkey)
                        fval[dkey] = dval

                for dkey in fval.keys():
                    if not val.has_key(dkey):
                        print 'WARNING: Foreign module: %s extra key: %s.%s' % (_languageModule, key, dkey)

        for key in foreignModule.__dict__.keys():
            if not englishModule.__dict__.has_key(key):
                print 'WARNING: Foreign module: %s extra key: %s' % (_languageModule, key)