import json

import requests as rq

from ankorstore_api_wrapper import utils, resources, exceptions


class APIWrapper:
    BASE_URL = 'https://www.ankorstore.com'
    BASE_URL_SANDBOX = 'https://www.public.sandbox.ankorstore.com'

    def __init__(self, api_version, client_id=None, client_secret=None, access_token=None, sandbox=False):
        self._api_version = api_version

        self._base_url = self.BASE_URL if not sandbox else self.BASE_URL_SANDBOX
        self._base_host = utils.urljoin(self._base_url, 'api', self._api_version)
        self._session = rq.Session()

        self._resources = {
            'orders': resources.OrderPool(
                utils.urljoin(self._base_host, 'orders'), self._session),
        }

        if access_token:
            self._session.headers.update({
                'Authorization': 'Bearer {}'.format(access_token)
            })
        else:
            self._authenticate(client_id, client_secret)

    def _authenticate(self, client_id, client_secret):
        if not client_id or not client_secret:
            raise ValueError('No client_id and client_secret provided')
        
        auth_url = 'https://www.ankorstore.com/oauth/token'
        auth_data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
            'scope': '*'
        }
        res = self._session.post(auth_url, data=auth_data)
        if res.status_code != 200:
            raise exceptions.AuthenticationError("Authentication failed with status code {}: {}".format(res.status_code, res.text))

        res_data = res.json()
        self._session.headers.update({
            'Authorization': 'Bearer {}'.format(res_data['access_token'])
        })
        return res_data

    @property
    def resources(self):
        """Return all resources as a list of Resources"""
        return self._resources

    @property
    def orders(self):
        return self._resources['orders']

