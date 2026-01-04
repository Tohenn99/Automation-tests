"""
Security Test 01: XSS (Cross-Site Scripting) Protection
Tests if signup and registration fields are protected from XSS attacks
"""

import pytest
from playwright.sync_api import Page
from POM import LoginPage, RegistrationPage, TestDataFactory


@pytest.mark.security
def test_xss_protection_in_registration_fields(page: Page):
    """
    Verifies all input fields properly sanitize XSS payloads
    Covers: signup form, registration form, address fields
    """
    login_page = LoginPage(page)
    login_page.navigate()

    # XSS payloads for testing
    xss_payloads = [
        "<script>alert('XSS')</script>",
        "<img src=x onerror=alert('XSS')>",
        "javascript:alert('XSS')",
        "<svg onload=alert('XSS')>",
        "';alert(String.fromCharCode(88,83,83))//",
        "<iframe src='javascript:alert(1)'></iframe>",
        "<body onload=alert('XSS')>",
    ]

    # Track if any XSS dialogs appear
    dialogs_triggered = []
    page.on("dialog", lambda dialog: dialogs_triggered.append(dialog.message))

    for payload in xss_payloads:
        # Test 1: XSS in signup name field
        page.locator(login_page.SIGNUP_NAME).fill(payload)
        page.locator(login_page.SIGNUP_EMAIL).fill("test@example.com")

        # Get only the form content, not entire page with ads
        form_content = page.locator('.signup-form').inner_html()

        # Check for injected malicious content in FORM only
        assert not _contains_malicious_content(form_content, payload), \
            f"XSS vulnerability detected in name field with payload: {payload}"

        # Test 2: XSS in email field
        page.locator(login_page.SIGNUP_NAME).fill("Normal Name")
        page.locator(login_page.SIGNUP_EMAIL).fill(payload + "@test.com")

        form_content = page.locator('.signup-form').inner_html()
        assert not _contains_malicious_content(form_content, payload), \
            f"XSS vulnerability detected in email field with payload: {payload}"

        # Clear fields
        page.reload()
        page.wait_for_load_state('networkidle')

    # Final check - submit with XSS payload and verify no execution
    page.locator(login_page.SIGNUP_NAME).fill("<script>alert('HACKED')</script>")
    page.locator(login_page.SIGNUP_EMAIL).fill(TestDataFactory.generate_email())

    # Click signup - if XSS works, dialog will trigger
    page.locator(login_page.SIGNUP_BUTTON).click()
    page.wait_for_timeout(2000)

    assert len(dialogs_triggered) == 0, \
        f"⚠️ CRITICAL: XSS EXECUTED! Alert dialogs triggered: {dialogs_triggered}"

    print("✅ XSS Protection Test PASSED - All inputs properly sanitized")


def _contains_malicious_content(html: str, payload: str) -> bool:
    """
    Check if HTML contains unescaped malicious patterns from the payload
    Ignores legitimate third-party scripts (Google Ads, Analytics, etc.)
    """
    dangerous_patterns = [
        "<script>",
        "onerror=",
        "onload=",
        "javascript:",
        "<svg",
        "<iframe src='javascript:",  # Only check OUR injected iframe
    ]

    # Check if payload appears unescaped
    for pattern in dangerous_patterns:
        if pattern in payload.lower() and pattern in html.lower():
            # Additional check: ensure it's not just HTML-encoded
            if payload.replace("<", "&lt;").replace(">", "&gt;") not in html:
                return True

    return False


@pytest.mark.security
def test_xss_protection_in_registration_form(page: Page):
    """
    Test XSS protection in full registration flow
    """
    login_page = LoginPage(page)
    reg_page = RegistrationPage(page)

    login_page.navigate()

    # Generate user with XSS payloads
    xss_name = "<img src=x onerror=alert('XSS')>"
    user_data = TestDataFactory.get_user_data_usa()
    user_data['name'] = xss_name

    # Attempt signup
    login_page.signup(xss_name, user_data['email'])

    # Wait for registration page
    try:
        page.wait_for_selector('#form', timeout=5000)
    except:
        pass

    # Check if XSS payload appears on registration page
    page_content = page.locator('#form').inner_html()

    # Verify payload is escaped
    assert "<img src=x" not in page_content, \
        "XSS payload not sanitized on registration page!"

    # Verify escaped version exists
    assert ("&lt;img" in page_content or
            xss_name not in page_content), \
        "XSS protection check inconclusive"

    print("✅ Registration form XSS protection verified")


@pytest.mark.security
def test_xss_protection_address_fields(page: Page):
    """
    Test XSS protection in address fields during registration
    """
    login_page = LoginPage(page)
    reg_page = RegistrationPage(page)

    # Complete signup
    user_data = TestDataFactory.get_user_data_usa()
    login_page.navigate()
    login_page.signup(user_data['name'], user_data['email'])

    page.wait_for_selector('#form')

    # Fill account info normally
    reg_page.fill_account_info(
        title=user_data['title'],
        password=user_data['password'],
        dob=user_data['dob']
    )

    # Inject XSS in address fields
    malicious_address = user_data['address'].copy()
    malicious_address['address1'] = "<script>alert('XSS')</script>"
    malicious_address['city'] = "';alert('XSS');//"
    malicious_address['company'] = "<svg onload=alert('XSS')>"

    # Track dialogs
    dialogs = []
    page.on("dialog", lambda d: dialogs.append(d.message))

    # Fill malicious address data
    reg_page.fill_address_info(malicious_address)

    # Submit
    reg_page.submit_registration()
    page.wait_for_timeout(2000)

    # Verify no XSS execution
    assert len(dialogs) == 0, \
        f"⚠️ CRITICAL: XSS in address fields! Dialogs: {dialogs}"

    # Check page source doesn't contain unescaped payloads
    page_source = page.content()

    assert "<script>alert" not in page_source, \
        "Address1 field vulnerable to XSS"
    assert "';alert(" not in page_source, \
        "City field vulnerable to XSS"
    assert "<svg onload" not in page_source, \
        "Company field vulnerable to XSS"

    print("✅ Address fields XSS protection verified")


@pytest.mark.security
def test_dom_based_xss_protection(page: Page):
    """
    Test protection against DOM-based XSS via URL parameters
    """
    login_page = LoginPage(page)

    # Try XSS via URL parameter
    xss_url = f"{login_page.base_url}/login?name=<script>alert('XSS')</script>"

    dialogs = []
    page.on("dialog", lambda d: dialogs.append(d.message))

    page.goto(xss_url)
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(2000)

    assert len(dialogs) == 0, \
        f"⚠️ DOM-based XSS vulnerability! Dialogs: {dialogs}"

    # Verify parameter is sanitized if reflected
    page_content = page.content()
    assert "<script>" not in page_content, \
        "URL parameter XSS not sanitized"

    print("✅ DOM-based XSS protection verified")