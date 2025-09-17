import socket
from dns_forw_rev.models import DNSLookupResponse
from typing import Optional
from fastapi import HTTPException


def dns_lookup(ip: Optional[str] = None, domain: Optional[str] = None) -> DNSLookupResponse:
    """
    Lookup DNS information: 
    - If 'ip' is provided, return its domain (reverse DNS).
    - If 'domain' is provided, return its IPs (forward DNS).
    """
    if ip:
        try:
            resolved_domain = socket.gethostbyaddr(ip)[0]
            return DNSLookupResponse(ip=ip, domain=resolved_domain)
        except socket.herror:
            raise HTTPException(status_code=404, detail="Domain not found for this IP")
    elif domain:
        try:
            resolved_ips = socket.gethostbyname_ex(domain)[2]
            return DNSLookupResponse(domain=domain, ips=resolved_ips)
        except socket.gaierror:
            raise HTTPException(status_code=404, detail="IP addresses not found for this domain")
    else:
        raise HTTPException(status_code=400, detail="Either 'ip' or 'domain' must be provided")
