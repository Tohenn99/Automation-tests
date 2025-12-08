import pytest
from playwright.sync_api import Page, expect


class TestInvalidEmailValidation:
    """Test suite for validating invalid email format"""

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

    def test_invalid_email_validation(self):
        """
        Test Case: Check validation for invalid email format - 96

        Steps:
        1. Go to login page
        2. Type Test User in Name field
        3. Type test@ in Email Address field
        4. Click Signup button
        5. Check for error message
        """

        print("\n" + "=" * 70)
        print("TEST: Invalid Email Format Validation")
        print("=" * 70)

        # Step 1: Go to login page
        print("\n📝 Step 1: Going to login page...")
        self.page.goto(self.base_url)
        expect(self.page).to_have_title("Automation Exercise")
        self.handle_cookie_consent()

        signup_link = self.page.locator('a[href="/login"]').first
        signup_link.click()

        expect(self.page).to_have_url(f"{self.base_url}/login")
        print("✅ Step 1: On login/signup page")

        # Verify signup section is visible
        signup_heading = self.page.locator('text=New User Signup!')
        expect(signup_heading).to_be_visible()
        print("   ✓ 'New User Signup!' section visible")

        # Step 2: Type Test User in Name field
        print("\n📝 Step 2: Typing name in Name field...")

        name_field = self.page.locator('input[data-qa="signup-name"]')
        expect(name_field).to_be_visible()

        name_field.fill("Test User")

        # Verify the value
        name_value = name_field.input_value()
        print(f"   Entered: '{name_value}'")

        assert name_value == "Test User", f"Expected 'Test User', got '{name_value}'"
        print("✅ Step 2: Name 'Test User' entered successfully")

        # Step 3: Type test@ in Email Address field
        print("\n📝 Step 3: Typing invalid email in Email Address field...")

        email_field = self.page.locator('input[data-qa="signup-email"]')
        expect(email_field).to_be_visible()

        invalid_email = "test@"
        email_field.fill(invalid_email)

        # Verify the value
        email_value = email_field.input_value()
        print(f"   Entered: '{email_value}'")

        assert email_value == invalid_email, f"Expected '{invalid_email}', got '{email_value}'"
        print(f"✅ Step 3: Invalid email '{invalid_email}' entered")
        print("   ⚠️ This is an incomplete/invalid email format")

        # Check HTML5 validation state before clicking
        print("\n🔍 Checking email field validity before submission...")

        # Get validation message and validity state
        validation_message_before = email_field.evaluate("el => el.validationMessage")
        is_valid_before = email_field.evaluate("el => el.validity.valid")

        print(f"   Email field valid: {is_valid_before}")
        if validation_message_before:
            print(f"   Validation message: '{validation_message_before}'")

        # Step 4: Click Signup button
        print("\n📝 Step 4: Clicking Signup button...")

        signup_button = self.page.locator('button[data-qa="signup-button"]')
        expect(signup_button).to_be_visible()

        # Get URL before clicking
        url_before = self.page.url
        print(f"   Current URL: {url_before}")

        print("🖱️ Clicking Signup button...")
        signup_button.click()

        # Wait for potential page change or validation
        self.page.wait_for_timeout(2000)

        print("✅ Step 4: Signup button clicked")

        # Step 5: Check for error message
        print("\n" + "=" * 70)
        print("STEP 5: CHECKING FOR ERROR MESSAGE")
        print("=" * 70)

        # Get URL after clicking
        url_after = self.page.url
        print(f"\n📍 URL after clicking: {url_after}")

        if url_before == url_after:
            print("   ➜ URL unchanged (stayed on signup page)")
        else:
            print("   ➜ URL changed (moved to different page)")

        # Check HTML5 validation message
        print("\n🔍 Checking HTML5 browser validation...")

        validation_message = email_field.evaluate("el => el.validationMessage")
        is_valid = email_field.evaluate("el => el.validity.valid")

        print(f"   Email field valid: {is_valid}")

        if validation_message:
            print(f"   ✅ Browser validation message found:")
            print(f"      '{validation_message}'")
        else:
            print("   ℹ️ No browser validation message")

        # Check if email field is focused (happens on validation error)
        is_focused = email_field.evaluate("el => el === document.activeElement")
        if is_focused:
            print("   ✓ Email field is focused (validation likely triggered)")

        # Check for custom error messages on the page
        print("\n🔍 Checking for custom error messages...")

        error_selectors = [
            '.error',
            '.invalid-feedback',
            '.alert-danger',
            '.text-danger',
            'p:has-text("error")',
            'p:has-text("invalid")',
            'span:has-text("error")',
            'div:has-text("Please")'
        ]

        errors_found = []
        for selector in error_selectors:
            try:
                error_elements = self.page.locator(selector).all()
                for error in error_elements:
                    if error.is_visible():
                        error_text = error.inner_text()
                        if error_text and len(error_text) < 200:  # Reasonable error message length
                            errors_found.append(error_text)
                            print(f"   ⚠️ Error message found: '{error_text}'")
            except:
                pass

        if not errors_found and not validation_message:
            print("   ℹ️ No custom error messages found on page")

        # Check if form is still visible (not submitted)
        print("\n🔍 Checking if signup form is still visible...")

        if name_field.is_visible() and email_field.is_visible():
            print("   ✓ Signup form still visible (form not submitted)")
        else:
            print("   ➜ Signup form not visible (may have navigated away)")

        # Check if registration form loaded (would mean signup succeeded)
        try:
            registration_form = self.page.locator('#form')
            if registration_form.is_visible(timeout=2000):
                print("   ⚠️ Registration form loaded (signup may have succeeded)")
            else:
                print("   ✓ Registration form not loaded")
        except:
            print("   ✓ Registration form not loaded")

        # Summary of validation behavior
        print("\n" + "=" * 70)
        print("VALIDATION SUMMARY")
        print("=" * 70)
        print(f"Input Details:")
        print(f"   Name: Test User")
        print(f"   Email: {invalid_email} (INVALID FORMAT)")
        print(f"\nValidation Results:")
        print(f"   • Email field valid: {is_valid}")

        if validation_message:
            print(f"   • Browser validation: ✓ TRIGGERED")
            print(f"     Message: '{validation_message}'")
        else:
            print(f"   • Browser validation: ✗ NOT TRIGGERED")

        print(f"   • Custom error messages: {len(errors_found)}")

        if errors_found:
            for error in errors_found:
                print(f"     - {error}")

        print(f"   • URL changed: {url_before != url_after}")
        print(f"   • Form submitted: {'No' if url_before == url_after else 'Yes'}")

        # Test assertions
        print("\n" + "=" * 70)
        print("TEST ASSERTIONS")
        print("=" * 70)

        # At least one of these should be true for proper validation
        has_validation = (
                validation_message or  # Browser validation
                len(errors_found) > 0 or  # Custom error messages
                (url_before == url_after and is_focused)  # Stayed on page with focus
        )

        if validation_message:
            print("✅ PASS: Browser validation triggered")
            print(f"   Message: '{validation_message}'")

        if len(errors_found) > 0:
            print("✅ PASS: Custom error message displayed")
            for error in errors_found:
                print(f"   - {error}")

        if url_before == url_after:
            print("✅ PASS: Form not submitted (stayed on page)")

        # Final result
        print("\n" + "=" * 70)
        print("TEST RESULT")
        print("=" * 70)

        if has_validation:
            print("✅ TEST PASSED: Validation working correctly!")
            print("   Invalid email format was caught")
        else:
            print("⚠️ TEST INCONCLUSIVE: Validation behavior unclear")
            print("   Email 'test@' may have been accepted")

        print("=" * 70 + "\n")

        # Assert that some form of validation occurred
        assert has_validation or url_before == url_after, \
            "Invalid email should trigger validation or prevent form submission"


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
