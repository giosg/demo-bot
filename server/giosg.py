from conf import SERVICE_URL
from retry_session import retry_session


class APIClient:

    def __init__(self, auth):
        self.auth = auth

    def list(self, url):
        return list(self.iterate(url))

    def retrieve(self, url):
        session = retry_session(2)
        response = session.get(SERVICE_URL + url, headers={
            'Authorization': '{token_type} {access_token}'.format(**self.auth),
        })
        response.raise_for_status()
        return response.json()

    def create(self, url, payload):
        session = retry_session(2)
        response = session.post(SERVICE_URL + url, json=payload, headers={
            'Authorization': '{token_type} {access_token}'.format(**self.auth),
        })
        response.raise_for_status()
        return response.json() if response.text else None

    def update(self, url, payload):
        session = retry_session(2)
        response = session.patch(SERVICE_URL + url, json=payload, headers={
            'Authorization': '{token_type} {access_token}'.format(**self.auth),
        })
        response.raise_for_status()
        return response.json() if response.text else None

    def destroy(self, url):
        session = retry_session(2)
        response = session.delete(SERVICE_URL + url, headers={
            'Authorization': '{token_type} {access_token}'.format(**self.auth),
        })
        response.raise_for_status()
        return response.json() if response.text else None

    def search(self, url, checker):
        for result in self.iterate(url):
            if checker(result):
                return result
        return None

    def iterate(self, url):
        while url:
            page = self.retrieve(url)
            for result in page['results']:
                yield result
            url = page['next']
