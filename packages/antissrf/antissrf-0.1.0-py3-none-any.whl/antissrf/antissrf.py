from socket import getaddrinfo
from ipaddress import ip_address

def is_ssrf(domain):
    addrinfo, = getaddrinfo(domain, 80)
    ip, = addrinfo[-1]
    ipaddr = ip_address(ip)
    return ipaddr.is_private