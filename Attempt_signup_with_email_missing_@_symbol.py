import pytest
from playwright.sync_api import Page, expect


class TestMissingAtSymbolValidation:
    """Test suite for validating email without @ symbol"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup method to navigate to the website before each test"""
        self.page = page
        self.base_url = "https://automationexercise.com"

    def handle_cookie_consent(self):
        """Handle cookie consent popup if it appears"""
        try:
            consent_button = self.page.locator('.fc-button.fc-cta-consent').first
            if consent_button.is_visible(timeout=5000):
                consent_button.click()
                self.page.wait_for_timeout(1000)
        except:
            pass

    def test_missing_at_symbol_validation(self):
        """
        Test Case: Check validation for email missing @ symbol - 95

        Steps:
        1. Navigate to login page
        2. Type Test User in Name field
        3. Type testexample.com in Email Address field
        4. Click Signup button
        5. Observe validation
        """

        print("\n" + "=" * 70)
        print("TEST: Email Without @ Symbol Validation")
        print("=" * 70)

        # Step 1: Navigate to login page
        print("\n🌐 Step 1: Navigating to login page...")
        self.page.goto(self.base_url)
        expect(self.page).to_have_title("Automation Exercise")
        self.handle_cookie_consent()

        signup_link = self.page.locator('a[href="/login"]').first
        signup_link.click()

        expect(self.page).to_have_url(f"{self.base_url}/login")
        print("✅ Step 1: On login page")

        # Verify signup section is visible
        signup_heading = self.page.locator('text=New User Signup!')
        expect(signup_heading).to_be_visible()
        print("   ✓ 'New User Signup!' section visible")

        # Step 2: Type Test User in Name field
        print("\n📝 Step 2: Typing name in Name field...")

        name_field = self.page.locator('input[data-qa="signup-name"]')
        expect(name_field).to_be_visible()

        name_field.fill("Test User")

        name_value = name_field.input_value()
        print(f"   Name entered: '{name_value}'")

        assert name_value == "Test User", f"Expected 'Test User', got '{name_value}'"
        print("✅ Step 2: 'Test User' entered in Name field")

        # Step 3: Type testexample.com in Email Address field
        print("\n📝 Step 3: Typing email WITHOUT @ symbol...")

        email_field = self.page.locator('input[data-qa="signup-email"]')
        expect(email_field).to_be_visible()

        invalid_email = "testexample.com"
        email_field.fill(invalid_email)

        email_value = email_field.input_value()
        print(f"   Email entered: '{email_value}'")

        assert email_value == invalid_email, f"Expected '{invalid_email}', got '{email_value}'"
        print(f"✅ Step 3: '{invalid_email}' entered in Email field")
        print("   ⚠️ INVALID: Missing @ symbol")

        # Check validation state before submission
        print("\n🔍 Pre-submission validation check...")

        email_type = email_field.get_attribute('type')
        print(f"   Email field type: '{email_type}'")

        validation_message_before = email_field.evaluate("el => el.validationMessage")
        is_valid_before = email_field.evaluate("el => el.validity.valid")

        print(f"   Email field valid (before): {is_valid_before}")
        if validation_message_before:
            print(f"   Validation message (before): '{validation_message_before}'")
        else:
            print("   No validation message yet")

        # Step 4: Click Signup button
        print("\n🖱️ Step 4: Clicking Signup button...")

        signup_button = self.page.locator('button[data-qa="signup-button"]')
        expect(signup_button).to_be_visible()

        url_before = self.page.url
        print(f"   Current URL: {url_before}")

        print("   Clicking Signup button...")
        signup_button.click()

        # Wait for response
        self.page.wait_for_timeout(2000)

        print("✅ Step 4: Signup button clicked")

        # Step 5: Observe validation
        print("\n" + "=" * 70)
        print("STEP 5: OBSERVING VALIDATION")
        print("=" * 70)

        url_after = self.page.url
        print(f"\n📍 URL Check:")
        print(f"   Before: {url_before}")
        print(f"   After:  {url_after}")

        if url_before == url_after:
            print("   ➜ Status: STAYED on signup page")
        else:
            print("   ➜ Status: NAVIGATED to different page")

        # Check HTML5 browser validation
        print("\n🔍 HTML5 Browser Validation:")

        validation_message = email_field.evaluate("el => el.validationMessage")
        is_valid = email_field.evaluate("el => el.validity.valid")
        validity_state = email_field.evaluate("""
            el => ({
                valueMissing: el.validity.valueMissing,
                typeMismatch: el.validity.typeMismatch,
                patternMismatch: el.validity.patternMismatch,
                valid: el.validity.valid
            })
        """)

        print(f"   Email field valid: {is_valid}")
        print(f"   Validity state:")
        for key, value in validity_state.items():
            print(f"      • {key}: {value}")

        if validation_message:
            print(f"\n   ✅ VALIDATION MESSAGE FOUND:")
            print(f"      '{validation_message}'")
        else:
            print(f"\n   ℹ️ No browser validation message")

        # Check if field is focused
        is_focused = email_field.evaluate("el => el === document.activeElement")
        print(f"\n   Email field focused: {is_focused}")
        if is_focused:
            print("      (Field focus often indicates validation error)")

        # Check for custom error messages
        print("\n🔍 Custom Error Messages:")

        error_selectors = [
            '.error',
            '.invalid-feedback',
            '.alert-danger',
            '.text-danger',
            '.help-block',
            'p:has-text("error")',
            'p:has-text("invalid")',
            'span.error',
            'div.error'
        ]

        errors_found = []
        for selector in error_selectors:
            try:
                error_elements = self.page.locator(selector).all()
                for error in error_elements:
                    if error.is_visible():
                        error_text = error.inner_text().strip()
                        if error_text and len(error_text) < 200:
                            errors_found.append(error_text)
                            print(f"   ⚠️ '{error_text}'")
            except:
                pass

        if not errors_found:
            print("   ℹ️ No custom error messages found")

        # Check if signup form is still visible
        print("\n🔍 Form State:")

        name_field_visible = name_field.is_visible()
        email_field_visible = email_field.is_visible()

        print(f"   Name field visible: {name_field_visible}")
        print(f"   Email field visible: {email_field_visible}")

        if name_field_visible and email_field_visible:
            print("   ➜ Signup form STILL VISIBLE (likely validation error)")
        else:
            print("   ➜ Signup form NOT VISIBLE (may have proceeded)")

        # Check if registration form appeared (signup succeeded)
        print("\n🔍 Registration Form Check:")

        try:
            registration_form = self.page.locator('#form')
            registration_form_visible = registration_form.is_visible(timeout=2000)

            if registration_form_visible:
                print("   ⚠️ Registration form IS VISIBLE")
                print("      (Signup may have succeeded despite invalid email)")
            else:
                print("   ✓ Registration form NOT VISIBLE")
        except:
            print("   ✓ Registration form NOT VISIBLE")

        # Validation summary
        print("\n" + "=" * 70)
        print("VALIDATION SUMMARY")
        print("=" * 70)

        print(f"\nInput:")
        print(f"   Name: Test User")
        print(f"   Email: {invalid_email}")
        print(f"   Issue: Missing @ symbol")

        print(f"\nValidation Results:")
        print(f"   • Email field valid: {is_valid}")
        print(f"   • Type mismatch: {validity_state.get('typeMismatch', 'unknown')}")

        if validation_message:
            print(f"   • Browser validation: ✅ TRIGGERED")
            print(f"     Message: '{validation_message}'")
        else:
            print(f"   • Browser validation: ❌ NOT TRIGGERED")

        if errors_found:
            print(f"   • Custom errors: ✅ FOUND ({len(errors_found)})")
            for error in errors_found:
                print(f"     - {error}")
        else:
            print(f"   • Custom errors: ❌ NONE")

        print(f"\nBehavior:")
        print(f"   • URL changed: {'Yes' if url_before != url_after else 'No'}")
        print(f"   • Form submitted: {'Yes' if url_before != url_after else 'No'}")
        print(f"   • Stayed on page: {'Yes' if url_before == url_after else 'No'}")

        # Determine validation status
        validation_occurred = (
                validation_message is not None and validation_message != "" or
                len(errors_found) > 0 or
                (url_before == url_after and is_focused) or
                not is_valid
        )

        print("\n" + "=" * 70)
        print("TEST RESULT")
        print("=" * 70)

        if validation_occurred:
            print("\n✅ VALIDATION DETECTED!")

            if validation_message:
                print(f"   ✓ Browser shows: '{validation_message}'")
            if errors_found:
                print(f"   ✓ Custom error(s) displayed")
            if not is_valid:
                print(f"   ✓ Field marked as invalid")
            if url_before == url_after:
                print(f"   ✓ Form submission prevented")

        else:
            print("\n⚠️ NO CLEAR VALIDATION DETECTED")
            print("   Email without @ may have been accepted")

        print("\n" + "=" * 70)
        print("Expected: Email field should require @ symbol")
        print(f"Actual: {'Validation working ✓' if validation_occurred else 'Validation unclear ⚠️'}")
        print("=" * 70 + "\n")

        # Assertion
        assert validation_occurred or url_before == url_after, \
            "Email without @ symbol should trigger validation or prevent submission"

        print("✅ Step 5: Validation observed and verified\n")


# Configuration for pytest
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context - full HD size"""
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080
        },
        "no_viewport": False
    }


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--headed"])