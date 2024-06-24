import os
import workers_kv


class WorkersKV:
    def __init__(self):
        self.kv = workers_kv.Namespace(
            account_id=os.environ["ACCOUNT_ID"],
            namespace_id=os.environ["NAMESPACE"],
            api_key=os.environ["API_KEY"],
        )

    def add(self, key: str, value: str | dict | list):
        return self.kv.write({key: value})

    def list(self):
        return self.kv.list_keys()

    def get(self, key: str):
        return self.kv.read(key)

    def rm(self, key: str):
        return self.kv.delete_one(key)
