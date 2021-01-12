import os
import configparser
import time
config_file_path = os.path.join( os.path.dirname(__file__) ,'..','config','localconfig.ini' )
class ConfigUtils:
    def __init__(self,conf_path = config_file_path):
        self.cfg = configparser.ConfigParser()
        self.cfg.read( conf_path,encoding='utf-8' )
    @property   # 类中的一个方法加property这个装饰器 属性方法
    def HOSTS(self):
        hosts_value = self.cfg.get('default','HOSTS')
        return hosts_value
    @property
    def REPORT_PATH(self):
        report_path_value = self.cfg.get('path','REPORT_PATH')
        return report_path_value
    @property
    def LOG_PATH(self):
        log_path_value = self.cfg.get('default','LOG_PATH')
        return log_path_value
    @property
    def LOG_LEVEL(self):
        log_level_value = int(self.cfg.get('default','LOG_LEVEL'))
        return log_level_value

    @property
    def LOG_NAME(self):
        log_level_value = '%s_%s.log'%(self.cfg.get('default', 'LOG_NAME'),time.strftime('%Y_%m_%d_%H_%M_%S',))
        return log_level_value

    @property
    def SMTP_RECEIVER(self):
        smtp_receiver_value = self.cfg.get('default', 'SMTP_RECEIVER')
        return smtp_receiver_value

local_config = ConfigUtils()
if __name__ == '__main__':
    print( local_config.SMTP_RECEIVER )