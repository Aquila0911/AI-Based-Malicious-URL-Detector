import re
from urllib.parse import unquote
import html

def test_xss(url):
    # First decode the URL to handle encoded attacks
    try:
        decoded_url = unquote(url)
        decoded_url = html.unescape(decoded_url)
    except Exception:
        decoded_url = url

    # Extended patterns for XSS detection
    xss_patterns = {
        'script_tags': r'<script.?>.?</script>',
        'javascript_protocol': r'javascript:|vbscript:|data:',
        'event_handlers': r'on\w+\s*=',
        'hex_encoded': r'&#x[0-9a-f]+;|\\x[0-9a-f]+',
        'encoded_tags': r'(%3C|&lt;).?(script|img|svg|iframe).?(%3E|&gt;)',
        'alert_prompt': r'(alert|prompt|confirm|console\.|eval)\s*\(',
        'svg_onload': r'<svg.?onload\s=',
        'img_onerror': r'<img.?onerror\s=',
        'dangerous_attributes': r'(href|src|action)\s*=\s*["\'].*?(javascript|data):',
        'base64_injection': r'base64[^<]\([^<]\)',
        'expression': r'expression\s*\(',
        'meta_refresh': r'<meta[^>]url\s=',
        'double_encoded': r'%25[0-9a-f]{2}'
    }
    
    matches_found = []
    
    for pattern_name, pattern in xss_patterns.items():
        if re.search(pattern, decoded_url, re.IGNORECASE):
            matches_found.append(pattern_name)
    
    return bool(matches_found), matches_found

# USE CASE:
# http://example.com/?test=<script>alert('XSS')</script>