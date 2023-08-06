import requests

class HttpClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.headers = { 'Authorization': api_key }

    def http_get(self, url, params={}):
        try:
            res = requests.get(self.base_url + url, params=params, headers=self.headers)
            res.raise_for_status()
            return res.json()
        except requests.exceptions.RequestException as err:
            raise SystemExit(err)

    def http_post(self, url, params={}, data={}):
        try:
            res = requests.post(self.base_url + url, params=params, json=data, headers=self.headers)
            res.raise_for_status()
            return res.json()
        except requests.exceptions.RequestException as err:
            raise SystemExit(err)
