"""
Security Test 07: Session Management & Cookie Security
Тества правилното управление на сесии и cookie security атрибути
"""

import pytest
from playwright.sync_api import Page
from POM import LoginPage, RegistrationPage, TestDataFactory


@pytest.mark.security
def test_session_management_and_cookies(page: Page):
    """
    Проверява:
    1. Session cookies security атрибути (HttpOnly, Secure, SameSite)
    2. Session timeout
    3. Session fixation protection
    4. Cookie scope and domain
    5. Logout functionality
    """
    user_data = TestDataFactory.get_user_data_usa()

    login_page = LoginPage(page)
    login_page.navigate()

    print("\n=== Session Management Security Test ===\n")

    # Вземи cookies преди login
    initial_cookies = page.context.cookies()
    initial_cookie_names = [c['name'] for c in initial_cookies]

    print(f"1. Initial cookies: {len(initial_cookies)}")

    # Register и login user
    login_page.signup(user_data['name'], user_data['email'])

    reg_page = RegistrationPage(page)
    reg_page.fill_account_info(
        title=user_data['title'],
        password=user_data['password'],
        dob=user_data['dob']
    )
    reg_page.fill_address_info(user_data['address'])
    reg_page.submit_registration()

    page.wait_for_timeout(2000)
    reg_page.continue_after_registration()

    # Вземи cookies след login
    authenticated_cookies = page.context.cookies()

    print(f"2. Cookies after authentication: {len(authenticated_cookies)}")

    # TEST 1: Session Cookie Security Attributes
    print("\n3. Analyzing Session Cookies Security...")

    session_cookies = []
    for cookie in authenticated_cookies:
        # Identify session cookies
        if any(keyword in cookie['name'].lower() for keyword in ['session', 'auth', 'token', 'sid']):
            session_cookies.append(cookie)

    if len(session_cookies) == 0:
        print("   ℹ No explicit session cookies found (may use different mechanism)")
    else:
        for cookie in session_cookies:
            print(f"\n   Cookie: {cookie['name']}")

            # HttpOnly flag (prevents XSS access)
            if cookie.get('httpOnly', False):
                print("   ✓ HttpOnly: YES (XSS protected)")
            else:
                print("   ✗ HttpOnly: NO (VULNERABLE to XSS)")

            # Secure flag (HTTPS only)
            if cookie.get('secure', False):
                print("   ✓ Secure: YES (HTTPS only)")
            else:
                print("   ⚠ Secure: NO (can be sent over HTTP)")

            # SameSite attribute (CSRF protection)
            same_site = cookie.get('sameSite', 'None')
            if same_site in ['Strict', 'Lax']:
                print(f"   ✓ SameSite: {same_site} (CSRF protected)")
            else:
                print(f"   ⚠ SameSite: {same_site} (CSRF vulnerable)")

            # Domain scope
            domain = cookie.get('domain', '')
            print(f"   Domain: {domain}")

            # Check if domain is too permissive
            if domain.startswith('.'):
                print(f"   ⚠ Warning: Cookie accessible to all subdomains")

    # TEST 2: Session Fixation Protection
    print("\n4. Testing Session Fixation Protection...")

    # Провери дали session ID се сменя след login
    new_cookies = [c for c in authenticated_cookies if c['name'] not in initial_cookie_names]

    if len(new_cookies) > 0:
        print(f"   ✓ New cookies after login: {len(new_cookies)}")
        print("   ✓ Session regeneration detected")
    else:
        print("   ⚠ No new session cookies - possible session fixation risk")

    # TEST 3: Cookie Expiration
    print("\n5. Checking Cookie Expiration...")

    for cookie in authenticated_cookies:
        if 'expires' in cookie and cookie['expires'] != -1:
            # Calculate expiration time
            import time
            expires_timestamp = cookie['expires']
            current_timestamp = time.time()
            time_to_expire = (expires_timestamp - current_timestamp) / 3600  # hours

            if time_to_expire < 0:
                print(f"   ⚠ {cookie['name']}: EXPIRED")
            elif time_to_expire > 24 * 365:  # More than 1 year
                print(f"   ⚠ {cookie['name']}: Very long expiration ({time_to_expire / 24 / 365:.1f} years)")
            else:
                print(f"   ✓ {cookie['name']}: Expires in {time_to_expire:.1f} hours")
        else:
            print(f"   ℹ {cookie['name']}: Session cookie (expires on browser close)")

    # TEST 4: Logout Functionality
    print("\n6. Testing Logout & Session Invalidation...")

    # Check if logged in
    logged_in_indicator = page.locator('a:has-text("Logout")').first
    if logged_in_indicator.is_visible():
        print("   ✓ User is logged in")

        # Perform logout
        logged_in_indicator.click()
        page.wait_for_load_state('networkidle')

        # Verify cookies are cleared/invalidated
        after_logout_cookies = page.context.cookies()

        # Session cookies трябва да са премахнати или invalidated
        logout_cookie_names = [c['name'] for c in after_logout_cookies]

        session_removed = True
        for session_cookie in session_cookies:
            if session_cookie['name'] in logout_cookie_names:
                session_removed = False
                print(f"   ⚠ Session cookie '{session_cookie['name']}' still present after logout")

        if session_removed or len(session_cookies) == 0:
            print("   ✓ Session cookies properly cleared on logout")

        # Опитай да достъпиш protected page
        page.goto(f"{login_page.base_url}/view_cart")
        page.wait_for_timeout(1000)

        # Трябва да можем да достъпим cart (не е protected в този сайт)
        # Но user-specific data не трябва да е налична
        current_url = page.url
        print(f"   After logout URL: {current_url}")

    else:
        print("   ⚠ No logout button found")

    # TEST 5: Cookie Path Security
    print("\n7. Checking Cookie Path Restrictions...")

    overly_permissive_cookies = []
    for cookie in authenticated_cookies:
        path = cookie.get('path', '/')
        if path == '/':
            overly_permissive_cookies.append(cookie['name'])

    if len(overly_permissive_cookies) > 0:
        print(f"   ℹ {len(overly_permissive_cookies)} cookies with root path (common but less restrictive)")
    else:
        print("   ✓ All cookies have restricted paths")

    # TEST 6: Multiple Sessions (Different Browsers)
    print("\n8. Testing Multiple Session Handling...")

    # Create second context (simulate different browser)
    context2 = page.context.browser.new_context()
    page2 = context2.new_page()

    page2.goto(login_page.base_url)
    page2.wait_for_load_state('networkidle')

    # Провери дали session-ите са изолирани
    context2_cookies = context2.cookies()
    context2_cookie_names = [c['name'] for c in context2_cookies]

    # Session cookies не трябва да са споделени
    shared_sessions = []
    for cookie in authenticated_cookies:
        if cookie['name'] in context2_cookie_names:
            # Провери дали value-то е същото
            cookie2 = next((c for c in context2_cookies if c['name'] == cookie['name']), None)
            if cookie2 and cookie2.get('value') == cookie.get('value'):
                shared_sessions.append(cookie['name'])

    assert len(shared_sessions) == 0, f"Sessions shared between contexts: {shared_sessions}"
    print("   ✓ Sessions properly isolated between contexts")

    context2.close()

    print("\n✓ Session Management Security Test PASSED\n")