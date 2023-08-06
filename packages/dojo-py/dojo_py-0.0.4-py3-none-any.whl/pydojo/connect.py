import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import time


def requests_retry_session(
    retries=10,
    backoff_factor=1,
    status_forcelist=(500, 502, 504, 401),
    session=None
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    session.proxies = {}
    session.proxies['http'] = 'socks5h://localhost:9050'
    session.proxies['https'] = 'socks5h://localhost:9050'
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def make_request(**data):

    headers = {"Authorization": "Bearer {}".format(data["header"])}
    params = data["params"]
    t0 = time.time()


    if str(data["type"]).lower() == "get":
        try:
            r = requests_retry_session().get(data["url"], headers=headers, params=params)
            print('Getting:', data["url"])
        except Exception as x:
            print('It failed :(', x.__class__.__name__)
        else:
            print('It worked', r.status_code)
        finally:
            t1 = time.time()
            print('Took', t1 - t0, 'seconds')

    if str(data["type"]).lower() == "post":
        payload = data["payload"]
        try:
            r = requests_retry_session().post(data["url"], headers=headers, params=params, data=payload)
            print('Getting:', data["url"])
        except Exception as x:
            print('It failed :(', x.__class__.__name__)
        else:
            print('It worked', r.status_code)
        finally:
            t1 = time.time()
            print('Took', t1 - t0, 'seconds')

    r = r.json()
    return r
