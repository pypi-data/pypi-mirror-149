import configparser

class ConfigUtility:
    _instance = None
    _config = None
    _CONFIG_VERSION = 2
    _VERSION = {'version':_CONFIG_VERSION}
    _REPORT_PATH = {'outputpath':'C:\IPRA','inputpath':'C:\IPRA'}
    _LOGGER_PATH = {'loggerpath':'C:\IPRA\LOG\\'}
    _DOWNLOAD_REPORT = {'pru':False,'aia':False}
    _LANGUAGE = {'language':'zh_HK'}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self._config = configparser.ConfigParser()
        configContent = self._config.read("C:\IPRA\config.ini")
        if len(configContent) == 0:
            self.CreateConfigFile()
        else:
            self.UpdateConfigFile()
    
    def CreateConfigFile(self):
        with open('C:\IPRA\config.ini', 'w') as configfile:
            self.CreateDefaultConfig().write(configfile)
        self._config.read("C:\IPRA\config.ini")
        
        pass
    
    def CreateDefaultConfig(self):
        defaultConfig = configparser.ConfigParser()
        defaultConfig['version'] = self._VERSION
        defaultConfig['report_path'] = self._REPORT_PATH
        defaultConfig['logger_path'] = self._LOGGER_PATH
        defaultConfig['default_download_report'] = self._DOWNLOAD_REPORT
        defaultConfig['language'] = self._LANGUAGE
        return defaultConfig
    
    def UpdateConfigFile(self):
        if 'version' in self._config:
            if 'version' in self._config['version']:
                if self._config['version']['version'] == str(self._CONFIG_VERSION):
                    #latest config file version, no need to update
                    return
                else:
                    #update config file
                    self.LoopCheckConfigFile()
                    return
            else:
                self.LoopCheckConfigFile()
                return
        else:
            self.LoopCheckConfigFile()
            return
        
    def LoopCheckConfigFile(self):
        if 'version' in self._config:
            self._config.set(section='version',option='version',value=str(self._CONFIG_VERSION))
        else:
            self._config.add_section('version')
            self._config.set(section='version',option='version',value=str(self._CONFIG_VERSION))
            
        if 'report_path' in self._config:
            for key in self._REPORT_PATH:
                if key not in self._config['report_path']:
                    self._config.set(section='report_path',option=key,value=self._REPORT_PATH[key])
        else:
            self._config.add_section('report_path')
            for key in self._REPORT_PATH:
                self._config.set(section='report_path',option=key,value=self._REPORT_PATH[key])
        
        if 'logger_path' in self._config:
            for key in self._LOGGER_PATH:
                if key not in self._config['logger_path']:
                    self._config.set(section='logger_path',option=key,value=self._LOGGER_PATH[key])
        else:
            self._config.add_section('logger_path')
            for key in self._LOGGER_PATH:
                self._config.set(section='logger_path',option=key,value=self._LOGGER_PATH[key])    

        if 'default_download_report' in self._config:
            for key in self._DOWNLOAD_REPORT:
                if key not in self._config['default_download_report']:
                    self._config.set(section='default_download_report',option=key,value=self._DOWNLOAD_REPORT[key])
        else:
            self._config.add_section('default_download_report')
            for key in self._DOWNLOAD_REPORT:
                self._config.set(section='default_download_report',option=key,value=self._DOWNLOAD_REPORT[key])   
                
        if 'language' in self._config:
            for key in self._LANGUAGE:
                if key not in self._config['language']:
                    self._config.set(section='language',option=key,value=self._LANGUAGE[key])
        else:
            self._config.add_section('language')
            for key in self._LANGUAGE:
                self._config.set(section='language',option=key,value=self._LANGUAGE[key])       
                
                
        with open('C:\IPRA\config.ini', 'w') as configfile:
            self._config.write(configfile)
        
        pass
    
    def GetConfig(self,section,key):
        try:
            return self._config[section][key]
        except Exception as e:
            return None
    
    def UpdateOrWriteConfig(self, section, key, value):
        self._config.set(section=section,option=key,value=value)
        with open('C:\IPRA\config.ini', 'w') as configfile:
            self._config.write(configfile)
        pass
    