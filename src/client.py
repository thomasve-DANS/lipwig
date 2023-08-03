import requests
from urllib.parse import urljoin, urlparse

class BaseClient:

    def __init__(self, base_url: str, *args, **kwargs):
        self.base_url = base_url

    def _get(self, url, params=None):
        return requests.get(
            url=url,
            params=params,
            verify=False
        )

    def _parse(self, url):
        return urlparse(url)

    def _join(self, path):
        return urljoin(self.base_url, path)

class GettyClient(BaseClient):

    def proxy(self, path):
        parsed = self._parse(path)
        url = self._join(
            parsed.query
        )
        print(repr(parsed))
        response = self._get(url)
        return response.json()
