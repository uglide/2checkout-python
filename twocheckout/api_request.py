import requests

from .error import TwocheckoutError


class Api:

    username = None
    password = None
    private_key = None
    seller_id = None
    mode = None
    version = '1'

    @classmethod
    def credentials(cls, credentials):
        Api.username = credentials['username']
        Api.password = credentials['password']
        if 'mode' in credentials:
            Api.mode = credentials['mode']

    @classmethod
    def auth_credentials(cls, credentials):
        Api.private_key = credentials['private_key']
        Api.seller_id = credentials['seller_id']
        if 'mode' in credentials:
            Api.mode = credentials['mode']

    @classmethod
    def call(cls, action, params=None, method="GET"):
        if params is None:
            params = {}

        auth = None

        if action == 'authService':
            params['sellerId'] = cls.seller_id
            params['privateKey'] = cls.private_key
            headers = {
                'Accept': 'application/json',
                'User-Agent': '2Checkout Python/0.1.0/%s',
                'Content-Type': 'application/JSON'
            }
        else:
            auth = (cls.username, cls.password)
            headers = {
                'Accept': 'application/json',
                'User-Agent': '2Checkout Python/0.1.0/%s'
            }

        url = cls.build_url(action)

        if method == "POST":
            data = params
            params = {}
        else:
            data = None

        try:
            response = requests.request(
                method, url, headers=headers, auth=auth, params=params,
                data=data, allow_redirects=True
            )

            return response.json()
        except Exception as e:
            raise TwocheckoutError("", str(e))

    @classmethod
    def build_url(cls, method):
        if cls.mode == 'sandbox':
            url = 'https://sandbox.2checkout.com'
        else:
            url = 'https://www.2checkout.com'
        if method == 'authService':
            url += '/checkout/api/' + cls.version + '/' + cls.seller_id + '/rs/' + method
        else:
            url += '/api/' + method
        return url