from .etc import settings

import json
import requests
import time

class STClient(object):
    
    def __init__(self) -> None:
        
        # set apis endpoints 
        self.auth_url = settings.HANZO_SERVER
        self.base_url = settings.ST_SERVER
        
        # set headers
        self.headers = {'Content-Type': 'application/json'}
        
        # connection access tokens
        self.access_token = None
        self.refresh_token = None
        
        
    def login(self, username: str, password: str) -> None:
        
        # keep user credentials
        self.username = username
        self.password = password
        
        # set login data
        login_data = {'username': username, 'password': password}
        
        # send login request
        response = requests.post(self.auth_url + '/login', headers=self.headers, data=json.dumps(login_data))
        
        # check response status code
        if response.status_code == 200:
            
            # get access token
            self.access_token = response.json()['access_token']
            
            # get refresh token
            self.refresh_token = response.json()['refresh_token']
            
            # set authorization header
            self.headers['Authorization'] = 'Bearer ' + self.access_token
            
        else:
            raise Exception('Login failed.')
        
    
    def refresh(self) -> None:
        
        if not self.refresh_token:
            raise ValueError('No refresh token available.')
        
        # set refresh data
        self.headers['Authorization'] = 'Bearer ' + self.refresh_token
        
        # send refresh request
        response = requests.post(self.auth_url + '/refresh', headers=self.headers)
        
        # check response status code
        if response.status_code == 200:
            
            # get access token
            self.access_token = response.json()['access_token']
            
            # get refresh token
            self.refresh_token = response.json()['refresh_token']
            
            # set authorization header
            self.headers['Authorization'] = 'Bearer ' + self.access_token
            
        else:
            raise ConnectionError('Refresh failed.')
        
        
    def set_access_token(self, access_token: str) -> None:
        
        # set access token
        self.access_token = access_token
        
        # set authorization header
        self.headers['Authorization'] = 'Bearer ' + self.access_token
        
    
    def set_refresh_token(self, refresh_token: str) -> None:
        
        # set refresh token
        self.refresh_token = refresh_token
        
        
    def session(self): 
        
        response = requests.get(self.base_url + '/session', headers=self.headers)
        
        if response.status_code != 200:
            raise ConnectionError(f'Session request failed: {response.text}')
        
        
    def get_access_token(self) -> str:
        
        return self.access_token
    
    def get_refresh_token(self) -> str:
        
        return self.refresh_token
    
    def ping(self) -> None:
        
        response = requests.get(self.base_url + '/ping', headers=self.headers)
        
        if response.status_code != 200:
            raise ConnectionError(f'Ping failed: {response.text}')
        
        return response.json()
    
    # general operations
    def get_databases(self):
        
        response = requests.get(self.base_url, headers=self.headers)
        
        if response.status_code != 200:
            raise Exception(f'Get databases failed: {response.text}')
        
        return response.json()
    
    def get_collections(self, database):
        
        response = requests.get(self.base_url + '/' + database, headers=self.headers)
        
        if response.status_code != 200:
            raise Exception(f'Get collections failed: {response.text}')
        
        return response.json()
    
    def count(self, database, collection):
        
        response = requests.get(self.base_url + '/' + database + '/' + collection + '/count', headers=self.headers)
        
        if response.status_code != 200:
            raise Exception(f'Count failed: {response.text}')
        
        return response.json()
    
    # crud operations
    def insert(self, database, collection, data):
        
        response = requests.post(self.base_url + '/' + database + '/' + collection, headers=self.headers, json=data)
        
        if response.status_code != 200:
            raise Exception(f'Insert failed: {response.text}')
        
        return response.json()
    
    
    def find_by_id(self, database, collection, id):
        
        response = requests.get(self.base_url + '/' + database + '/' + collection + '/' + id, headers=self.headers)
        
        if response.status_code != 200:
            raise Exception(f'Find by id failed: {response.text}')
        
        return response.json()
    
    
    def find_by(self, database, collection, query):
        
        response = requests.get(self.base_url + '/' + database + '/' + collection + '/findBy', headers=self.headers, params=query)
        
        if response.status_code != 200:
            raise Exception(f'Find failed: {response.text}')
        
        return response.json()
    
    def find_all(self, database, collection): 
        
        response = requests.get(self.base_url + '/' + database + '/' + collection, headers=self.headers)
        
        if response.status_code != 200:
            raise Exception(f'Find all failed: {response.text}')
        
        return response.json()
    
    def find_first(self, database, collection):
        
        response = requests.get(self.base_url + '/' + database + '/' + collection + '/first', headers=self.headers)
        
        if response.status_code != 200:
            raise Exception(f'Find first failed: {response.text}')
        
        return response.json()
    
    def find_last(self, database, collection):
        
        response = requests.get(self.base_url + '/' + database + '/' + collection + '/last', headers=self.headers)
        
        if response.status_code != 200:
            raise Exception(f'Find last failed: {response.text}')
        
        return response.json()
    
    def drop_collection(self, database, collection):
        
        response = requests.delete(self.base_url + '/' + database + '/' + collection, headers=self.headers)
        
        if response.status_code != 200:
            raise Exception(f'Drop collection failed: {response.text}')
        
        return response.json()
    
    def delete(self, database, collection, id):
        
        response = requests.delete(self.base_url + '/' + database + '/' + collection + '/' + id, headers=self.headers)
        
        if response.status_code != 200:
            raise Exception(f'Delete failed: {response.text}')
        
        return response.json()
    
    def update(self, database, collection, id, data):
        
        response = requests.put(self.base_url + '/' + database + '/' + collection + '/' + id, headers=self.headers, json=data)
        
        if response.status_code != 200:
            raise Exception(f'Update failed: {response.text}')
        
        return response.json()
    
    def update_many(self, database, collection, query, data):
        
        response = requests.put(self.base_url + '/' + database + '/' + collection + '/updateMany', headers=self.headers, params=query, json=data)
        
        if response.status_code != 200:
            raise Exception(f'Update by failed: {response.text}')
        
        return response.json()