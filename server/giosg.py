from conf import SERVICE_URL
from retry_session import retry_session


class APIClient:

    def __init__(self, auth):
        self.auth = auth

    def list(self, url):
        results = []
        while url:
            page = self.retrieve(url)
            results.extend(page['results'])
            url = page['next']
        return results

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
        return response.json()

    def update(self, url, payload):
        session = retry_session(2)
        response = session.patch(SERVICE_URL + url, json=payload, headers={
            'Authorization': '{token_type} {access_token}'.format(**self.auth),
        })
        response.raise_for_status()
        return response.json()

    def destroy(self, url):
        session = retry_session(2)
        response = session.delete(SERVICE_URL + url, headers={
            'Authorization': '{token_type} {access_token}'.format(**self.auth),
        })
        response.raise_for_status()
        return response.json()
