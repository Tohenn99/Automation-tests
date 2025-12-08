import pytest
from playwright.sync_api import Page, expect
import random
import string


class TestEmptyLastNameValidation:
    """Test suite for validating empty last name field"""

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

    def test_empty_lastname_validation(self):
        """
        Test Case: Test validation when Last name field is empty - 76

        Steps:
        1. Navigate to registration form
        2. Fill Title, Password, Date of Birth
        3. Fill First name in ADDRESS INFORMATION
        4. Leave Last name field empty
        5. Fill other address fields
        6. Click Create Account button
        7. Observe validation
        """

        print("\n" + "=" * 70)
        print("TEST: Empty Last Name Field Validation")
        print("=" * 70)

        # Navigate to website
        print("\n🌐 Opening website...")
        self.page.goto(self.base_url)
        expect(self.page).to_have_title("Automation Exercise")
        self.handle_cookie_consent()
        print("✅ Opened website")

        # Step 1: Navigate to registration form
        print("\n📝 Step 1: Navigating to registration form...")

        signup_link = self.page.locator('a[href="/login"]').first
        signup_link.click()
        expect(self.page).to_have_url(f"{self.base_url}/login")
        print("✅ On signup page")

        # Fill initial signup
        unique_email = self.generate_unique_email()
        print(f"\n📧 Filling signup form with email: {unique_email}")

        self.page.locator('input[data-qa="signup-name"]').fill("Test User")
        self.page.locator('input[data-qa="signup-email"]').fill(unique_email)
        self.page.locator('button[data-qa="signup-button"]').click()

        self.page.wait_for_selector('#form')
        print("✅ Step 1: Registration form loaded")

        # Step 2: Fill Title, Password, Date of Birth
        print("\n" + "-" * 70)
        print("STEP 2: Filling Account Information")
        print("-" * 70)

        # Select Mr. title
        self.page.locator('#id_gender1').check()
        print("✓ Selected Title: Mr.")

        # Fill Password
        self.page.locator('#password').fill('Test@123')
        print("✓ Filled Password: Test@123")

        # Fill Date of Birth
        self.page.locator('#days').select_option('15')
        self.page.locator('#months').select_option('6')
        self.page.locator('#years').select_option('1990')
        print("✓ Selected Date of Birth: 15-June-1990")

        # Newsletter and offers (optional)
        self.page.locator('#newsletter').check()
        self.page.locator('#optin').check()
        print("✓ Checked newsletter and offers")

        print("\n✅ Step 2: Account Information filled")

        # Step 3: Fill First name in ADDRESS INFORMATION
        print("\n" + "-" * 70)
        print("STEP 3: Filling First Name in Address Information")
        print("-" * 70)

        # Scroll to address section
        address_heading = self.page.locator('text=Address Information')
        address_heading.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)

        self.page.locator('#first_name').fill('John')
        print("✓ Filled First name: John")

        print("\n✅ Step 3: First name filled")

        # Step 4: Leave Last name field empty
        print("\n" + "-" * 70)
        print("STEP 4: Leaving Last Name Field EMPTY")
        print("-" * 70)

        last_name_field = self.page.locator('#last_name')

        # Ensure it's empty
        last_name_field.clear()

        # Check if it's empty
        last_name_value = last_name_field.input_value()
        print(f"✓ Last name field value: '{last_name_value}'")

        if last_name_value == "":
            print("✅ Step 4: Last name field is EMPTY (as intended)")
        else:
            print(f"⚠️ Last name field contains: '{last_name_value}'")

        # Step 5: Fill other address fields
        print("\n" + "-" * 70)
        print("STEP 5: Filling Other Address Fields")
        print("-" * 70)

        # Company
        self.page.locator('#company').fill('Test Company')
        print("✓ Filled Company: Test Company")

        # Address 1
        self.page.locator('#address1').fill('123 Main Street')
        print("✓ Filled Address 1: 123 Main Street")

        # Address 2
        self.page.locator('#address2').fill('Apt 4B')
        print("✓ Filled Address 2: Apt 4B")

        # Country
        self.page.locator('#country').select_option('United States')
        print("✓ Selected Country: United States")

        # State
        self.page.locator('#state').fill('California')
        print("✓ Filled State: California")

        # City
        self.page.locator('#city').fill('Los Angeles')
        print("✓ Filled City: Los Angeles")

        # Zipcode
        self.page.locator('#zipcode').fill('90001')
        print("✓ Filled Zipcode: 90001")

        # Mobile Number
        self.page.locator('#mobile_number').fill('5551234567')
        print("✓ Filled Mobile Number: 5551234567")

        print("\n✅ Step 5: Other address fields filled")

        # Summary before submission
        print("\n" + "=" * 70)
        print("FORM SUMMARY BEFORE SUBMISSION")
        print("=" * 70)
        print("Account Information:")
        print("  ✓ Title: Mr.")
        print("  ✓ Password: Test@123")
        print("  ✓ Date of Birth: 15-June-1990")
        print("\nAddress Information:")
        print("  ✓ First name: John")
        print("  ❌ Last name: EMPTY (intentionally left blank)")
        print("  ✓ Company: Test Company")
        print("  ✓ Address 1: 123 Main Street")
        print("  ✓ Address 2: Apt 4B")
        print("  ✓ Country: United States")
        print("  ✓ State: California")
        print("  ✓ City: Los Angeles")
        print("  ✓ Zipcode: 90001")
        print("  ✓ Mobile Number: 5551234567")
        print("=" * 70)

        # Step 6: Click Create Account button
        print("\n" + "-" * 70)
        print("STEP 6: Clicking Create Account Button")
        print("-" * 70)

        create_account_button = self.page.locator('button[data-qa="create-account"]')

        # Check if button is visible
        expect(create_account_button).to_be_visible()
        print("✓ Create Account button is visible")

        # Get current URL before clicking
        url_before = self.page.url
        print(f"✓ Current URL: {url_before}")

        # Click the button
        print("\n🖱️ Clicking Create Account button...")
        create_account_button.click()

        print("✅ Step 6: Create Account button clicked")

        # Step 7: Observe validation
        print("\n" + "=" * 70)
        print("STEP 7: OBSERVING VALIDATION")
        print("=" * 70)

        # Wait for page to respond
        self.page.wait_for_load_state('networkidle')
        self.page.wait_for_timeout(2000)

        # Get current URL after clicking
        url_after = self.page.url
        print(f"\n📍 URL after submission: {url_after}")

        # Check if we're still on the same page or moved
        if url_before == url_after:
            print("   ➜ URL unchanged (stayed on registration form)")
        else:
            print("   ➜ URL changed (moved to different page)")

        # Check for browser validation message
        print("\n🔍 Checking for validation messages...")

        # Check for HTML5 validation on last name field
        last_name_validation = last_name_field.evaluate(
            "el => el.validationMessage"
        )

        if last_name_validation:
            print(f"   ✓ Browser validation message: '{last_name_validation}'")
        else:
            print("   ℹ️ No browser validation message")

        # Check if last name field is marked as invalid
        last_name_validity = last_name_field.evaluate(
            "el => el.validity.valid"
        )

        print(f"   Field validity: {last_name_validity}")

        # Check for success message
        try:
            success_message = self.page.locator('h2[data-qa="account-created"]')
            if success_message.is_visible(timeout=3000):
                success_text = success_message.inner_text()
                print(f"\n✅ Account Created! Message: '{success_text}'")
                print("   ➜ Validation: Last name field is NOT required")
            else:
                print("\n   ℹ️ No success message found")
        except:
            print("\n   ℹ️ No success message visible")

        # Check if we're still on form (validation failed)
        try:
            form_still_visible = self.page.locator('#form').is_visible(timeout=2000)
            if form_still_visible and url_before == url_after:
                print("\n⚠️ Still on registration form")
                print("   ➜ Possible validation error (form not submitted)")
            else:
                print("\n✓ Form submitted successfully")
        except:
            pass

        # Check for any error messages on page
        print("\n🔍 Checking for error messages...")

        error_selectors = [
            '.error',
            '.invalid-feedback',
            '.alert-danger',
            'text=required',
            'text=error'
        ]

        errors_found = []
        for selector in error_selectors:
            try:
                error_element = self.page.locator(selector).first
                if error_element.is_visible(timeout=1000):
                    error_text = error_element.inner_text()
                    errors_found.append(error_text)
                    print(f"   ⚠️ Error found: '{error_text}'")
            except:
                pass

        if not errors_found:
            print("   ℹ️ No error messages found on page")

        # Final validation report
        print("\n" + "=" * 70)
        print("VALIDATION REPORT")
        print("=" * 70)
        print(f"Last Name Field:")
        print(f"   • Value: '{last_name_value}' (empty)")
        print(f"   • Browser validation message: {last_name_validation if last_name_validation else 'None'}")
        print(f"   • Field valid: {last_name_validity}")
        print(f"\nForm Submission:")
        print(f"   • URL changed: {url_before != url_after}")
        print(f"   • Error messages found: {len(errors_found)}")
        print(f"   • Account created: {'Yes' if url_after != url_before else 'Checking...'}")

        print("\n✅ Step 7: Validation observed")

        # Summary
        print("\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        print("Test Scenario: Submit registration with EMPTY Last name field")
        print(f"\nResult:")

        if url_after != url_before:
            print("   ✓ Form was submitted (moved to new page)")
            print("   ✓ Last name field appears to be OPTIONAL")
        elif last_name_validation:
            print(f"   ✓ Validation triggered: '{last_name_validation}'")
            print("   ✓ Last name field appears to be REQUIRED")
        else:
            print("   ℹ️ Form behavior unclear - manual inspection recommended")

        print("=" * 70)

        print("\n✅ TEST COMPLETED: Validation Behavior Observed!\n")


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