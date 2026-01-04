"""
Security Test 04: HTTPS & SSL/TLS Security
Проверява дали сайта използва правилно HTTPS и secure connections
"""

import pytest
from playwright.sync_api import Page
from POM import LoginPage, PaymentPage


@pytest.mark.security
def test_https_and_secure_connection(page: Page):
    """
    Проверява:
    1. Сайтът използва HTTPS
    2. Sensitive страници (login, payment) са през HTTPS
    3. Mixed content (HTTP ресурси в HTTPS страница)
    4. Secure cookies
    """
    login_page = LoginPage(page)

    # TEST 1: Homepage използва HTTPS
    page.goto(login_page.base_url)
    page.wait_for_load_state('networkidle')

    homepage_url = page.url
    assert homepage_url.startswith('https://'), f"Homepage not using HTTPS: {homepage_url}"
    print(f"✓ Homepage uses HTTPS: {homepage_url}")

    # TEST 2: Login page използва HTTPS
    login_page.navigate()
    login_url = page.url
    assert login_url.startswith('https://'), f"Login page not using HTTPS: {login_url}"
    print(f"✓ Login page uses HTTPS: {login_url}")

    # TEST 3: Провери за Mixed Content (HTTP resources в HTTPS page)
    mixed_content_detected = []
    insecure_requests = []

    def check_request(request):
        url = request.url
        if url.startswith('http://'):
            insecure_requests.append(url)
            # Ако е на същия домейн, това е mixed content
            if 'automationexercise.com' in url:
                mixed_content_detected.append(url)

    page.on('request', check_request)

    # Reload за да хванем всички requests
    page.reload()
    page.wait_for_load_state('networkidle')

    assert len(mixed_content_detected) == 0, \
        f"Mixed content detected (HTTP on HTTPS page): {mixed_content_detected}"

    if len(insecure_requests) > 0:
        print(f"⚠ Warning: {len(insecure_requests)} insecure external requests detected")
        for req in insecure_requests[:3]:  # Show first 3
            print(f"  - {req}")
    else:
        print("✓ No mixed content detected")

    # TEST 4: Payment page трябва да е HTTPS
    page.goto(f"{login_page.base_url}/payment")
    payment_url = page.url
    assert payment_url.startswith('https://'), f"Payment page not using HTTPS: {payment_url}"
    print(f"✓ Payment page uses HTTPS: {payment_url}")

    # TEST 5: Проверка на cookies за Secure flag
    cookies = page.context.cookies()

    insecure_cookies = []
    for cookie in cookies:
        # Session cookies трябва да имат Secure flag
        if 'session' in cookie['name'].lower() or 'token' in cookie['name'].lower():
            if not cookie.get('secure', False):
                insecure_cookies.append(cookie['name'])

    if len(insecure_cookies) > 0:
        print(f"⚠ Warning: Session cookies without Secure flag: {insecure_cookies}")
    else:
        print("✓ Session cookies have Secure flag")

    # TEST 6: Провери за HSTS header (HTTP Strict Transport Security)
    response = page.goto(login_page.base_url)
    headers = response.headers

    has_hsts = 'strict-transport-security' in headers
    if has_hsts:
        print(f"✓ HSTS header present: {headers['strict-transport-security']}")
    else:
        print("⚠ Warning: HSTS header not found")

    # TEST 7: Форми с sensitive data трябва да submit към HTTPS
    page.goto(f"{login_page.base_url}/login")
    page.wait_for_load_state('networkidle')

    form_action = page.locator('form').first.get_attribute('action')
    if form_action:
        if form_action.startswith('http:'):
            assert False, f"Form submits to insecure URL: {form_action}"
        print(f"✓ Form action is secure: {form_action or 'relative URL'}")

    print("✓ HTTPS & SSL/TLS Security Test PASSED")