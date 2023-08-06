__version__ = '0.1.0'
from socket import getaddrinfo
from ipaddress import ip_address

def is_ssrf(domain):
    addrinfo = getaddrinfo(domain, 80)[0]
    ip = addrinfo[-1][0]
    ipaddr = ip_address(ip)
    return ipaddr.is_private