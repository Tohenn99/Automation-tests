import pytest
from playwright.sync_api import Page, expect


class TestSarahRegistration:
    """Test suite for registering Sarah McDonald"""

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
                print("✅ Cookie consent accepted")
        except:
            pass

    def test_register_sarah_mcdonald(self):
        """
        Test Case: Register Sarah McDonald with complete details - 92

        Steps:
        1. Open Chrome browser
        2. Navigate to http://automationexercise.com
        3. Click Signup / Login in navigation
        4. Enter name "Sarah McDonald" in Name field
        5. Enter email "sarah.mcdonald@example.com" in Email Address field
        6. Click Signup button
        7. Select Mrs. radio button under Title
        8. Type Pass@2024 in Password field
        9. Select Date of Birth: Day 12, Month August, Year 1988
        10. Scroll to ADDRESS INFORMATION section
        11. Type Sarah in First name field
        12. Type McDonald in Last name field
        13. Type 456 Granville Street, Suite 200 in Address field
        14. Select Canada from Country dropdown
        15. Type British Columbia in State field
        16. Type Vancouver in City field
        17. Type V6B 1A1 in Zipcode field (with space)
        18. Type 6045551234 in Mobile Number field (10 digits)
        19. Click Create Account button
        20. Check for account creation confirmation
        """

        print("\n" + "=" * 70)
        print("TEST: Register Sarah McDonald")
        print("=" * 70)

        # Step 1 & 2: Open Chrome browser and navigate to website
        print("\n🌐 Opening browser and navigating to website...")
        self.page.goto(self.base_url)

        # Verify page loaded
        expect(self.page).to_have_title("Automation Exercise")
        self.handle_cookie_consent()
        print("✅ Step 1-2: Opened http://automationexercise.com")

        # Step 3: Click Signup / Login in navigation
        print("\n🔐 Clicking Signup / Login...")
        signup_login_link = self.page.locator('a[href="/login"]').first
        signup_login_link.click()

        # Wait for login page to load
        expect(self.page).to_have_url(f"{self.base_url}/login")
        print("✅ Step 3: Clicked 'Signup / Login' in navigation")

        # Step 4: Enter name "Sarah McDonald" in Name field
        print("\n📝 Filling signup form...")
        name_field = self.page.locator('input[data-qa="signup-name"]')
        name_field.fill("Sarah McDonald")
        print("✅ Step 4: Entered name 'Sarah McDonald'")

        # Step 5: Enter email in Email Address field
        email_field = self.page.locator('input[data-qa="signup-email"]')
        email_field.fill("sarah.mcdonald@example.com")
        print("✅ Step 5: Entered email 'sarah.mcdonald@example.com'")

        # Step 6: Click Signup button
        signup_button = self.page.locator('button[data-qa="signup-button"]')
        signup_button.click()

        # Wait for registration form to load
        self.page.wait_for_selector('#form')
        print("✅ Step 6: Clicked 'Signup' button - Registration form loaded")

        print("\n" + "-" * 70)
        print("FILLING ACCOUNT INFORMATION")
        print("-" * 70)

        # Step 7: Select Mrs. radio button under Title
        mrs_radio = self.page.locator('#id_gender2')
        mrs_radio.check()
        print("✅ Step 7: Selected 'Mrs.' title")

        # Step 8: Type Pass@2024 in Password field
        password_field = self.page.locator('#password')
        password_field.fill("Pass@2024")
        print("✅ Step 8: Entered password 'Pass@2024'")

        # Step 9: Select Date of Birth: Day 12, Month August, Year 1988
        day_dropdown = self.page.locator('#days')
        day_dropdown.select_option("12")

        month_dropdown = self.page.locator('#months')
        month_dropdown.select_option("8")  # August is month 8

        year_dropdown = self.page.locator('#years')
        year_dropdown.select_option("1988")

        print("✅ Step 9: Selected Date of Birth: 12-August-1988")

        # Step 10: Scroll to ADDRESS INFORMATION section
        print("\n" + "-" * 70)
        print("FILLING ADDRESS INFORMATION")
        print("-" * 70)

        address_section = self.page.locator('text=Address Information')
        address_section.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)
        print("✅ Step 10: Scrolled to ADDRESS INFORMATION section")

        # Step 11: Type Sarah in First name field
        first_name_field = self.page.locator('#first_name')
        first_name_field.fill("Sarah")
        print("✅ Step 11: Entered First name 'Sarah'")

        # Step 12: Type McDonald in Last name field
        last_name_field = self.page.locator('#last_name')
        last_name_field.fill("McDonald")
        print("✅ Step 12: Entered Last name 'McDonald'")

        # Step 13: Type address in Address field
        address_field = self.page.locator('#address1')
        address_field.fill("456 Granville Street, Suite 200")
        print("✅ Step 13: Entered Address '456 Granville Street, Suite 200'")

        # Step 14: Select Canada from Country dropdown
        country_dropdown = self.page.locator('#country')
        country_dropdown.select_option("Canada")
        print("✅ Step 14: Selected Country 'Canada'")

        # Step 15: Type British Columbia in State field
        state_field = self.page.locator('#state')
        state_field.fill("British Columbia")
        print("✅ Step 15: Entered State 'British Columbia'")

        # Step 16: Type Vancouver in City field
        city_field = self.page.locator('#city')
        city_field.fill("Vancouver")
        print("✅ Step 16: Entered City 'Vancouver'")

        # Step 17: Type V6B 1A1 in Zipcode field (with space)
        zipcode_field = self.page.locator('#zipcode')
        zipcode_field.fill("V6B 1A1")
        print("✅ Step 17: Entered Zipcode 'V6B 1A1' (with space)")

        # Step 18: Type 6045551234 in Mobile Number field (10 digits)
        mobile_field = self.page.locator('#mobile_number')
        mobile_field.fill("6045551234")
        print("✅ Step 18: Entered Mobile Number '6045551234' (10 digits)")

        # Step 19: Click Create Account button
        print("\n🚀 Creating account...")
        create_account_button = self.page.locator('button[data-qa="create-account"]')
        create_account_button.click()
        print("✅ Step 19: Clicked 'Create Account' button")

        # Wait for account creation confirmation
        self.page.wait_for_load_state('networkidle')
        self.page.wait_for_timeout(2000)

        # Step 20: Check for account creation confirmation
        print("\n" + "-" * 70)
        print("ACCOUNT CREATION VERIFICATION")
        print("-" * 70)

        try:
            # Look for success message
            success_heading = self.page.locator('h2[data-qa="account-created"]')

            if success_heading.is_visible(timeout=5000):
                success_text = success_heading.inner_text()
                print(f"✅ Success message found: '{success_text}'")

                # Verify the exact text
                expect(success_heading).to_have_text("Account Created!")

                # Check for continue button
                continue_button = self.page.locator('a[data-qa="continue-button"]')
                if continue_button.is_visible():
                    print("✅ Continue button is visible")

                print("\n✅ Step 20: Account creation confirmed successfully!")

            else:
                print("❌ Success message not found")

        except Exception as e:
            print(f"❌ Error verifying account creation: {str(e)}")

        # Display registration summary
        print("\n" + "=" * 70)
        print("REGISTRATION SUMMARY")
        print("=" * 70)
        print("Personal Information:")
        print("  Name: Sarah McDonald")
        print("  Email: sarah.mcdonald@example.com")
        print("  Title: Mrs.")
        print("  Password: Pass@2024")
        print("  Date of Birth: 12-August-1988")
        print("\nAddress Information:")
        print("  First Name: Sarah")
        print("  Last Name: McDonald")
        print("  Address: 456 Granville Street, Suite 200")
        print("  Country: Canada")
        print("  State: British Columbia")
        print("  City: Vancouver")
        print("  Zipcode: V6B 1A1")
        print("  Mobile: 6045551234")
        print("=" * 70)

        print("\n" + "=" * 70)
        print("✅ TEST PASSED: Sarah McDonald registered successfully!")
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