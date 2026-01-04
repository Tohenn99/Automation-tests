"""
Security Test 10: Payment Form Security (PCI DSS Compliance Check)
Тества security на payment формата за спазване на PCI DSS стандарти
"""

import pytest
from playwright.sync_api import Page
import re
from POM import LoginPage, ProductsPage, CartPage, CheckoutPage, PaymentPage, TestDataFactory


@pytest.mark.security
def test_payment_form_security(page: Page):
    """
    Проверява PCI DSS compliance и payment security:
    1. Credit card data не се съхранява в localStorage/cookies
    2. Card number masking
    3. CVV не се изпраща в plain text
    4. HTTPS на payment page
    5. No card data in URL/logs
    6. Client-side validation
    """
    print("\n=== Payment Form Security Test (PCI DSS) ===\n")

    payment_data = TestDataFactory.get_payment_data()

    # Navigate директно към payment page за тестване
    page.goto("https://automationexercise.com/payment")
    page.wait_for_load_state('networkidle')

    # Handle cookie consent if it appears
    try:
        consent_button = page.locator('.fc-button.fc-cta-consent').first
        if consent_button.is_visible(timeout=3000):
            consent_button.click()
            page.wait_for_timeout(1000)
    except:
        pass

    # TEST 1: Payment Page използва HTTPS
    print("1. Checking HTTPS on Payment Page...")

    payment_url = page.url
    assert payment_url.startswith('https://'), \
        f"CRITICAL: Payment page not using HTTPS: {payment_url}"
    print(f"   ✓ Payment page uses HTTPS: {payment_url}")

    # TEST 2: Card Number Field Security
    print("\n2. Checking Credit Card Field Security...")

    payment_page = PaymentPage(page)
    card_field = page.locator(payment_page.CARD_NUMBER)

    # Провери field type
    card_type = card_field.get_attribute('type')
    print(f"   Card field type: {card_type}")

    # Провери autocomplete
    card_autocomplete = card_field.get_attribute('autocomplete')
    if card_autocomplete in ['off', 'cc-number']:
        print(f"   ✓ Autocomplete: {card_autocomplete}")
    else:
        print(f"   ⚠ Autocomplete: {card_autocomplete or 'not set'}")

    # Fill card number
    card_field.fill(payment_data['card_number'])

    # TEST 3: Card Data не се съхранява в browser storage
    print("\n3. Checking Browser Storage for Card Data...")

    page.wait_for_timeout(1000)

    # LocalStorage check
    local_storage = page.evaluate("() => JSON.stringify(localStorage)")
    assert payment_data['card_number'] not in local_storage, \
        "CRITICAL: Card number found in localStorage!"
    print("   ✓ No card data in localStorage")

    # SessionStorage check
    session_storage = page.evaluate("() => JSON.stringify(sessionStorage)")
    assert payment_data['card_number'] not in session_storage, \
        "CRITICAL: Card number found in sessionStorage!"
    print("   ✓ No card data in sessionStorage")

    # Cookies check
    cookies = page.context.cookies()
    for cookie in cookies:
        cookie_value = cookie.get('value', '')
        assert payment_data['card_number'] not in cookie_value, \
            f"CRITICAL: Card number in cookie: {cookie['name']}"
    print("   ✓ No card data in cookies")

    # TEST 4: CVV Field Security
    print("\n4. Checking CVV Field Security...")

    cvv_field = page.locator(payment_page.CVC)

    # CVV field type
    cvv_type = cvv_field.get_attribute('type')
    if cvv_type == 'password':
        print("   ✓ CVV field type: password (masked)")
        cvv_masked = True
    else:
        print(f"   ⚠ CVV field type: {cvv_type} (not masked)")
        cvv_masked = False

    # CVV autocomplete
    cvv_autocomplete = cvv_field.get_attribute('autocomplete')
    if cvv_autocomplete in ['off', 'cc-csc']:
        print(f"   ✓ CVV autocomplete: {cvv_autocomplete}")

    # Fill CVV
    cvv_field.fill(payment_data['cvc'])

    # TEST 5: Sensitive Data Visibility Check
    print("\n5. Checking Sensitive Data Visibility...")

    page.wait_for_timeout(500)

    # Check if card number appears as visible text on page (not in input value)
    visible_text = page.inner_text('body')

    # Card number should not be visible in rendered page text
    card_visible_in_text = payment_data['card_number'] in visible_text
    if card_visible_in_text:
        print("   ⚠ WARNING: Card number visible in page text")
    else:
        print("   ✓ Card number not visible in rendered text")

    # For CVV - it's OK to be in DOM if field is masked
    if cvv_masked:
        print("   ✓ CVV properly masked (type=password)")
        cvv_secure = True
    else:
        # If not masked, check if visible in text
        cvv_visible_in_text = payment_data['cvc'] in visible_text
        if cvv_visible_in_text:
            print("   ⚠ WARNING: CVV visible in page text AND not masked")
            cvv_secure = False
        else:
            print("   ℹ CVV in DOM but not visible (acceptable)")
            cvv_secure = True

    # Critical assertion: Card number must not be visible as plain text
    assert not card_visible_in_text, \
        "CRITICAL: Full card number visible in page text!"

    print("   ℹ Note: Data in DOM input values is normal if properly masked")

    # TEST 6: Network Requests - Card Data Encryption
    print("\n6. Monitoring Network Requests...")

    network_payloads = []

    def capture_request(request):
        if request.method == 'POST':
            try:
                post_data = request.post_data
                if post_data:
                    network_payloads.append({
                        'url': request.url,
                        'data': post_data
                    })
            except:
                pass

    page.on('request', capture_request)

    # Fill remaining payment fields
    page.locator(payment_page.NAME_ON_CARD).fill(payment_data['name'])
    page.locator(payment_page.EXPIRY_MONTH).fill(payment_data['expiry_month'])
    page.locator(payment_page.EXPIRY_YEAR).fill(payment_data['expiry_year'])

    # Submit payment (но не чакаме да завърши)
    page.locator(payment_page.PAY_BUTTON).click()
    page.wait_for_timeout(2000)

    # Анализирай network payloads
    card_in_plaintext = False
    for payload in network_payloads:
        if payment_data['card_number'] in payload['data']:
            print(f"   ⚠ WARNING: Card sent in plaintext to: {payload['url']}")
            card_in_plaintext = True

    if not card_in_plaintext:
        print("   ✓ Card data not sent in plaintext (may be encrypted/tokenized)")

    # TEST 7: Console Logs - No Card Data
    print("\n7. Checking Console Logs...")

    console_messages = []

    def console_handler(msg):
        console_messages.append(msg.text)

    page.on('console', console_handler)

    # Navigate back to payment page (reload may cause redirect)
    page.goto("https://automationexercise.com/payment")
    page.wait_for_load_state('networkidle')

    # Handle consent again
    try:
        consent_button = page.locator('.fc-button.fc-cta-consent').first
        if consent_button.is_visible(timeout=2000):
            consent_button.click()
            page.wait_for_timeout(500)
    except:
        pass

    # Wait for payment form to be ready
    page.wait_for_selector(payment_page.CARD_NUMBER, state='visible', timeout=10000)

    # Fill again за да генерираме logs
    page.locator(payment_page.CARD_NUMBER).fill(payment_data['card_number'])
    page.locator(payment_page.CVC).fill(payment_data['cvc'])

    page.wait_for_timeout(1000)

    card_in_console = False
    for msg in console_messages:
        if payment_data['card_number'] in msg or payment_data['cvc'] in msg:
            card_in_console = True
            print(f"   ✗ CRITICAL: Card data in console: {msg[:50]}")

    if not card_in_console:
        print("   ✓ No card data leaked in console")

    # TEST 8: Client-Side Validation
    print("\n8. Testing Client-Side Validation...")

    invalid_cards = [
        "1234",  # Too short
        "abcd1234abcd1234",  # Letters
        "<script>alert(1)</script>",  # XSS
    ]

    validation_works = False
    for invalid_card in invalid_cards:
        page.locator(payment_page.CARD_NUMBER).fill(invalid_card)
        page.locator(payment_page.PAY_BUTTON).click()
        page.wait_for_timeout(500)

        # Провери за validation message
        validation_msg = page.locator('.error, .alert-danger, [role="alert"]')
        if validation_msg.count() > 0 and validation_msg.first.is_visible():
            validation_works = True
            print(f"   ✓ Validation rejected: {invalid_card[:20]}")
            break

    if not validation_works:
        print("   ℹ Client-side validation may be minimal (relies on server)")

    # TEST 9: Luhn Algorithm Check (Optional)
    print("\n9. Testing Luhn Algorithm Validation...")

    invalid_luhn_card = "4532015112830367"  # Invalid Luhn

    page.locator(payment_page.CARD_NUMBER).fill(invalid_luhn_card)
    page.locator(payment_page.CVC).fill("871")
    page.locator(payment_page.EXPIRY_MONTH).fill("12")
    page.locator(payment_page.EXPIRY_YEAR).fill("2027")
    page.locator(payment_page.NAME_ON_CARD).fill("Test")

    page.locator(payment_page.PAY_BUTTON).click()
    page.wait_for_timeout(1000)

    # Ако има error, validation работи
    error_visible = page.locator('.error, .alert-danger').count() > 0
    if error_visible:
        print("   ✓ Luhn algorithm validation present")
    else:
        print("   ℹ Luhn validation not detected (may be server-side)")

    # TEST 10: URL не съдържа sensitive data
    print("\n10. Checking URL for Sensitive Data...")

    current_url = page.url

    assert payment_data['card_number'] not in current_url, \
        "CRITICAL: Card number in URL!"
    assert payment_data['cvc'] not in current_url, \
        "CRITICAL: CVV in URL!"

    print("   ✓ No sensitive payment data in URL")

    # OVERALL PCI DSS COMPLIANCE SCORE
    print("\n" + "=" * 50)
    print("PCI DSS COMPLIANCE ASSESSMENT:")
    print("=" * 50)

    pci_score = 0
    max_pci_score = 10

    if payment_url.startswith('https://'):
        pci_score += 2
        print("✓ HTTPS on payment page (Critical)")

    if payment_data['card_number'] not in local_storage:
        pci_score += 2
        print("✓ No card data in localStorage (Critical)")

    if payment_data['card_number'] not in session_storage:
        pci_score += 2
        print("✓ No card data in sessionStorage (Critical)")

    if not card_visible_in_text:
        pci_score += 1
        print("✓ Card number not visible in page text")

    if not card_in_console:
        pci_score += 1
        print("✓ No card data in console logs")

    if not card_in_plaintext:
        pci_score += 1
        print("✓ Card data appears encrypted/tokenized")

    if payment_data['card_number'] not in current_url:
        pci_score += 1
        print("✓ No card data in URL")

    print(f"\nPCI Compliance Score: {pci_score}/{max_pci_score}")

    if pci_score >= 8:
        print("Overall Rating: EXCELLENT 🟢")
    elif pci_score >= 6:
        print("Overall Rating: GOOD 🟡")
    elif pci_score >= 4:
        print("Overall Rating: FAIR 🟠")
    else:
        print("Overall Rating: POOR - PCI NON-COMPLIANT 🔴")

    print("=" * 50 + "\n")

    # Критичен assertion - минимум 6/10
    assert pci_score >= 6, \
        f"Payment security insufficient: {pci_score}/{max_pci_score}"

    print("✓ Payment Form Security Test PASSED\n")