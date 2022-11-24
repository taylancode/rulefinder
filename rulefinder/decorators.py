from functools import wraps
import socket

class Decorators:
    '''
    Class object containing decorators
    '''

    @staticmethod
    def check_connectivity(func) -> bool:
        '''
        Top level function for reachability check
        '''
        @wraps(func)
        def is_reachable(*args, **kwargs):

            '''
            Decorator checks reachability over 443 to the specified host

            :param kwargs['host']: String Keyword Arg containing hostname or address
            :return: Original function
            '''
            try:
                sock = socket.socket()
                sock.connect((kwargs['host'], 443))
                return func(*args, **kwargs)
            except (TimeoutError, OSError):
                return False
            finally:
                sock.close()

        return is_reachable
