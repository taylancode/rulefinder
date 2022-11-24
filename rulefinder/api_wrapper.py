from rulefinder.decorators import Decorators
from requests import request
from requests.exceptions import SSLError, HTTPError, TooManyRedirects, Timeout
from requests import Response

class APIWrapper:
    '''
    API Wrapper class
    '''

    @staticmethod
    def api_call(values: dict=None, verify: bool=False, timeout: int=300) -> Response:
        '''
        Makes an API call and returns Response object

        :param values: Dictionary containing, base_url, request_type (GET/POST), params, headers, verification and timeout
        :param verify: (Optional) Boolean to override verify (Default is False)
        :param timeout: (Optional) Int containing timeout in seconds (Default is 300)
        :return: Response object
        '''

        try:

            url = values['base_url']
            req_type = values['type']
            params = values['params']
            headers = values['headers']
            ver = verify
            time = timeout

        except KeyError as err:
            raise Exception(f'Expected 4 values, missing one or more {err}')

        try:

            req = request(
                req_type,
                url=url,
                headers=headers,
                params=params,
                verify=ver,
                timeout=time
            )

            req.raise_for_status()
            return req

        except (SSLError, HTTPError, Timeout, ConnectionError, TooManyRedirects) as err:
            raise Exception(f'API call failed due to {err}')

class PA_API:
    '''
    Class containing Palo Alto API call wrappers
    '''

    @staticmethod
    @Decorators.check_connectivity
    def get_post_rulebase(host: str, dgroup: str, key: str) -> Response:
        '''
        Gets all post rules in specified device group

        :param host: String containing Panorama Hostname/Address
        :param dgroup: String containing device group to search
        :param key: String containing API Key
        :return: Response object
        '''

        values = {
            'base_url': f'https://{host}/api',
            'type': 'POST',
            'params': {
                'type': 'config',
                'action': 'get',
                'xpath': f"/config/devices/entry[@name='localhost.localdomain']/device-group/entry[@name='{dgroup}']/post-rulebase/security",
            },
            'headers': {
                'X-PAN-KEY': key,
            }
        }

        return APIWrapper.api_call(values)

    @staticmethod
    @Decorators.check_connectivity
    def get_all_shared_objects(host: str, key: str) -> Response:
        '''
        Gets all shared address objects

        :param host: String containing Panorama Hostname/Address
        :param key: String containing API Key
        :return: Response object
        '''

        values = {
            'base_url': f'https://{host}/api',
            'type': 'GET',
            'params': {
                'type': 'config',
                'action': 'get',
                'xpath': '/config/shared/address',
            },
            'headers': {
                'X-PAN-KEY': key,
            }
        }

        return APIWrapper.api_call(values)
