from requests import *
from tabulate import tabulate


class CustomProxy:
    def __init__(self, list_proxies, max_retries=1, verbose=False):
        self.proxies_size = len(list_proxies)
        self.list_proxies = [{'http': proxies, 'https': proxies} for proxies in list_proxies]
        self.stats = [{'num_access': 0, 'num_error': 0, 'last_err': ''} for _ in range(self.proxies_size)]
        self.proxies_pos = 0
        self.proxies = self.list_proxies[0]
        self.verbose = verbose
        self.max_retries = max_retries if max_retries else self.proxies_size

    def request(self, method, url, timeout=60):
        for _ in range(self.max_retries):
            self.stats[self.proxies_pos]['num_access'] = self.stats[self.proxies_pos]['num_access'] + 1
            try:
                r = method(url, proxies=self.proxies, timeout=timeout)
                self.stats[self.proxies_pos]['last_err'] = ''
                return r
            except Exception as e:
                self.stats[self.proxies_pos]['last_err'] = str(e)
                self.change_proxies()

    def change_proxies(self):
        self.stats[self.proxies_pos]['num_error'] = self.stats[self.proxies_pos]['num_error'] + 1
        self.proxies_pos = (self.proxies_pos + 1) % self.proxies_size
        self.proxies = self.list_proxies[self.proxies_pos]
        if self.verbose:
            print('change proxies to [{}] -'.format(self.proxies_pos), self.proxies)

    def summary(self):
        tabel = []
        keys = [key for key in self.stats[0] if key not in ['num_access', 'num_error', 'last_err']]
        # print(keys)
        for proxies, stat in zip(self.list_proxies, self.stats):
            err_rate = stat['num_error'] * 100 / float(stat['num_access']) if stat['num_access'] else 0
            row = [str(proxies), err_rate, stat['num_access'], stat['num_error']]
            for key in keys:
                row.append(stat[key])
            row.append(stat['last_err'])
            tabel.append(row)
        print(tabulate(tabel, headers=['proxies', 'err_rate (%)', 'num_access', 'num_error', 'last_error'] + keys))

class GeonodeProxy(CustomProxy):
  def __init__(self, limit, max_retries=1, protocols=[], country=None, uptime=None, speed=None, anonymity=[], google=None, verbose=False):
    param = {
        'limit':limit,
        'page':1,
        'sort_by':'lastChecked',
        'sort_type':'desc',
        'country': country,
        'anonymityLevel': anonymity,
        'protocols': ','.join(protocols) if protocols else protocols,
        'google': google if google is None else ('true' if google else 'false'),
        'filterUpTime': uptime,
        'speed': speed
    }
    
    r = get('https://proxylist.geonode.com/api/proxy-list', params=param)
    data = r.json()['data']
    proxies = ['{}://{}:{}'.format(proxy['protocols'][0], proxy['ip'], proxy['port']) for proxy in data]
    super().__init__(proxies, max_retries, verbose)