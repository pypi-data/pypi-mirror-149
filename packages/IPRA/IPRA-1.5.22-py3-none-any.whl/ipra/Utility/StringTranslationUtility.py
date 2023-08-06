from ipra.Utility.ConfigUtility import ConfigUtility

class StringTranslationUtility:
    _instance = None
    _CHINESE_STRING = []
    _ENGLISH_STRING = []
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._language = ConfigUtility().GetConfig('language','language')

    def CompanyFullName(self,companyName):
        if companyName == 'PRU':
            return 'PRUDENTIAL'
        else:
            return companyName
    
    def GetString(self,index):
        if self._language == 'zh-HK':
            return self._CHINESE_STRING[index]
        else:
            return self._ENGLISH_STRING[index]
            