from socket import getaddrinfo
from ipaddress import ip_address
import sys

class CallableModule():

    def __init__(self, wrapped):
        self._wrapped = wrapped

    def __call__(self, *args, **kwargs):
        return self._wrapped.is_ssrf(*args, **kwargs)

    def __getattr__(self, attr):
        return object.__getattribute__(self._wrapped, attr)

sys.modules[__name__] = CallableModule(sys.modules[__name__])

def is_ssrf(domain):
    addrinfo = getaddrinfo(domain, 80)[0]
    ip = addrinfo[-1][0]
    ipaddr = ip_address(ip)
    return ipaddr.is_private
