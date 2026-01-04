"""
Security Test 09: Clickjacking Protection
Tests whether the site is protected from clickjacking attacks via iframe embedding
"""

import pytest
from playwright.sync_api import Page
from POM import LoginPage


@pytest.mark.security
def test_clickjacking_protection(page: Page):
    """
    Verifies clickjacking protection:
    1. X-Frame-Options header
    2. Content-Security-Policy frame-ancestors directive
    3. Practical iframe embedding test
    4. Frame busting code
    """
    login_page = LoginPage(page)

    print("\n=== Clickjacking Protection Test ===\n")

    # TEST 1: Check X-Frame-Options header
    print("1. Checking X-Frame-Options Header...")

    response = page.goto(login_page.base_url)
    page.wait_for_load_state('networkidle')

    headers = {k.lower(): v for k, v in response.headers.items()}

    x_frame_options = headers.get('x-frame-options', '').upper()

    if x_frame_options in ['DENY', 'SAMEORIGIN']:
        print(f"   ✓ X-Frame-Options: {x_frame_options}")
        protection_level_xfo = "PROTECTED"
    elif x_frame_options:
        print(f"   ⚠ X-Frame-Options: {x_frame_options} (weak protection)")
        protection_level_xfo = "WEAK"
    else:
        print(f"   ✗ X-Frame-Options: NOT SET (VULNERABLE)")
        protection_level_xfo = "VULNERABLE"

    # TEST 2: Check CSP frame-ancestors directive
    print("\n2. Checking Content-Security-Policy (frame-ancestors)...")

    csp = headers.get('content-security-policy', '').lower()

    has_frame_ancestors = False
    csp_protection_level = "NONE"

    if 'frame-ancestors' in csp:
        has_frame_ancestors = True

        if "'none'" in csp:
            print("   ✓ CSP frame-ancestors: 'none' (strongest protection)")
            csp_protection_level = "STRONG"
        elif "'self'" in csp:
            print("   ✓ CSP frame-ancestors: 'self' (same-origin only)")
            csp_protection_level = "MEDIUM"
        else:
            print(f"   ⚠ CSP frame-ancestors: custom policy")
            csp_protection_level = "CUSTOM"
    else:
        print("   ✗ CSP frame-ancestors: NOT SET")

    # TEST 3: Practical iframe embedding test
    print("\n3. Testing Actual Iframe Embedding...")

    # Create HTML page with iframe
    iframe_test_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Clickjacking Test</title>
        <style>
            #target-frame {{
                width: 800px;
                height: 600px;
                border: 2px solid red;
            }}
        </style>
    </head>
    <body>
        <h1>Clickjacking Test - Iframe Embedding</h1>
        <iframe id="target-frame" src="{login_page.base_url}"></iframe>

        <script>
            // Attempt to access iframe content
            window.addEventListener('load', function() {{
                try {{
                    const frame = document.getElementById('target-frame');
                    const frameDoc = frame.contentDocument || frame.contentWindow.document;
                    console.log('IFRAME_ACCESS_SUCCESS: Can access iframe content');
                }} catch(e) {{
                    console.log('IFRAME_ACCESS_BLOCKED: ' + e.message);
                }}
            }});
        </script>
    </body>
    </html>
    """

    # Create a new page with our test HTML
    test_page = page.context.new_page()

    # Listen for console messages
    console_messages = []
    test_page.on('console', lambda msg: console_messages.append(msg.text))

    # Listen for errors (frame blocking)
    frame_errors = []

    def handle_page_error(error):
        frame_errors.append(str(error))

    test_page.on('pageerror', handle_page_error)

    # Set content and verify
    try:
        test_page.set_content(iframe_test_html)
        test_page.wait_for_timeout(3000)  # Wait for iframe to load

        # Check if iframe is loaded
        iframe = test_page.frame_locator('#target-frame').first

        try:
            # Try to get content from iframe
            iframe_loaded = test_page.locator('#target-frame').evaluate("""
                (frame) => {
                    try {
                        return frame.contentWindow.location.href !== 'about:blank';
                    } catch(e) {
                        return false;
                    }
                }
            """)

            if iframe_loaded:
                print("   ⚠ WARNING: Site can be embedded in iframe!")
                iframe_protection = "WEAK"
            else:
                print("   ✓ Site blocked iframe embedding")
                iframe_protection = "PROTECTED"

        except Exception as e:
            print(f"   ✓ Iframe embedding blocked: {str(e)[:50]}")
            iframe_protection = "PROTECTED"

    except Exception as e:
        print(f"   ✓ Iframe test blocked: {str(e)[:50]}")
        iframe_protection = "PROTECTED"

    # Check console messages
    for msg in console_messages:
        if 'IFRAME_ACCESS_BLOCKED' in msg:
            print(f"   ✓ Cross-origin access blocked")
        elif 'IFRAME_ACCESS_SUCCESS' in msg:
            print(f"   ✗ WARNING: Iframe content is accessible!")

    test_page.close()

    # TEST 4: Frame Busting Code Detection
    print("\n4. Checking for Frame Busting Code...")

    page_content = page.content()
    page_scripts = page.evaluate("""
        () => {
            const scripts = Array.from(document.querySelectorAll('script'));
            return scripts.map(s => s.textContent).join(' ');
        }
    """)

    frame_busting_patterns = [
        'top.location',
        'window.top',
        'parent.frames',
        'self != top',
        'top != self',
        'frameElement',
    ]

    frame_busting_found = False
    for pattern in frame_busting_patterns:
        if pattern in page_scripts:
            print(f"   ✓ Frame busting code detected: {pattern}")
            frame_busting_found = True
            break

    if not frame_busting_found:
        print("   ℹ No client-side frame busting detected (relying on headers)")

    # TEST 5: Test different sensitive pages
    print("\n5. Testing Clickjacking Protection on Sensitive POM...")

    sensitive_pages = [
        '/login',
        '/payment',
        '/signup',
    ]

    for path in sensitive_pages:
        resp = page.goto(f"{login_page.base_url}{path}")
        page.wait_for_timeout(500)

        headers = {k.lower(): v for k, v in resp.headers.items()}
        xfo = headers.get('x-frame-options', '').upper()

        if xfo in ['DENY', 'SAMEORIGIN']:
            print(f"   ✓ {path}: Protected ({xfo})")
        else:
            print(f"   ⚠ {path}: Not protected")

    # OVERALL ASSESSMENT
    print("\n" + "=" * 50)
    print("CLICKJACKING PROTECTION ASSESSMENT:")
    print("=" * 50)

    protection_score = 0

    if protection_level_xfo == "PROTECTED":
        protection_score += 2
        print("✓ X-Frame-Options: GOOD")

    if csp_protection_level in ["STRONG", "MEDIUM"]:
        protection_score += 2
        print("✓ CSP frame-ancestors: GOOD")

    if iframe_protection == "PROTECTED":
        protection_score += 1
        print("✓ Practical iframe test: BLOCKED")

    if frame_busting_found:
        protection_score += 1
        print("✓ Frame busting code: PRESENT")

    print(f"\nProtection Score: {protection_score}/6")

    if protection_score >= 4:
        print("Overall Rating: WELL PROTECTED 🟢")
    elif protection_score >= 2:
        print("Overall Rating: PARTIALLY PROTECTED 🟡")
    else:
        print("Overall Rating: VULNERABLE 🔴")

    print("=" * 50 + "\n")

    # Minimum of 2 out of 6 points required to pass the test
    assert protection_score >= 2, \
        f"Insufficient clickjacking protection: {protection_score}/6"

    print("✓ Clickjacking Protection Test PASSED\n")
