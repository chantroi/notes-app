from appwrite.client import Client
from appwrite.services.databases import Databases
import os

class Note:
    def __init__(self):
        client = Client()
        (client
          .set_endpoint('https://cloud.appwrite.io/v1')
          .set_project(os.getenv('PROJECT_ID'))
          .set_key(os.getenv("API_ID"))
        )
        self.db = Databases(client)

    def add_note(self, key, data, auth):
        result = self.db.create_document('notes', 'notes', key, {'value': data, 'auth': auth})
        return result['value']
        
    def get_note(self, key):
        result = self.db.get_document('notes', 'notes', key)
        return result['value']
        
    def get_auth(self, key):
        result = self.db.get_document('notes', 'notes', key)
        return result['auth']
        
    def update_note(self, key, data, auth):
        result = self.db.update_document('notes', 'notes', key, {'value': data, 'auth': auth})
        return result['value']