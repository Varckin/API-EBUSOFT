import ipaddress, geoip2.database
from geoip2.errors import AddressNotFoundError
from ip_geo_lookup.settings import SETTINGS
from ip_geo_lookup.models import IPResponse
from typing import Optional, Tuple


class IPGeoService:
    def __init__(self):
        self.city_reader = geoip2.database.Reader(SETTINGS.CITY_DB_PATH)
        self.asn_reader = geoip2.database.Reader(SETTINGS.ASN_DB_PATH)
        self.country_reader = geoip2.database.Reader(SETTINGS.COUNTRY_DB_PATH)

    def _validate_ip(self, ip: str):
        """
        Validates the provided IP address.
        """
        try:
            ipaddress.ip_address(ip)
        except ValueError:
            raise ValueError("Invalid IP address")

    def get_country(self, ip: str) -> Optional[str]:
        """
        Retrieves the ISO country code associated with the given IP address.
        """
        self._validate_ip(ip)
        try:
            data = self.country_reader.country(ip)
            return data.country.iso_code
        except AddressNotFoundError:
            return None

    def get_city(self, ip: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Retrieves the region (state/province) and city associated with the given IP address.
        """
        self._validate_ip(ip)
        try:
            data = self.city_reader.city(ip)
            return data.subdivisions.most_specific.name, data.city.name
        except AddressNotFoundError:
            return None, None

    def get_asn(self, ip: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Retrieves the Autonomous System Number (ASN) and organization for the given IP address.
        """
        self._validate_ip(ip)
        try:
            data = self.asn_reader.asn(ip)
            return f"AS{data.autonomous_system_number}", data.autonomous_system_organization
        except AddressNotFoundError:
            return None, None
        
    def lookup(self, ip: str) -> IPResponse:
        """
        Performs a full IP lookup, combining country, region, city, ASN, and provider information.
        """
        self._validate_ip(ip)
        country = self.get_country(ip)
        region, city = self.get_city(ip)
        asn, provider = self.get_asn(ip)

        # fallback: if country is not found via country_db, get it from city_db
        if not country:
            country, _ = self.get_city(ip)
        
        return IPResponse(
            ip=ip,
            country=country,
            region=region,
            city=city,
            asn=asn,
            provider=provider
        )
