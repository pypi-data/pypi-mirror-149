import imp
from frproxy import CustomProxy, GeonodeProxy
from requests import *
gp = GeonodeProxy(100, 10)
print(gp.request(get, 'https://httpbin.org/ip', timeout=2))