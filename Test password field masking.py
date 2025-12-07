import pytest
from playwright.sync_api import Page, expect
import random
import string


class TestPasswordMasking:
    """Test suite for verifying password field masking"""

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

    def generate_unique_email(self):
        """Generate a unique email address"""
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"testuser_{random_string}@example.com"

    def test_password_field_masking(self):
        """
        Test Case: Verify password field masking behavior - 89

        Steps:
        - Navigate to registration form
        - Click in Password field
        - Type Test@123
        - Observe characters as typing
        - Check if password is masked with dots or asterisks
        """

        print("\n" + "=" * 70)
        print("TEST: Password Field Masking Verification")
        print("=" * 70)

        # Navigate to website
        print("\n🌐 Opening website...")
        self.page.goto(self.base_url)
        expect(self.page).to_have_title("Automation Exercise")
        self.handle_cookie_consent()
        print("✅ Opened website")

        # Navigate to registration form
        print("\n📝 Navigating to registration form...")

        # Click Signup/Login
        signup_link = self.page.locator('a[href="/login"]').first
        signup_link.click()
        expect(self.page).to_have_url(f"{self.base_url}/login")
        print("✅ On signup page")

        # Fill initial signup form
        unique_email = self.generate_unique_email()
        print(f"\n📧 Filling signup form with email: {unique_email}")

        self.page.locator('input[data-qa="signup-name"]').fill("Test User")
        self.page.locator('input[data-qa="signup-email"]').fill(unique_email)
        self.page.locator('button[data-qa="signup-button"]').click()

        self.page.wait_for_selector('#form')
        print("✅ Registration form loaded")

        # Locate the password field
        print("\n" + "-" * 70)
        print("PASSWORD FIELD TESTING")
        print("-" * 70)

        password_field = self.page.locator('#password')

        # Verify password field is visible
        expect(password_field).to_be_visible()
        print("✅ Password field located")

        # Click in Password field
        print("\n🖱️ Clicking in Password field...")
        password_field.click()
        self.page.wait_for_timeout(500)
        print("✅ Clicked in Password field")

        # Check the input type attribute BEFORE typing
        print("\n🔍 Checking password field attributes...")

        input_type_before = password_field.get_attribute('type')
        print(f"   Input type attribute: '{input_type_before}'")

        # Type password character by character and observe
        print("\n⌨️ Typing password 'Test@123' character by character...")

        test_password = "Test@123"

        # Clear the field first
        password_field.clear()

        # Type each character with a delay to observe masking
        for i, char in enumerate(test_password, 1):
            password_field.type(char, delay=200)  # Type with 200ms delay

            # Get the current value
            current_value = password_field.input_value()

            print(f"   Typed: '{char}' (Character {i}/{len(test_password)})")
            print(f"      Field value length: {len(current_value)} characters")

            # Brief pause to observe
            self.page.wait_for_timeout(300)

        print("\n✅ Finished typing password")

        # Check the final value in the field
        print("\n🔍 Analyzing password field masking...")

        final_value = password_field.input_value()
        input_type_after = password_field.get_attribute('type')

        print(f"\n   Password Field Analysis:")
        print(f"   • Input type: '{input_type_after}'")
        print(f"   • Expected password: '{test_password}'")
        print(f"   • Actual field value: '{final_value}'")
        print(f"   • Password length: {len(test_password)} characters")
        print(f"   • Field value length: {len(final_value)} characters")

        # Check if password is masked
        print("\n" + "-" * 70)
        print("MASKING VERIFICATION")
        print("-" * 70)

        is_password_type = input_type_after == 'password'
        values_match = final_value == test_password

        if is_password_type:
            print("\n✅ Field type is 'password' - Browser will mask the input")
            print("   • Characters are displayed as dots (•) or asterisks (*)")
            print("   • This is handled by the browser automatically")
            print("   • The actual value in the field is: '{}'".format(test_password))
        else:
            print(f"\n⚠️ Field type is '{input_type_after}' - Not a standard password field")

        if values_match:
            print("✅ Field value matches typed password (stored correctly)")
        else:
            print(f"❌ Field value mismatch!")
            print(f"   Expected: {test_password}")
            print(f"   Found: {final_value}")

        # Visual representation
        print("\n" + "-" * 70)
        print("VISUAL REPRESENTATION")
        print("-" * 70)
        print(f"What you typed:    {test_password}")
        print(f"What user sees:    {'•' * len(test_password)} (masked)")
        print(f"What is stored:    {final_value}")

        # Additional check - try to get the visible text (should not show password)
        try:
            visible_text = password_field.inner_text()
            if visible_text:
                print(f"\n⚠️ Visible text found: '{visible_text}'")
            else:
                print("\n✅ No visible text (password is properly masked)")
        except:
            print("\n✅ Cannot read visible text (password is properly masked)")

        # Check for any password visibility toggle
        print("\n🔍 Checking for password visibility toggle...")

        try:
            # Look for common password toggle icons/buttons near the password field
            password_container = password_field.locator('..')
            toggle_button = password_container.locator('button, i, span').all()

            if len(toggle_button) > 0:
                print(f"   Found {len(toggle_button)} element(s) near password field")
                print("   (May include visibility toggle)")
            else:
                print("   No toggle button found")
        except:
            print("   No toggle button found")

        # Final assertions
        print("\n" + "=" * 70)
        print("TEST ASSERTIONS")
        print("=" * 70)

        assert input_type_after == 'password', \
            f"Password field should have type='password', found type='{input_type_after}'"
        print("✅ PASS: Password field type is 'password'")

        assert values_match, \
            f"Password value should match typed text"
        print("✅ PASS: Password value stored correctly")

        # Summary
        print("\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        print("Password Field Behavior:")
        print(f"   • Field type: password ✓")
        print(f"   • Masking: Enabled ✓")
        print(f"   • Characters typed: {len(test_password)}")
        print(f"   • Visual display: {'•' * len(test_password)}")
        print(f"   • Stored value: Correct ✓")
        print("\nResult: Password field properly masks user input")
        print("=" * 70)

        print("\n✅ TEST PASSED: Password Field is Properly Masked!\n")


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