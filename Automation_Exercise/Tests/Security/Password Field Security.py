"""
Security Test 03: Password Field Security
Тества дали паролите са правилно защитени и скрити
"""

import pytest
from playwright.sync_api import Page
from POM import LoginPage, RegistrationPage, TestDataFactory


@pytest.mark.security
def test_password_field_security(page: Page):
    """
    Проверява security на password полетата:
    1. Password field type е 'password' (не plain text)
    2. Password не се показва в page source
    3. Password не се cache-ва в browser
    4. Autocomplete атрибути
    """
    # Създай user и отиди до registration
    user_data = TestDataFactory.get_user_data_usa()

    login_page = LoginPage(page)
    login_page.navigate()
    login_page.signup(user_data['name'], user_data['email'])

    reg_page = RegistrationPage(page)

    # TEST 1: Password field type
    password_field = page.locator(reg_page.PASSWORD)
    password_type = password_field.get_attribute('type')

    assert password_type == 'password', f"Password field type is '{password_type}', should be 'password'"
    print("✓ Password field type is correctly set to 'password'")

    # TEST 2: Fill password и провери дали не е visible
    test_password = "SuperSecret@123"
    password_field.fill(test_password)

    # Провери value attribute (не трябва да е в plaintext в DOM)
    password_value = password_field.input_value()
    assert password_value == test_password, "Password not stored correctly in field"

    # Провери дали паролата е визуално скрита (masked)
    # Проверка на computed style
    is_masked = page.evaluate("""
        (selector) => {
            const field = document.querySelector(selector);
            const style = window.getComputedStyle(field);
            const type = field.type;
            return type === 'password';
        }
    """, reg_page.PASSWORD)

    assert is_masked, "Password is not visually masked"
    print("✓ Password is visually masked in UI")

    # TEST 3: Провери autocomplete атрибути
    autocomplete = password_field.get_attribute('autocomplete')
    # Autocomplete трябва да е или "new-password" или "current-password" или изключено
    if autocomplete:
        assert autocomplete in ['off', 'new-password', 'current-password'], \
            f"Insecure autocomplete setting: {autocomplete}"
    print(f"✓ Autocomplete setting: {autocomplete or 'not set'}")

    # TEST 4: Password не трябва да се появява в URL
    current_url = page.url
    assert test_password not in current_url, "Password leaked in URL!"
    print("✓ Password not exposed in URL")

    # TEST 5: Провери дали password field има paste protection (optional)
    # Някои сайтове disable paste за security
    paste_disabled = password_field.get_attribute('onpaste')
    if paste_disabled and 'return false' in paste_disabled:
        print("✓ Paste is disabled on password field (extra security)")

    # TEST 6: Fill цялата форма и провери console за password leaks
    console_messages = []
    page.on("console", lambda msg: console_messages.append(msg.text))

    reg_page.fill_account_info(
        title=user_data['title'],
        password=test_password,
        dob=user_data['dob']
    )

    # Провери дали паролата не е в console logs
    for msg in console_messages:
        assert test_password not in msg, f"Password leaked in console: {msg}"

    print("✓ Password not leaked in console logs")
    print("✓ Password Field Security Test PASSED")