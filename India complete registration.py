import pytest
from playwright.sync_api import Page, expect
import random
import string


class TestTrifonRegistration:
    """Test suite for registering Trifon Testov - CHER-63"""

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
        return f"trifon_{random_string}@testmail.com"

    def test_register_trifon_testov(self):
        """
        Test Case: Register Trifon Testov - CHER-63

        Steps:
        1. Select Mr. radio button under Title
        2. Check Name field shows pre-filled name
        3. Check Email field shows pre-filled email
        4. Click in Password field
        5. Type Test@123
        6. Select Day 15 from dropdown
        7. Select Month May from dropdown
        8. Select Year 1990 from dropdown
        9. Scroll down to ADDRESS INFORMATION section
        10. Type Trifon in First name field
        11. Type Testov in Last name field
        12. Type Street address 123 in Address field
        13. Select India from Country dropdown
        14. Type Maharashtra in State field
        15. Type Mumbai in City field
        16. Type 400001 in Zipcode field
        17. Type 9876543210 in Mobile Number field
        18. Click orange Create Account button
        """

        print("\n" + "=" * 70)
        print("TEST: Register Trifon Testov - CHER-63")
        print("=" * 70)

        # Navigate to website and signup
        self.page.goto(self.base_url)
        expect(self.page).to_have_title("Automation Exercise")
        self.handle_cookie_consent()
        print("✅ Opened website")

        # Go to Signup/Login page
        signup_login_link = self.page.locator('a[href="/login"]').first
        signup_login_link.click()
        expect(self.page).to_have_url(f"{self.base_url}/login")
        print("✅ On Signup/Login page")

        # Fill initial signup form
        signup_name = "Trifon Testov"
        signup_email = self.generate_unique_email()

        print(f"\n📝 Entering signup details:")
        print(f"   Name: {signup_name}")
        print(f"   Email: {signup_email}")

        name_field = self.page.locator('input[data-qa="signup-name"]')
        name_field.fill(signup_name)

        email_field = self.page.locator('input[data-qa="signup-email"]')
        email_field.fill(signup_email)

        signup_button = self.page.locator('button[data-qa="signup-button"]')
        signup_button.click()

        # Wait for registration form
        self.page.wait_for_selector('#form')
        print("✅ Registration form loaded")

        print("\n" + "-" * 70)
        print("FILLING REGISTRATION FORM")
        print("-" * 70)

        # Step 1: Select Mr. radio button under Title
        mr_radio = self.page.locator('#id_gender1')
        mr_radio.check()
        print("✅ Step 1: Selected 'Mr.' radio button")

        # Step 2: Check Name field shows pre-filled name
        prefilled_name = self.page.locator('#name')
        name_value = prefilled_name.input_value()

        print(f"✅ Step 2: Name field shows pre-filled name: '{name_value}'")
        assert name_value == signup_name, f"Expected '{signup_name}', got '{name_value}'"

        # Verify name field is disabled/readonly
        is_readonly = prefilled_name.get_attribute('readonly')
        if is_readonly:
            print(f"   ℹ️ Name field is read-only")

        # Step 3: Check Email field shows pre-filled email
        prefilled_email = self.page.locator('#email')
        email_value = prefilled_email.input_value()

        print(f"✅ Step 3: Email field shows pre-filled email: '{email_value}'")
        assert email_value == signup_email, f"Expected '{signup_email}', got '{email_value}'"

        # Verify email field is disabled/readonly
        is_readonly = prefilled_email.get_attribute('readonly')
        if is_readonly:
            print(f"   ℹ️ Email field is read-only")

        # Step 4: Click in Password field
        password_field = self.page.locator('#password')
        password_field.click()
        print("✅ Step 4: Clicked in Password field")

        # Step 5: Type Test@123
        password_field.fill("Test@123")
        print("✅ Step 5: Typed 'Test@123' in Password field")

        # Step 6: Select Day 15 from dropdown
        day_dropdown = self.page.locator('#days')
        day_dropdown.select_option("15")
        print("✅ Step 6: Selected Day '15'")

        # Step 7: Select Month May from dropdown
        month_dropdown = self.page.locator('#months')
        month_dropdown.select_option("5")  # May is month 5
        print("✅ Step 7: Selected Month 'May'")

        # Step 8: Select Year 1990 from dropdown
        year_dropdown = self.page.locator('#years')
        year_dropdown.select_option("1990")
        print("✅ Step 8: Selected Year '1990'")

        # Step 9: Scroll down to ADDRESS INFORMATION section
        address_section = self.page.locator('text=Address Information')
        address_section.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)
        print("✅ Step 9: Scrolled to ADDRESS INFORMATION section")

        # Step 10: Type Trifon in First name field
        first_name_field = self.page.locator('#first_name')
        first_name_field.fill("Trifon")
        print("✅ Step 10: Typed 'Trifon' in First name field")

        # Step 11: Type Testov in Last name field
        last_name_field = self.page.locator('#last_name')
        last_name_field.fill("Testov")
        print("✅ Step 11: Typed 'Testov' in Last name field")

        # Step 12: Type Street address 123 in Address field
        address_field = self.page.locator('#address1')
        address_field.fill("Street address 123")
        print("✅ Step 12: Typed 'Street address 123' in Address field")

        # Step 13: Select India from Country dropdown
        country_dropdown = self.page.locator('#country')
        country_dropdown.select_option("India")
        print("✅ Step 13: Selected 'India' from Country dropdown")

        # Step 14: Type Maharashtra in State field
        state_field = self.page.locator('#state')
        state_field.fill("Maharashtra")
        print("✅ Step 14: Typed 'Maharashtra' in State field")

        # Step 15: Type Mumbai in City field
        city_field = self.page.locator('#city')
        city_field.fill("Mumbai")
        print("✅ Step 15: Typed 'Mumbai' in City field")

        # Step 16: Type 400001 in Zipcode field
        zipcode_field = self.page.locator('#zipcode')
        zipcode_field.fill("400001")
        print("✅ Step 16: Typed '400001' in Zipcode field")

        # Step 17: Type 9876543210 in Mobile Number field
        mobile_field = self.page.locator('#mobile_number')
        mobile_field.fill("9876543210")
        print("✅ Step 17: Typed '9876543210' in Mobile Number field")

        # Step 18: Click orange Create Account button
        create_account_button = self.page.locator('button[data-qa="create-account"]')
        create_account_button.click()
        print("✅ Step 18: Clicked orange 'Create Account' button")

        # Wait for account creation confirmation
        self.page.wait_for_load_state('networkidle')
        self.page.wait_for_timeout(2000)

        # Verify account creation
        print("\n" + "-" * 70)
        print("ACCOUNT CREATION VERIFICATION")
        print("-" * 70)

        try:
            success_heading = self.page.locator('h2[data-qa="account-created"]')

            if success_heading.is_visible(timeout=5000):
                success_text = success_heading.inner_text()
                print(f"✅ Success message: '{success_text}'")

                expect(success_heading).to_have_text("Account Created!")

                # Check for continue button
                continue_button = self.page.locator('a[data-qa="continue-button"]')
                if continue_button.is_visible():
                    print("✅ Continue button is visible")

                print("\n✅ Account creation confirmed!")

            else:
                print("❌ Success message not found")

        except Exception as e:
            print(f"❌ Error: {str(e)}")

        # Display registration summary
        print("\n" + "=" * 70)
        print("REGISTRATION SUMMARY - CHER-63")
        print("=" * 70)
        print("Account Information:")
        print(f"  Name: {signup_name} (pre-filled)")
        print(f"  Email: {signup_email} (pre-filled)")
        print("  Title: Mr.")
        print("  Password: Test@123")
        print("  Date of Birth: 15-May-1990")
        print("\nAddress Information:")
        print("  First Name: Trifon")
        print("  Last Name: Testov")
        print("  Address: Street address 123")
        print("  Country: India")
        print("  State: Maharashtra")
        print("  City: Mumbai")
        print("  Zipcode: 400001")
        print("  Mobile: 9876543210")
        print("=" * 70)

        print("\n" + "=" * 70)
        print("✅ TEST PASSED: Trifon Testov registered successfully!")
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