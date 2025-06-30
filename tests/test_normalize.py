import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import pytest

from spider.utils import normalize_url

@pytest.mark.parametrize(
    "raw,expected",
    [
        # Lower-case host and scheme + remove trailing slash
        (
            "HTTPS://Example.COM/path/",
            "https://example.com/path",
        ),
        # Strip www subdomain
        (
            "https://www.example.com/",
            "https://example.com",
        ),
        # Remove tracking params (utm_*) and sort remaining
        (
            "https://example.com/?b=2&utm_source=newsletter&a=1",
            "https://example.com?a=1&b=2",
        ),
        # Remove fixed tracking params (gclid, fbclid, ref)
        (
            "https://example.com/page?ref=twitter&gclid=123&x=1",
            "https://example.com/page?x=1",
        ),
        # Remove session params in query
        (
            "https://example.com/?PHPSESSID=42&foo=bar",
            "https://example.com?foo=bar",
        ),
        # Remove session id in path (jsessionid)
        (
            "https://example.com/page;jsessionid=ABCDEF123?x=1",
            "https://example.com/page?x=1",
        ),
        # Combine several rules
        (
            "https://WWW.EXAMPLE.com/path/;JSESSIONID=xyz?utm_medium=email&sid=33&B=2&a=1#section",
            "https://example.com/path?a=1&b=2",
        ),
        # No query should still work
        (
            "https://example.com",
            "https://example.com",
        ),
        # Root path with slash preserved (should remove trailing slash though)
        (
            "https://example.com/",
            "https://example.com",
        ),
    ],
)

def test_normalize_url(raw, expected):
    assert normalize_url(raw) == expected
