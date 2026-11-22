"""Shared HTTP helper for the stdlib-only scripts (retry, back-off, Retry-After, per-host spacing).

Imported as a sibling module: ``python3 scripts/<script>.py`` puts ``scripts/`` on ``sys.path``.
"""
from __future__ import annotations

import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

USER_AGENT = "cancer-predisposition-variant-analyst/2.0 (+https://github.com/bloo-berries/cancer-predisposition-variant-analyst)"
MAX_RETRY_AFTER_S = 60.0

_last_request: dict[str, float] = {}


@dataclass
class Response:
    status: int
    body: bytes
    headers: dict[str, str]
    url: str

    def text(self) -> str:
        return self.body.decode("utf-8", "replace")


def retry_after_seconds(value: str | None, default: float) -> float:
    """Parse a Retry-After header (delta-seconds or HTTP-date); never raises."""
    if not value:
        return default
    value = value.strip()
    try:
        secs = float(value)
    except ValueError:
        try:
            when = parsedate_to_datetime(value)
        except (TypeError, ValueError, IndexError):
            return default
        if when.tzinfo is None:
            when = when.replace(tzinfo=timezone.utc)
        secs = (when - datetime.now(timezone.utc)).total_seconds()
    return min(max(secs, 0.0), MAX_RETRY_AFTER_S)


def _space(host: str, min_interval: float | None) -> None:
    if not min_interval:
        return
    wait = _last_request.get(host, 0.0) + min_interval - time.monotonic()
    if wait > 0:
        time.sleep(wait)


def request(
    url: str,
    *,
    method: str = "GET",
    data: bytes | None = None,
    headers: dict[str, str] | None = None,
    timeout: float = 30,
    retries: int = 3,
    retry_on: tuple[int, ...] = (429, 500, 502, 503, 504),
    honour_retry_after: bool = True,
    min_interval: float | None = None,
) -> Response:
    """Perform one HTTP request with up to ``retries`` further attempts.

    Retries on the status codes in ``retry_on`` (sleeping ``Retry-After`` when present and
    honoured, else 1.5 s x attempt) and on ``URLError``/timeouts. ``min_interval`` spaces
    successive requests to the same host (seconds). Raises ``urllib.error.HTTPError`` for a
    non-retryable or still-failing status and ``urllib.error.URLError``/``TimeoutError`` when
    the network stays down.
    """
    host = urllib.parse.urlparse(url).hostname or url
    hdrs = {"User-Agent": USER_AGENT, "Accept": "*/*", **(headers or {})}
    attempt = 0
    while True:
        _space(host, min_interval)
        req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = b"" if method == "HEAD" else resp.read()
                _last_request[host] = time.monotonic()
                return Response(resp.status, body, dict(resp.headers.items()), resp.geturl())
        except urllib.error.HTTPError as e:
            _last_request[host] = time.monotonic()
            if e.code in retry_on and attempt < retries:
                default = 1.5 * (attempt + 1)
                time.sleep(retry_after_seconds(e.headers.get("Retry-After"), default) if honour_retry_after else default)
                attempt += 1
                continue
            raise
        except (urllib.error.URLError, TimeoutError):
            _last_request[host] = time.monotonic()
            if attempt < retries:
                time.sleep(1.5 * (attempt + 1))
                attempt += 1
                continue
            raise
