import requests


class APISession(requests.Session):
    def __init__(self, url, api_key):
        self.url = url.rstrip('/')
        self.api_key = api_key
        super().__init__()

    def request(
        self,
        method,
        url,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=None,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
    ):
        url = self.url + url
        if headers is None:
            headers = {}
        headers['Authorization'] = f'Bearer {self.api_key}'
        return super().request(
            method,
            url,
            params,
            data,
            headers,
            cookies,
            files,
            auth,
            timeout,
            allow_redirects,
            proxies,
            hooks,
            stream,
            verify,
            cert,
            json,
        )
