from urllib.parse import urljoin
import requests
import urllib3
import sys
import os

version = '0.1.23'

class LockerClientException(Exception):
    pass


class LockerStat():
    def __init__(self, path):
        self.path = path
        self.basename = os.path.basename(path)
        
        self.mtime = None
        self.size = None
        self.type = None


    def __str__(self):
        return f'{self.path} {self.type} {self.size} {self.mtime}'

class LockerClient():
    
    def __init__(self, host=None, key=None, insecure=False):
        self.host = host or os.getenv('LOCKER_HOST')
        self.key = key or os.getenv('LOCKER_KEY')

        assert(self.host)
        self.verify = not insecure # do not verify ssl

        if not self.verify:
            print("Insecure mode!")
            urllib3.disable_warnings()

        if self.host.startswith('http://') or self.host.startswith('https://'):
            self.base_url = self.host
        else:
            self.base_url = f'https://{self.host}'

        self.app_url = urljoin(self.base_url, 'app/')

        self.headers = {
            'User-Agent': 'locker-admin/0.1',
            'X-API-KEY': self.key
        }

    def path_url(self, path):
        if path.startswith('/'):
            path = path[1:]

        return urljoin(self.app_url, path)

    def post(self, path, data):
        #
        # make HTTP POST request with api-key
        # 

        url = self.path_url(path)
        r = requests.post(url, headers=self.headers, json=data, verify=self.verify)    
        r.raise_for_status()
        return r

    def stat(self, path):

        url = self.path_url(path)
        r = requests.head(url, headers=self.headers, verify=self.verify)    
        # if r.status_code == 200:
        r.raise_for_status()
        st = LockerStat(path)
        st.type = r.headers['X-FileType']
        st.mtime = r.headers['X-FileMTime']
        st.size = r.headers['X-FileSize']
        return st
        #    raise LockerClientException(f"ERROR! stat for {url} returned HTTP code {r.status_code}")

    def get(self, path, stream=False):
        url = self.path_url(path)
        r = requests.get(url, headers=self.headers, stream=stream, verify=self.verify)    
        r.raise_for_status()
        return r
        # raise LockerClientException(f"ERROR! get for {url} returned HTTP code {r.status_code}")

    def put(self, path, data):
        url = self.path_url(path)
        r = requests.put(url, headers=self.headers, data=data, verify=self.verify)
        r.raise_for_status()
        return r

    def mkdir(self, path):
        url = self.path_url(path)
        headers = self.headers
        data={'cmd': 'mkdir'}
        r = requests.post(url, headers=self.headers, json=data, verify=self.verify)
        r.raise_for_status()
        return r

    def rm(self, path, recursive=False):
        url = self.path_url(path)
        headers = self.headers
        if recursive:
            headers['recursive'] = '1'
            headers['rmdir'] = '1'
        r = requests.delete(url, headers=headers, verify=self.verify)
        return r

    def pubconf(self):
        r = requests.get(urljoin(self.base_url, '/pubconf'))
        r.raise_for_status()
        return r.json()

    def set_roomspace_secret(self, secret):
        data = {'secret': secret}
        r = requests.post(urljoin(self.base_url, '/set_roomspace_secret'), headers=self.headers, json=data, verify=self.verify)    
        r.raise_for_status()


    def get_flags(self, path='/var/flags.json', flag='flag', n=20):
        url = self.path_url(path)
        payload = {
            'cmd': 'get_flags',
            'flag': flag,
            'n': n
        } 
        r = requests.post(url, headers=self.headers, json=payload)
        r.raise_for_status()
        return r.json()

    def drop_flags(self, path, flag, droplist):
        url = self.path_url(path)
        payload = {
            'cmd': 'drop_flags',
            'flag': flag,
            'droplist': droplist
        } 
        r = requests.post(url, headers=self.headers, json=payload)
        r.raise_for_status()
        return r.json()

    def list_append(self, path, e, default=None):
        data = {
            'cmd': 'list_append',
            'default': default,
            'e': e
        }
        r = self.post(path, data)

    def list_delete(self, path, id):
        data = {
            'cmd': 'list_delete',
            'e': {
                '_id': id
            }
        }
        r = self.post(path, data)

    def __str__(self):
        return 'Locker host:{} key:{}'.format(self.host, bool(self.key))



