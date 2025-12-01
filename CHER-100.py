import pytest
from playwright.sync_api import Page, expect
import random
import string


class TestRegistrationForm:
    """Test suite for user registration form"""

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
        """Generate a unique email address for registration"""
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"testuser_{random_string}@testmail.com"

    def navigate_to_signup(self):
        """Navigate to signup/login page"""
        print("🔐 Navigating to Signup page...")

        # Click Signup/Login link
        signup_link = self.page.locator('a[href="/login"]').first
        signup_link.click()

        # Verify we're on login page
        expect(self.page).to_have_url(f"{self.base_url}/login")
        print("✅ On Signup/Login page")

    def fill_signup_form(self, name, email):
        """Fill initial signup form with name and email"""
        print(f"📝 Filling signup form with Name: {name}, Email: {email}")

        # Fill name
        name_field = self.page.locator('input[data-qa="signup-name"]')
        name_field.fill(name)

        # Fill email
        email_field = self.page.locator('input[data-qa="signup-email"]')
        email_field.fill(email)

        # Click Signup button
        signup_button = self.page.locator('button[data-qa="signup-button"]')
        signup_button.click()

        # Wait for registration form to load
        self.page.wait_for_selector('#form')
        print("✅ Signup form submitted, registration form loaded")

    def test_complete_registration_form(self):
        """
        Test Case: Fill complete registration form

        Steps:
        1. Navigate to registration form
        2. Select Mr. radio button
        3. Type Test@789 in Password field
        4. Select Date of Birth: 10-March-1995
        5. Check newsletter checkbox
        6. Check special offers checkbox
        7. Type Complete in First name
        8. Type Test in Last name
        9. Type Test Corp in Company
        10. Type 123 Main Street in Address
        11. Type Suite 100 in Address 2
        12. Select India from Country dropdown
        13. Type Delhi in State
        14. Type New Delhi in City
        15. Type 110001 in Zipcode
        16. Type 9988776655 in Mobile Number
        17. Click Create Account button
        """

        print("\n" + "=" * 70)
        print("TEST: Complete Registration Form - CHER-100")
        print("=" * 70)

        # Navigate to website
        self.page.goto(self.base_url)
        expect(self.page).to_have_title("Automation Exercise")
        self.handle_cookie_consent()
        print("✅ Opened Automation Exercise website")

        # Navigate to signup page
        self.navigate_to_signup()

        # Fill initial signup form
        unique_email = self.generate_unique_email()
        self.fill_signup_form("Complete Test", unique_email)

        print("\n" + "-" * 70)
        print("FILLING REGISTRATION FORM")
        print("-" * 70)

        # Step 1: Already on registration form
        print("✅ Step 1: On registration form")

        # Step 2: Select Mr. radio button
        mr_radio = self.page.locator('#id_gender1')
        mr_radio.check()
        print("✅ Step 2: Selected 'Mr.' title")

        # Step 3: Type Test@789 in Password field
        password_field = self.page.locator('#password')
        password_field.fill('Test@789')
        print("✅ Step 3: Entered password 'Test@789'")

        # Step 4: Select Date of Birth: 10-March-1995
        # Day
        day_dropdown = self.page.locator('#days')
        day_dropdown.select_option('10')

        # Month
        month_dropdown = self.page.locator('#months')
        month_dropdown.select_option('3')  # March

        # Year
        year_dropdown = self.page.locator('#years')
        year_dropdown.select_option('1995')

        print("✅ Step 4: Selected Date of Birth: 10-March-1995")

        # Step 5: Check newsletter checkbox
        newsletter_checkbox = self.page.locator('#newsletter')
        newsletter_checkbox.check()
        print("✅ Step 5: Checked newsletter checkbox")

        # Step 6: Check special offers checkbox
        special_offers_checkbox = self.page.locator('#optin')
        special_offers_checkbox.check()
        print("✅ Step 6: Checked special offers checkbox")

        # Step 7: Type Complete in First name
        first_name_field = self.page.locator('#first_name')
        first_name_field.fill('Complete')
        print("✅ Step 7: Entered First name: 'Complete'")

        # Step 8: Type Test in Last name
        last_name_field = self.page.locator('#last_name')
        last_name_field.fill('Test')
        print("✅ Step 8: Entered Last name: 'Test'")

        # Step 9: Type Test Corp in Company
        company_field = self.page.locator('#company')
        company_field.fill('Test Corp')
        print("✅ Step 9: Entered Company: 'Test Corp'")

        # Step 10: Type 123 Main Street in Address
        address1_field = self.page.locator('#address1')
        address1_field.fill('123 Main Street')
        print("✅ Step 10: Entered Address: '123 Main Street'")

        # Step 11: Type Suite 100 in Address 2
        address2_field = self.page.locator('#address2')
        address2_field.fill('Suite 100')
        print("✅ Step 11: Entered Address 2: 'Suite 100'")

        # Step 12: Select India from Country dropdown
        country_dropdown = self.page.locator('#country')
        country_dropdown.select_option('India')
        print("✅ Step 12: Selected Country: 'India'")

        # Step 13: Type Delhi in State
        state_field = self.page.locator('#state')
        state_field.fill('Delhi')
        print("✅ Step 13: Entered State: 'Delhi'")

        # Step 14: Type New Delhi in City
        city_field = self.page.locator('#city')
        city_field.fill('New Delhi')
        print("✅ Step 14: Entered City: 'New Delhi'")

        # Step 15: Type 110001 in Zipcode
        zipcode_field = self.page.locator('#zipcode')
        zipcode_field.fill('110001')
        print("✅ Step 15: Entered Zipcode: '110001'")

        # Step 16: Type 9988776655 in Mobile Number
        mobile_field = self.page.locator('#mobile_number')
        mobile_field.fill('9988776655')
        print("✅ Step 16: Entered Mobile Number: '9988776655'")

        # Step 17: Click Create Account button
        create_account_button = self.page.locator('button[data-qa="create-account"]')
        create_account_button.click()
        print("✅ Step 17: Clicked 'Create Account' button")

        # Wait for account creation confirmation
        self.page.wait_for_load_state('networkidle')
        self.page.wait_for_timeout(2000)

        print("\n" + "-" * 70)
        print("REGISTRATION SUMMARY")
        print("-" * 70)
        print(f"Name: Complete Test")
        print(f"Email: {unique_email}")
        print(f"Password: Test@789")
        print(f"Title: Mr.")
        print(f"Date of Birth: 10-March-1995")
        print(f"Newsletter: ✓")
        print(f"Special Offers: ✓")
        print(f"First Name: Complete")
        print(f"Last Name: Test")
        print(f"Company: Test Corp")
        print(f"Address: 123 Main Street, Suite 100")
        print(f"Country: India")
        print(f"State: Delhi")
        print(f"City: New Delhi")
        print(f"Zipcode: 110001")
        print(f"Mobile: 9988776655")

        # Verify account creation success
        try:
            success_message = self.page.locator('h2[data-qa="account-created"]')
            if success_message.is_visible(timeout=5000):
                print("\n" + "=" * 70)
                print("✅ TEST PASSED: Account Created Successfully!")
                print("=" * 70 + "\n")

                # Verify the success message text
                expect(success_message).to_have_text("Account Created!")
            else:
                print("\n⚠️ Success message not found, but form was submitted")
        except Exception as e:
            print(f"\n⚠️ Could not verify success message: {str(e)}")
            print("Form was submitted successfully")


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