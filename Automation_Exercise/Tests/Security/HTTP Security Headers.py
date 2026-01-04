"""
Security Test 05: HTTP Security Headers
Проверява наличието и правилната конфигурация на security headers
"""

import pytest
from playwright.sync_api import Page
from POM import LoginPage


@pytest.mark.security
def test_http_security_headers(page: Page):
    """
    Проверява critical HTTP security headers:
    1. X-Frame-Options (Clickjacking protection)
    2. X-Content-Type-Options (MIME sniffing protection)
    3. X-XSS-Protection (XSS filter)
    4. Content-Security-Policy (CSP)
    5. Referrer-Policy
    6. Permissions-Policy
    """
    login_page = LoginPage(page)

    # Направи request и вземи headers
    response = page.goto(login_page.base_url)
    page.wait_for_load_state('networkidle')

    headers = {k.lower(): v for k, v in response.headers.items()}

    print(f"\n=== HTTP Security Headers Analysis ===")
    print(f"URL: {response.url}\n")

    security_score = 0
    max_score = 8

    # TEST 1: X-Frame-Options (Clickjacking protection)
    x_frame = headers.get('x-frame-options', '').upper()
    if x_frame in ['DENY', 'SAMEORIGIN']:
        print(f"✓ X-Frame-Options: {x_frame} (SECURE)")
        security_score += 1
    else:
        print(f"✗ X-Frame-Options: {x_frame or 'MISSING'} (VULNERABLE to clickjacking)")
        print("  Recommendation: Set to 'DENY' or 'SAMEORIGIN'")

    # TEST 2: X-Content-Type-Options (MIME sniffing protection)
    x_content_type = headers.get('x-content-type-options', '').lower()
    if x_content_type == 'nosniff':
        print(f"✓ X-Content-Type-Options: nosniff (SECURE)")
        security_score += 1
    else:
        print(f"✗ X-Content-Type-Options: {x_content_type or 'MISSING'} (VULNERABLE)")
        print("  Recommendation: Set to 'nosniff'")

    # TEST 3: X-XSS-Protection (Legacy XSS filter)
    x_xss = headers.get('x-xss-protection', '')
    if x_xss:
        print(f"✓ X-XSS-Protection: {x_xss}")
        security_score += 0.5
    else:
        print(f"⚠ X-XSS-Protection: MISSING (Legacy header, CSP is better)")

    # TEST 4: Content-Security-Policy (Most important!)
    csp = headers.get('content-security-policy', '')
    if csp:
        print(f"✓ Content-Security-Policy: PRESENT")
        print(f"  Policy: {csp[:100]}...")
        security_score += 2

        # Провери за unsafe directives
        if 'unsafe-inline' in csp:
            print("  ⚠ Warning: 'unsafe-inline' found in CSP (reduces protection)")
        if 'unsafe-eval' in csp:
            print("  ⚠ Warning: 'unsafe-eval' found in CSP (reduces protection)")
    else:
        print(f"✗ Content-Security-Policy: MISSING (HIGH RISK)")
        print("  Recommendation: Implement strict CSP")

    # TEST 5: Strict-Transport-Security (HSTS)
    hsts = headers.get('strict-transport-security', '')
    if hsts:
        print(f"✓ Strict-Transport-Security: {hsts}")
        security_score += 1

        # Провери за includeSubDomains
        if 'includesubdomains' in hsts.lower():
            print("  ✓ includeSubDomains is set")
            security_score += 0.5
    else:
        print(f"✗ Strict-Transport-Security: MISSING")
        print("  Recommendation: Set HSTS with max-age=31536000")

    # TEST 6: Referrer-Policy
    referrer = headers.get('referrer-policy', '')
    if referrer:
        print(f"✓ Referrer-Policy: {referrer}")
        security_score += 1
    else:
        print(f"⚠ Referrer-Policy: MISSING")
        print("  Recommendation: Set to 'no-referrer' or 'strict-origin-when-cross-origin'")

    # TEST 7: Permissions-Policy (formerly Feature-Policy)
    permissions = headers.get('permissions-policy', '')
    feature_policy = headers.get('feature-policy', '')

    if permissions or feature_policy:
        print(f"✓ Permissions-Policy: {permissions or feature_policy}")
        security_score += 1
    else:
        print(f"⚠ Permissions-Policy: MISSING")
        print("  Recommendation: Restrict dangerous features (camera, microphone, geolocation)")

    # TEST 8: Провери за information disclosure headers
    dangerous_headers = []

    if 'server' in headers:
        server_header = headers['server']
        if any(char.isdigit() for char in server_header):
            dangerous_headers.append(f"Server: {server_header}")

    if 'x-powered-by' in headers:
        dangerous_headers.append(f"X-Powered-By: {headers['x-powered-by']}")

    if dangerous_headers:
        print(f"\n⚠ Information Disclosure Headers Found:")
        for h in dangerous_headers:
            print(f"  - {h}")
        print("  Recommendation: Remove version information")
    else:
        print(f"\n✓ No information disclosure headers")
        security_score += 1

    # Финален резултат
    print(f"\n{'=' * 50}")
    print(f"Security Headers Score: {security_score}/{max_score}")
    print(f"Rating: ", end='')

    if security_score >= 7:
        print("EXCELLENT 🟢")
    elif security_score >= 5:
        print("GOOD 🟡")
    elif security_score >= 3:
        print("FAIR 🟠")
    else:
        print("POOR 🔴")

    print(f"{'=' * 50}\n")

    # Assertion - минимум 3 от 8 точки
    assert security_score >= 3, \
        f"Security headers insufficient: {security_score}/{max_score}"

    print("✓ HTTP Security Headers Test COMPLETED")