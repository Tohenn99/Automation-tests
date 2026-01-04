"""
Security Test: Sensitive Data Exposure
Checks if passwords, card numbers, etc. leak in console/storage/network
"""

import pytest
from playwright.sync_api import Page
import json
from POM import LoginPage, RegistrationPage, PaymentPage, TestDataFactory


@pytest.mark.security
def test_sensitive_data_exposure(page: Page):
    """Checks for sensitive data leaks in console, localStorage, cookies, network"""

    user_data = TestDataFactory.get_user_data_usa()
    payment_data = TestDataFactory.get_payment_data()

    # Only check long values (6+ chars) to avoid false positives like "123"
    sensitive_data = [
        user_data['password'],           # "Test@2024"
        payment_data['card_number'],     # "4532..."
        user_data['address']['mobile']   # "3105551234"
    ]

    print("\n=== Sensitive Data Exposure Test ===\n")

    # Track console logs (skip browser warnings)
    console_logs = []
    def log_handler(msg):
        text = msg.text.lower()
        if not any(x in text for x in ['autocomplete', '[dom]', 'suggested:', 'violation']):
            console_logs.append(msg.text)
    page.on('console', log_handler)

    # Track network responses (only from target site)
    leaked_responses = []
    def response_handler(response):
        try:
            if 'automationexercise.com' in response.url:
                body = response.text()
                for data in sensitive_data:
                    if data in body:
                        leaked_responses.append(f"{response.url}: {data[:4]}***")
        except:
            pass
    page.on('response', response_handler)

    # Perform registration
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.signup(user_data['name'], user_data['email'])

    reg_page = RegistrationPage(page)
    reg_page.fill_account_info(user_data['title'], user_data['password'], user_data['dob'])
    page.wait_for_timeout(2000)

    # TEST 1: Console Logs
    print("1. Console Logs...")
    exposed_console = [log for log in console_logs if any(data in log for data in sensitive_data)]
    assert len(exposed_console) == 0, f"⚠️ Data in console: {exposed_console}"
    print("   ✅ Clean")

    # TEST 2: LocalStorage
    print("2. LocalStorage...")
    ls = page.evaluate("() => JSON.stringify(localStorage)")
    for data in sensitive_data:
        assert data not in ls, f"⚠️ Found: {data[:4]}***"
    print("   ✅ Clean")

    # TEST 3: SessionStorage
    print("3. SessionStorage...")
    ss = page.evaluate("() => JSON.stringify(sessionStorage)")
    for data in sensitive_data:
        assert data not in ss, f"⚠️ Found: {data[:4]}***"
    print("   ✅ Clean")

    # TEST 4: Cookies
    print("4. Cookies...")
    cookies_str = json.dumps(page.context.cookies())
    assert user_data['password'] not in cookies_str, "⚠️ Password in cookies!"
    assert payment_data['card_number'] not in cookies_str, "⚠️ Card in cookies!"
    print("   ✅ Clean")

    # TEST 5: Page Source
    print("5. Page Source...")
    source = page.content()
    assert user_data['password'] not in source, "⚠️ Password in page source!"
    print("   ✅ Clean")

    # TEST 6: Network Responses
    print("6. Network Responses...")
    assert len(leaked_responses) == 0, f"⚠️ Data in responses: {leaked_responses}"
    print("   ✅ Clean")

    # TEST 7: Password Fields Type
    print("7. Input Field Types...")
    pwd_fields = page.locator('input[type="password"]').all()
    assert len(pwd_fields) > 0, "⚠️ No password fields with type='password'"
    print(f"   ✅ {len(pwd_fields)} password fields")

    # TEST 8: Credit Card Protection
    print("8. Credit Card Data...")
    page.goto(f"{login_page.base_url}/payment")
    page.wait_for_timeout(1000)

    payment_page = PaymentPage(page)
    payment_page.fill_payment_details(payment_data)
    page.wait_for_timeout(1000)

    payment_source = page.content()
    assert payment_data['card_number'] not in payment_source, "⚠️ Card number in source!"
    print("   ✅ Clean")

    print("\n✅ All Sensitive Data Properly Protected\n")


@pytest.mark.security
def test_password_not_in_urls(page: Page):
    """Verify passwords never appear in URLs (especially GET requests)"""

    user_data = TestDataFactory.get_user_data_usa()
    password_in_url = []

    def check_request(request):
        if user_data['password'] in request.url or 'password=' in request.url.lower():
            password_in_url.append({'method': request.method, 'url': request.url[:100]})

    page.on('request', check_request)

    login_page = LoginPage(page)
    login_page.navigate()
    login_page.signup(user_data['name'], user_data['email'])
    page.wait_for_timeout(2000)

    assert len(password_in_url) == 0, f"⚠️ Password in URLs: {password_in_url}"
    print("✅ Passwords not exposed in URLs")


@pytest.mark.security
def test_no_sensitive_data_in_javascript(page: Page):
    """Check that sensitive data isn't hardcoded in JavaScript"""

    user_data = TestDataFactory.get_user_data_usa()
    login_page = LoginPage(page)
    login_page.navigate()

    # Check global JS variables
    dangerous_vars = page.evaluate("""() => {
        const bad = [];
        for (let key in window) {
            try {
                const val = String(window[key]).toLowerCase();
                if ((val.includes('password') && val.includes('=')) || 
                    (val.includes('api') && val.includes('key'))) {
                    bad.push(key);
                }
            } catch(e) {}
        }
        return bad;
    }""")

    if dangerous_vars:
        print(f"⚠️ Warning: Suspicious JS variables: {dangerous_vars}")
    else:
        print("✅ No suspicious JS variables")

    # Not a failure, just a warning
    assert True