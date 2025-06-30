import logging
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
from typing import Any

def init_logging(log_level: int = logging.INFO) -> None:
    """
    Initialize the root logger with a console handler.

    :param log_level: Logging level (e.g., logging.DEBUG, logging.INFO)
    """
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def normalize_url(url: str) -> str:
    """
    Normalize a URL by applying the following rules:
    1. Lower-case scheme and host, strip leading "www.".
    2. Remove URL path parameters such as ";jsessionid=…".
    3. Remove trailing slashes from the path.
    4. Remove common tracking query parameters (utm_*, ref, gclid, fbclid, etc.).
    5. Remove common session identifiers from query (phpsessid, jsessionid, asp.net_sessionid, etc.).
    6. Sort the remaining query parameters for a stable ordering.
    :param url: The URL to normalize.
    :return: Normalized URL.
    """
    parsed = urlparse(url)

    # 1. Canonicalise scheme and host
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]

    # 2. Remove path parameters (matrix parameters) such as ";jsessionid=…"
    path = parsed.path
    if ";" in path:
        path = path.split(";")[0]
    # 3. Remove trailing slash entirely, including for root path
    path = path.rstrip("/")

    # 4 & 5. Filter query parameters
    TRACKING_PREFIXES = ("utm_",)
    TRACKING_PARAMS = {
        "ref",
        "gclid",
        "fbclid",
        "fb_source",
        "igshid",
    }
    SESSION_PARAMS = {
        "phpsessid",
        "jsessionid",
        "sessionid",
        "sid",
        "asp.net_sessionid",
    }

    filtered_qsl = [
        (k.lower(), v)
        for k, v in parse_qsl(parsed.query, keep_blank_values=True)
        if (
            k.lower() not in TRACKING_PARAMS
            and k.lower() not in SESSION_PARAMS
            and not any(k.lower().startswith(prefix) for prefix in TRACKING_PREFIXES)
        )
    ]

    # 6. Sort remaining params for stability
    query = urlencode(sorted(filtered_qsl))

    # Fragment is deliberately dropped.
    normalized = urlunparse((scheme, netloc, path, "", query, ""))
    return normalized
