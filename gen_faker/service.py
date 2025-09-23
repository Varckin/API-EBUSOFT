from functools import lru_cache
from faker import Faker
from typing import Any, Dict, List, Optional


@lru_cache(maxsize=64)
def _create_faker(locale: str, seed: Optional[int]) -> Faker:
    faker = Faker(locale)
    if seed is not None:
        faker.seed_instance(seed)
    return faker


def generate_name(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).name()


def generate_first_name(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).first_name()


def generate_last_name(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).last_name()


def generate_email(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).email()


def generate_address(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).address()


def generate_city(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).city()


def generate_country(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).country()


def generate_phone(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).phone_number()


def generate_company(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).company()


def generate_job(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).job()


def generate_text(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).text()


def generate_sentence(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).sentence()


def generate_paragraph(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).paragraph()


def generate_url(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).url()


def generate_ipv4(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).ipv4()


def generate_ipv6(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).ipv6()


def generate_mac(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).mac_address()


def generate_date(locale="en_US", seed=None) -> str:
    return str(_create_faker(locale, seed).date())


def generate_datetime(locale="en_US", seed=None) -> str:
    return str(_create_faker(locale, seed).date_time())


def generate_credit_card(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).credit_card_number()


def generate_profile(locale="en_US", seed=None) -> dict:
    return _create_faker(locale, seed).profile()


def generate_user_agent(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).user_agent()


def generate_color(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).color_name()


def generate_uuid(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).uuid4()


def generate_license_plate(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).license_plate()


def generate_ssn(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).ssn()


def generate_passport(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).passport_number()


def generate_birthdate(locale="en_US", seed=None) -> str:
    return str(_create_faker(locale, seed).date_of_birth())


def generate_iban(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).iban()


def generate_swift(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).swift()


def generate_bban(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).bban()


def generate_pricetag(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).pricetag()


def generate_hostname(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).hostname()


def generate_tld(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).tld()


def generate_mime_type(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).mime_type()


def generate_word(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).word()


def generate_words(locale="en_US", seed=None) -> List[str]:
    return _create_faker(locale, seed).words(nb=3)


def generate_catch_phrase(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).catch_phrase()


def generate_barcode(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).ean13()


def generate_file_name(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).file_name()


def generate_currency_code(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).currency_code()


def generate_timezone(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).timezone()


def generate_language(locale="en_US", seed=None) -> str:
    return _create_faker(locale, seed).language_name()


def generate_boolean(locale="en_US", seed=None) -> bool:
    return _create_faker(locale, seed).boolean()


def generate_latlng(locale="en_US", seed=None) -> tuple:
    return _create_faker(locale, seed).latlng()


PROVIDERS: Dict[str, Any] = {
    "name": generate_name,
    "first_name": generate_first_name,
    "last_name": generate_last_name,
    "email": generate_email,
    "address": generate_address,
    "city": generate_city,
    "country": generate_country,
    "phone": generate_phone,
    "company": generate_company,
    "job": generate_job,
    "text": generate_text,
    "sentence": generate_sentence,
    "paragraph": generate_paragraph,
    "url": generate_url,
    "ipv4": generate_ipv4,
    "ipv6": generate_ipv6,
    "mac": generate_mac,
    "date": generate_date,
    "datetime": generate_datetime,
    "credit_card": generate_credit_card,
    "profile": generate_profile,
    "user_agent": generate_user_agent,
    "color": generate_color,
    "uuid": generate_uuid,
    "license_plate": generate_license_plate,
    "ssn": generate_ssn,
    "passport": generate_passport,
    "birthdate": generate_birthdate,
    "iban": generate_iban,
    "swift": generate_swift,
    "bban": generate_bban,
    "pricetag": generate_pricetag,
    "hostname": generate_hostname,
    "tld": generate_tld,
    "mime_type": generate_mime_type,
    "word": generate_word,
    "words": generate_words,
    "catch_phrase": generate_catch_phrase,
    "barcode": generate_barcode,
    "file_name": generate_file_name,
    "currency_code": generate_currency_code,
    "timezone": generate_timezone,
    "language": generate_language,
    "boolean": generate_boolean,
    "latlng": generate_latlng,
}


def generate(
    provider: str,
    locale: str,
    seed: Optional[int],
    quantity: int,
    kwargs: Optional[Dict[str, Any]] = None
) -> List[Any]:
    if provider not in PROVIDERS:
        raise ValueError(f"Unknown provider: {provider}")
    
    func = PROVIDERS[provider]
    kwargs = kwargs or {}

    return [func(locale, seed, **kwargs) for _ in range(quantity)]
