from conf import SERVICE_URL
from retry_session import retry_session


def list(url, auth):
    results = []
    while url:
        page = retrieve(url, auth)
        results.extend(page['results'])
        url = page['next']
    return results


def retrieve(url, auth):
    session = retry_session(2)
    response = session.get(SERVICE_URL + url, headers={
        'Authorization': '{token_type} {access_token}'.format(**auth),
    })
    response.raise_for_status()
    return response.json()


def create(url, payload, auth):
    session = retry_session(2)
    response = session.post(SERVICE_URL + url, json=payload, headers={
        'Authorization': '{token_type} {access_token}'.format(**auth),
    })
    response.raise_for_status()
    return response.json()


def update(url, payload, auth):
    session = retry_session(2)
    response = session.patch(SERVICE_URL + url, json=payload, headers={
        'Authorization': '{token_type} {access_token}'.format(**auth),
    })
    response.raise_for_status()
    return response.json()


def destroy(url, auth):
    session = retry_session(2)
    response = session.delete(SERVICE_URL + url, headers={
        'Authorization': '{token_type} {access_token}'.format(**auth),
    })
    response.raise_for_status()
    return response.json()
