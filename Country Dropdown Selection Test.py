import pytest
from playwright.sync_api import Page, expect
import random
import string


class TestCountryDropdown:
    """Test suite for validating country dropdown selections"""

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

    def select_and_verify_country(self, country_name, step_number):
        """Select a country and verify it's selected"""
        print(f"\n{'=' * 70}")
        print(f"STEP {step_number}: Selecting {country_name.upper()}")
        print(f"{'=' * 70}")

        country_dropdown = self.page.locator('#country')

        # Click dropdown
        print(f"🖱️ Clicking Country dropdown...")
        country_dropdown.click()
        self.page.wait_for_timeout(300)

        # Select country
        print(f"📍 Selecting '{country_name}'...")
        country_dropdown.select_option(country_name)
        self.page.wait_for_timeout(500)

        # Get selected value
        selected_value = country_dropdown.input_value()

        # Get selected option text
        selected_text = country_dropdown.evaluate(
            "el => el.options[el.selectedIndex].text"
        )

        print(f"   Selected value: '{selected_value}'")
        print(f"   Selected text: '{selected_text}'")

        # Verify selection
        if selected_text == country_name or selected_value == country_name:
            print(f"✅ {country_name} is SELECTED")
            return True
        else:
            print(f"❌ {country_name} is NOT selected")
            print(f"   Expected: {country_name}")
            print(f"   Found: {selected_text}")
            return False

    def test_country_dropdown_selections(self):
        """
        Test Case: Test country dropdown with multiple selections - 81

        Steps:
        - Navigate to registration form
        - Select India and verify
        - Select United States and verify
        - Select Canada and verify
        - Select Australia and verify
        - Select Israel and verify
        - Select New Zealand and verify
        - Select Singapore and verify
        """

        print("\n" + "=" * 70)
        print("TEST: Country Dropdown Multiple Selection Test")
        print("=" * 70)

        # Navigate to website
        print("\n🌐 Opening website...")
        self.page.goto(self.base_url)
        expect(self.page).to_have_title("Automation Exercise")
        self.handle_cookie_consent()
        print("✅ Opened website")

        # Navigate to registration form
        print("\n📝 Navigating to registration form...")

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
        print("✅ Registration form loaded")

        # Scroll to country dropdown
        print("\n📜 Scrolling to Country dropdown...")
        country_dropdown = self.page.locator('#country')
        country_dropdown.scroll_into_view_if_needed()
        self.page.wait_for_timeout(500)
        print("✅ Country dropdown visible")

        # Track results
        countries_to_test = [
            "India",
            "United States",
            "Canada",
            "Australia",
            "Israel",
            "New Zealand",
            "Singapore"
        ]

        results = {}
        step = 1

        # Test each country
        for country in countries_to_test:
            result = self.select_and_verify_country(country, step)
            results[country] = result
            step += 2  # Each selection takes 2 steps (click dropdown + select)

        # Final verification summary
        print("\n" + "=" * 70)
        print("COUNTRY DROPDOWN TEST SUMMARY")
        print("=" * 70)

        print("\n📊 Selection Results:")

        all_passed = True
        for country, passed in results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"   {status} - {country}")
            if not passed:
                all_passed = False

        # Statistics
        total = len(results)
        passed = sum(1 for result in results.values() if result)
        failed = total - passed

        print(f"\n📈 Statistics:")
        print(f"   Total countries tested: {total}")
        print(f"   Passed: {passed}")
        print(f"   Failed: {failed}")
        print(f"   Success rate: {(passed / total) * 100:.1f}%")

        # Current selection
        country_dropdown = self.page.locator('#country')
        final_selection = country_dropdown.evaluate(
            "el => el.options[el.selectedIndex].text"
        )

        print(f"\n🌍 Final Country Selection: {final_selection}")

        # Assertions
        print("\n" + "=" * 70)
        print("ASSERTIONS")
        print("=" * 70)

        for country, passed in results.items():
            assert passed, f"Country '{country}' should be selectable"
            print(f"✓ {country} selection verified")

        assert all_passed, "All country selections should work correctly"
        print("\n✅ All country selections work correctly")

        # Test details
        print("\n" + "=" * 70)
        print("TEST DETAILS")
        print("=" * 70)
        print("Countries tested in order:")
        for i, country in enumerate(countries_to_test, 1):
            print(f"   {i}. {country}")

        print(f"\nDropdown behavior:")
        print(f"   ✓ Dropdown clickable")
        print(f"   ✓ Countries selectable")
        print(f"   ✓ Selection updates correctly")
        print(f"   ✓ Multiple selections work")

        print("\n" + "=" * 70)
        print("✅ TEST PASSED: Country Dropdown Works Correctly!")
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
    pytest.main([__file__, "-v", "-s", "--headed"])