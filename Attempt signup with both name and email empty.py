import pytest
from playwright.sync_api import Page, expect


class TestEmptyFieldsValidation:
    """Test suite for validating empty name and email fields"""

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

    def test_empty_fields_validation(self):
        """
        Test Case: Validate behavior when Name and Email fields are empty - 66

        Steps:
        1. Open Chrome browser
        2. Go to http://automationexercise.com/login
        3. Locate New User Signup! section
        4. Leave Name field empty
        5. Leave Email Address field empty
        6. Click orange Signup button
        7. Observe validation behavior
        """

        print("\n" + "=" * 70)
        print("TEST: Empty Name and Email Fields Validation")
        print("=" * 70)

        # Step 1 & 2: Open Chrome browser and navigate to login page
        print("\n🌐 Step 1-2: Opening browser and navigating to login page...")
        self.page.goto(f"{self.base_url}/login")

        # Wait for page to load
        self.page.wait_for_load_state('networkidle')
        self.handle_cookie_consent()

        # Verify we're on login page
        expect(self.page).to_have_url(f"{self.base_url}/login")
        print("✅ Step 1-2: On http://automationexercise.com/login")

        # Step 3: Locate New User Signup! section
        print("\n📝 Step 3: Locating 'New User Signup!' section...")

        signup_heading = self.page.locator('text=New User Signup!')
        expect(signup_heading).to_be_visible()

        # Scroll to ensure it's visible
        signup_heading.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)

        print("✅ Step 3: 'New User Signup!' section located")

        # Locate the fields
        name_field = self.page.locator('input[data-qa="signup-name"]')
        email_field = self.page.locator('input[data-qa="signup-email"]')
        signup_button = self.page.locator('button[data-qa="signup-button"]')

        # Verify all elements are visible
        expect(name_field).to_be_visible()
        expect(email_field).to_be_visible()
        expect(signup_button).to_be_visible()

        print("   ✓ Name field visible")
        print("   ✓ Email Address field visible")
        print("   ✓ Signup button visible")

        # Step 4: Leave Name field empty
        print("\n📝 Step 4: Ensuring Name field is empty...")

        name_field.clear()
        name_value = name_field.input_value()

        print(f"   Name field value: '{name_value}'")

        if name_value == "":
            print("✅ Step 4: Name field is EMPTY")
        else:
            print(f"⚠️ Name field contains: '{name_value}'")
            name_field.clear()
            print("   Cleared Name field")

        # Step 5: Leave Email Address field empty
        print("\n📝 Step 5: Ensuring Email Address field is empty...")

        email_field.clear()
        email_value = email_field.input_value()

        print(f"   Email Address field value: '{email_value}'")

        if email_value == "":
            print("✅ Step 5: Email Address field is EMPTY")
        else:
            print(f"⚠️ Email field contains: '{email_value}'")
            email_field.clear()
            print("   Cleared Email Address field")

        # Check field attributes
        print("\n🔍 Field Attributes:")

        name_required = name_field.get_attribute('required')
        email_required = email_field.get_attribute('required')
        email_type = email_field.get_attribute('type')

        print(f"   Name field 'required' attribute: {name_required}")
        print(f"   Email field 'required' attribute: {email_required}")
        print(f"   Email field 'type' attribute: {email_type}")

        # Check validation state before clicking
        print("\n🔍 Pre-submission validation state:")

        name_validation_msg = name_field.evaluate("el => el.validationMessage")
        name_valid = name_field.evaluate("el => el.validity.valid")

        email_validation_msg = email_field.evaluate("el => el.validationMessage")
        email_valid = email_field.evaluate("el => el.validity.valid")

        print(f"   Name field valid: {name_valid}")
        if name_validation_msg:
            print(f"   Name validation message: '{name_validation_msg}'")

        print(f"   Email field valid: {email_valid}")
        if email_validation_msg:
            print(f"   Email validation message: '{email_validation_msg}'")

        # Step 6: Click orange Signup button
        print("\n🖱️ Step 6: Clicking orange Signup button...")

        # Check button color/style
        button_bg_color = signup_button.evaluate("el => window.getComputedStyle(el).backgroundColor")
        print(f"   Button background color: {button_bg_color}")

        # Get URL before clicking
        url_before = self.page.url
        print(f"   Current URL: {url_before}")

        print("\n   Clicking Signup button...")
        signup_button.click()

        # Wait for response
        self.page.wait_for_timeout(2000)

        print("✅ Step 6: Signup button clicked")

        # Step 7: Observe validation behavior
        print("\n" + "=" * 70)
        print("STEP 7: OBSERVING VALIDATION BEHAVIOR")
        print("=" * 70)

        # Check URL after clicking
        url_after = self.page.url

        print(f"\n📍 URL Comparison:")
        print(f"   Before: {url_before}")
        print(f"   After:  {url_after}")

        if url_before == url_after:
            print("   ➜ Result: STAYED on login page")
        else:
            print("   ➜ Result: NAVIGATED to different page")

        # Check validation messages after clicking
        print("\n🔍 Post-submission validation state:")

        name_validation_after = name_field.evaluate("el => el.validationMessage")
        name_valid_after = name_field.evaluate("el => el.validity.valid")
        name_validity_state = name_field.evaluate("""
            el => ({
                valueMissing: el.validity.valueMissing,
                valid: el.validity.valid
            })
        """)

        email_validation_after = email_field.evaluate("el => el.validationMessage")
        email_valid_after = email_field.evaluate("el => el.validity.valid")
        email_validity_state = email_field.evaluate("""
            el => ({
                valueMissing: el.validity.valueMissing,
                valid: el.validity.valid
            })
        """)

        print(f"\n   Name Field:")
        print(f"      • Valid: {name_valid_after}")
        print(f"      • Value missing: {name_validity_state['valueMissing']}")

        if name_validation_after:
            print(f"      • ✅ Validation message: '{name_validation_after}'")
        else:
            print(f"      • No validation message")

        print(f"\n   Email Field:")
        print(f"      • Valid: {email_valid_after}")
        print(f"      • Value missing: {email_validity_state['valueMissing']}")

        if email_validation_after:
            print(f"      • ✅ Validation message: '{email_validation_after}'")
        else:
            print(f"      • No validation message")

        # Check which field has focus
        print("\n🔍 Field Focus:")

        name_focused = name_field.evaluate("el => el === document.activeElement")
        email_focused = email_field.evaluate("el => el === document.activeElement")

        print(f"   Name field focused: {name_focused}")
        print(f"   Email field focused: {email_focused}")

        if name_focused:
            print("   ➜ Name field has focus (likely first validation error)")
        elif email_focused:
            print("   ➜ Email field has focus")

        # Check for custom error messages
        print("\n🔍 Custom Error Messages:")

        error_selectors = [
            '.error',
            '.invalid-feedback',
            '.alert-danger',
            '.text-danger',
            'p.error',
            'span.error'
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

        # Check if form is still visible
        print("\n🔍 Form State:")

        name_field_visible = name_field.is_visible()
        email_field_visible = email_field.is_visible()
        signup_button_visible = signup_button.is_visible()

        print(f"   Name field visible: {name_field_visible}")
        print(f"   Email field visible: {email_field_visible}")
        print(f"   Signup button visible: {signup_button_visible}")

        if name_field_visible and email_field_visible:
            print("   ➜ Signup form STILL VISIBLE")

        # Validation Summary
        print("\n" + "=" * 70)
        print("VALIDATION SUMMARY")
        print("=" * 70)

        print(f"\nField States:")
        print(f"   Name field:")
        print(f"      • Value: EMPTY")
        print(f"      • Required: {name_required is not None}")
        print(f"      • Valid: {name_valid_after}")

        print(f"   Email field:")
        print(f"      • Value: EMPTY")
        print(f"      • Required: {email_required is not None}")
        print(f"      • Valid: {email_valid_after}")

        print(f"\nValidation Messages:")

        validation_triggered = False

        if name_validation_after:
            print(f"   ✅ Name field: '{name_validation_after}'")
            validation_triggered = True
        else:
            print(f"   ❌ Name field: No message")

        if email_validation_after:
            print(f"   ✅ Email field: '{email_validation_after}'")
            validation_triggered = True
        else:
            print(f"   ❌ Email field: No message")

        if errors_found:
            print(f"   ✅ Custom errors: {len(errors_found)} found")
            for error in errors_found:
                print(f"      - {error}")
            validation_triggered = True

        print(f"\nForm Behavior:")
        print(f"   • URL changed: {'Yes' if url_before != url_after else 'No'}")
        print(f"   • Form submitted: {'Yes' if url_before != url_after else 'No'}")
        print(f"   • Validation triggered: {'Yes' if validation_triggered else 'No'}")

        # Test Result
        print("\n" + "=" * 70)
        print("TEST RESULT")
        print("=" * 70)

        stayed_on_page = url_before == url_after

        if validation_triggered:
            print("\n✅ VALIDATION IS WORKING!")

            if name_validation_after:
                print(f"   ✓ Name field shows: '{name_validation_after}'")
            if email_validation_after:
                print(f"   ✓ Email field shows: '{email_validation_after}'")
            if stayed_on_page:
                print(f"   ✓ Form submission prevented")
            if name_focused or email_focused:
                print(f"   ✓ Field focused (guiding user to error)")

        elif stayed_on_page:
            print("\n⚠️ FORM NOT SUBMITTED")
            print("   Validation may have occurred without visible messages")

        else:
            print("\n⚠️ UNEXPECTED BEHAVIOR")
            print("   Form submitted despite empty required fields")

        print("\n" + "=" * 70)
        print("Expected: Empty required fields should trigger validation")
        print(
            f"Actual: {'Validation working ✓' if validation_triggered or stayed_on_page else 'Unexpected behavior ⚠️'}")
        print("=" * 70 + "\n")

        # Assertion
        assert validation_triggered or stayed_on_page, \
            "Empty required fields should trigger validation or prevent submission"

        print("✅ Step 7: Validation behavior observed and verified\n")


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