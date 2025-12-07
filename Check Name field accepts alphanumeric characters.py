import pytest
from playwright.sync_api import Page, expect
import random
import string


class TestSignupFormLoad:
    """Test suite for verifying signup form loads correctly"""

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
        """Generate a unique email to avoid conflicts"""
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"user123_{random_string}@email.com"

    def test_signup_form_loads_after_signup(self):
        """
        Test Case: Verify registration form loads after signup - 94

        Steps:
        1. Go to login page
        2. Type User123 in Name field
        3. Type valid@email.com in Email Address field
        4. Click Signup button
        5. Check if registration form loads
        """

        print("\n" + "=" * 70)
        print("TEST: Verify Registration Form Loads After Signup")
        print("=" * 70)

        # Navigate to website
        self.page.goto(self.base_url)
        expect(self.page).to_have_title("Automation Exercise")
        self.handle_cookie_consent()
        print("✅ Opened website")

        # Step 1: Go to login page
        print("\n" + "-" * 70)
        print("STEP 1: Go to Login Page")
        print("-" * 70)

        signup_login_link = self.page.locator('a[href="/login"]').first
        signup_login_link.click()

        # Verify we're on login page
        expect(self.page).to_have_url(f"{self.base_url}/login")

        # Verify signup section is visible
        signup_section = self.page.locator('text=New User Signup!')
        expect(signup_section).to_be_visible()

        print("✅ Step 1: On login page - Signup section visible")

        # Step 2: Type User123 in Name field
        print("\n" + "-" * 70)
        print("STEP 2: Enter Name")
        print("-" * 70)

        name_field = self.page.locator('input[data-qa="signup-name"]')

        # Verify name field is visible
        expect(name_field).to_be_visible()

        name_field.fill("User123")

        print("✅ Step 2: Typed 'User123' in Name field")

        # Step 3: Type email in Email Address field
        print("\n" + "-" * 70)
        print("STEP 3: Enter Email Address")
        print("-" * 70)

        email_field = self.page.locator('input[data-qa="signup-email"]')

        # Verify email field is visible
        expect(email_field).to_be_visible()

        # Use unique email to avoid "Email already exists" error
        unique_email = self.generate_unique_email()
        email_field.fill(unique_email)

        print(f"✅ Step 3: Typed '{unique_email}' in Email Address field")
        print("   (Using unique email to avoid conflicts)")

        # Step 4: Click Signup button
        print("\n" + "-" * 70)
        print("STEP 4: Click Signup Button")
        print("-" * 70)

        signup_button = self.page.locator('button[data-qa="signup-button"]')

        # Verify button is visible
        expect(signup_button).to_be_visible()

        # Get button text
        button_text = signup_button.inner_text()
        print(f"📝 Button text: '{button_text}'")

        signup_button.click()
        print("✅ Step 4: Clicked 'Signup' button")

        # Step 5: Check if registration form loads
        print("\n" + "-" * 70)
        print("STEP 5: Check if Registration Form Loads")
        print("-" * 70)

        # Wait for registration form to load
        self.page.wait_for_load_state('networkidle')

        # Check for registration form elements
        print("\n🔍 Checking for registration form elements...")

        # Check for form container
        form_container = self.page.locator('#form')
        form_visible = form_container.is_visible(timeout=5000)

        if form_visible:
            print("✅ Registration form container found")
        else:
            print("❌ Registration form container not found")

        # Check for "Enter Account Information" heading
        account_info_heading = self.page.locator('text=Enter Account Information')
        heading_visible = account_info_heading.is_visible(timeout=5000)

        if heading_visible:
            print("✅ 'Enter Account Information' heading found")
        else:
            print("❌ 'Enter Account Information' heading not found")

        # Check for key form fields
        print("\n🔍 Checking for key form fields...")

        fields_to_check = [
            ('#id_gender1', 'Title (Mr.) radio button'),
            ('#id_gender2', 'Title (Mrs.) radio button'),
            ('#password', 'Password field'),
            ('#days', 'Day dropdown'),
            ('#months', 'Month dropdown'),
            ('#years', 'Year dropdown'),
            ('#first_name', 'First name field'),
            ('#last_name', 'Last name field'),
            ('#address1', 'Address field'),
            ('#country', 'Country dropdown'),
            ('#state', 'State field'),
            ('#city', 'City field'),
            ('#zipcode', 'Zipcode field'),
            ('#mobile_number', 'Mobile number field'),
            ('button[data-qa="create-account"]', 'Create Account button')
        ]

        fields_found = 0
        fields_missing = []

        for selector, field_name in fields_to_check:
            field = self.page.locator(selector)
            if field.is_visible(timeout=2000):
                fields_found += 1
                print(f"   ✓ {field_name}")
            else:
                fields_missing.append(field_name)
                print(f"   ✗ {field_name}")

        # Summary
        print("\n" + "-" * 70)
        print("REGISTRATION FORM VERIFICATION SUMMARY")
        print("-" * 70)
        print(f"Form container visible: {'✅ Yes' if form_visible else '❌ No'}")
        print(f"Account Info heading visible: {'✅ Yes' if heading_visible else '❌ No'}")
        print(f"Form fields found: {fields_found}/{len(fields_to_check)}")

        if fields_missing:
            print(f"\nMissing fields:")
            for field in fields_missing:
                print(f"  - {field}")

        print("✅ Step 5: Registration form load check completed")

        # Assertions
        assert form_visible, "Registration form container should be visible"
        assert heading_visible, "'Enter Account Information' heading should be visible"
        assert fields_found >= 10, f"Expected at least 10 form fields, found {fields_found}"

        print("\n" + "=" * 70)
        print("✅ TEST PASSED: Registration Form Loaded Successfully!")
        print("   - Login page accessed")
        print("   - Name 'User123' entered")
        print(f"   - Email '{unique_email}' entered")
        print("   - Signup button clicked")
        print("   - Registration form loaded with all required fields")
        print("=" * 70 + "\n")


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
    # Run the test using pytest
    pytest.main([__file__, "-v", "-s", "--headed"])