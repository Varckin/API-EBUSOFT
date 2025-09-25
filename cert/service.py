import asyncio
import math
from typing import Iterable, List, Set
from urllib.parse import urlencode

import httpx

from cert.models import CrtShRawItem, CrtShItem
from cert.settings import settings


def _build_query(domain: str, exact: bool, include_expired: bool) -> str:
    """
    Build query string for site.
    exact=True  -> q=<domain>
    exact=False -> q=%.<domain> (subdomains). In URL '%' is encoded as '%25'.
    Public crt.sh doesn't have 'exclude expired' filter - filtered by application if needed.
    """
    q = domain.strip()
    if not exact:
        if not q.startswith("*.") and not q.startswith("%.") and not q.startswith("%."):
            q = f"%.{q.lstrip('.')}"
    params = {"q": q, "output": "json"}
    return f"/?{urlencode(params)}"


def _split_names(name_value: str) -> List[str]:
    """Split name_value by newlines, clean and remove duplicates."""
    parts = [p.strip() for p in (name_value or "").split("\n")]
    seen: Set[str] = set()
    out: List[str] = []
    for p in parts:
        if p and p not in seen:
            out.append(p)
            seen.add(p)
    return out


def normalize(raw: Iterable[CrtShRawItem]) -> List[CrtShItem]:
    """Deduplicate by id and normalize name list."""
    out: List[CrtShItem] = []
    seen_ids: Set[int] = set()

    for r in raw:
        if r.id is None:
            # In practice id is almost always present, but just in case.
            continue
        if r.id in seen_ids:
            continue
        seen_ids.add(r.id)

        names = _split_names(r.name_value or "") if settings.split_names else []

        out.append(
            CrtShItem(
                id=r.id,
                common_name=r.common_name,
                names=names,
                issuer_name=r.issuer_name,
                entry_timestamp=r.entry_timestamp,
                not_before=r.not_before,
                not_after=r.not_after,
                serial_number=r.serial_number,
            )
        )
        if len(out) >= settings.max_records:
            break

    return out


async def fetch_crtsh(domain: str, exact: bool, include_expired: bool) -> List[CrtShItem]:
    """
    Async request to site with exponential retries and response normalization.
    """
    url_path = _build_query(domain, exact, include_expired)

    timeout = httpx.Timeout(
        connect=settings.connect_timeout_s,
        read=settings.read_timeout_s,
        write=settings.write_timeout_s,
        pool=settings.pool_timeout_s,
    )
    limits = httpx.Limits(
        max_keepalive_connections=settings.max_keepalive_connections,
        max_connections=settings.max_connections,
    )
    headers = {
        "User-Agent": settings.user_agent,
        "Accept": "application/json",
    }

    attempt = 0
    last_exc: Exception | None = None

    async with httpx.AsyncClient(
        base_url=str(settings.crt_base),
        timeout=timeout,
        headers=headers,
        limits=limits,
        http2=True,
        follow_redirects=True,
    ) as client:
        while attempt <= settings.retries:
            try:
                resp = await client.get(url_path)
                # Retry upstream overload/errors
                if resp.status_code >= 500 or resp.status_code == 429:
                    raise httpx.HTTPStatusError(
                        f"Upstream returned {resp.status_code}",
                        request=resp.request,
                        response=resp,
                    )
                resp.raise_for_status()
                data = resp.json()
                if isinstance(data, dict):
                    data = [data]
                raw_items = [CrtShRawItem.model_validate(item) for item in data]
                return normalize(raw_items)

            except (httpx.TimeoutException, httpx.NetworkError, httpx.HTTPStatusError) as e:
                last_exc = e
                if attempt == settings.retries:
                    break
                backoff = settings.initial_backoff_s * math.pow(2, attempt)
                await asyncio.sleep(backoff)
                attempt += 1

    assert last_exc is not None
    raise last_exc
