#requests封装
import requests
from utils.config_utils import local_config

class RequestsUtils:
    def __init__(self):
        self.hosts = local_config.HOSTS
        self.session = requests.session()
    def get(self,requests_info):
        url = self.hosts+requests_info['请求地址']
        response = self.session.get(url = url,
                                    params = requests_info['请求参数(get)'])

    def get(self,requests_info):
        url = self.hosts+requests_info['请求地址']
        return url