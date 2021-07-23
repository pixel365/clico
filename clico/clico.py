import os
from typing import List, Union, Optional, Dict

import requests
from requests.exceptions import RequestException

from .models import Error, Result, Link, Integration

API_URL = 'https://cli.com/api/v1'


class Clico:
    def __init__(self, api_key: Optional[str] = None):
        self._api_key: Optional[str] = api_key or os.getenv('CLICO_API_KEY')

        if not self._api_key:
            raise ValueError('API key is required')

    def _call(self, path: str, data: Union[List, Dict]) -> Union[Error, Result]:
        try:
            r = requests.post(f'{API_URL}{path}', json=data, timeout=5,
                              headers={'Authorization': f'Bearer {self._api_key}'})
            if r.status_code != requests.codes.OK:
                if r.headers.get('Content-Type', None) != 'application/json':
                    return Error(**{'status': r.status_code})
                return Error(**{**{'status': r.status_code}, **r.json()})
        except RequestException as e:
            return Error(status=500, message=e)
        return Result(**r.json())

    def single_link(self, link: Link) -> Union[Error, Link]:
        assert isinstance(link, Link), f'Type `{type(link).__name__}` is not an instance of `Link` object'
        api_result = self._call(path='/link', data=link.dict())
        if isinstance(api_result, Error):
            return api_result
        return Link(**{**link.dict(), **{'short_link': api_result.result}})

    def multiple_links(self, links: List[Link]) -> Union[Error, List[Link]]:
        assert len(links) > 0, f'Type `{type(links).__name__}` is not an instance of `list` object'
        links = links[:1000]
        api_result = self._call(path='/links', data=[link.dict() for link in links])
        if isinstance(api_result, Error):
            return api_result

        result = []
        for i in range(len(links)):
            result.append(Link(**{**links[i].dict(), **{'short_link': api_result.result[i]}}))
        return result

    def integration(self, data: Integration) -> Union[Error, Integration]:
        assert isinstance(data, Integration), f'Type `{type(data).__name__}` is not an instance of `Integration` object'
        api_result = self._call(path='/integration', data=data.dict())
        if isinstance(api_result, Error):
            return api_result
        return Integration(**{**data.dict(), **{'token': api_result.result}})
