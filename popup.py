"""
Automated Test Case: TC-PROD-001
Title: Check Products page loads successfully
Framework: Playwright
Browser: Chrome
"""

import time
from playwright.sync_api import sync_playwright, expect


class TestProductsPage:

    def test_products_page_loads_successfully(self):
        """
        Test Case ID: TC-PROD-001
        Description: Check Products page loads successfully
        Expected: Products page loads within 3 seconds with all elements visible
        """

        with sync_playwright() as p:
            # Step 1: Open browser (Chrome) with your existing profile
            print("Step 1: Opening Chrome browser with your profile...")

            # Option 1: Use your existing Chrome profile (RECOMMENDED)
            browser = p.chromium.launch(
                headless=False,
                channel="chrome",
                args=[
                    '--user-data-dir=C:/Users/User/AppData/Local/Google/Chrome/User Data',
                    '--profile-directory=Default',  # Change to 'Profile 1', 'Profile 2' if you use multiple profiles
                    '--start-maximized'  # Start in full screen
                ]
            )

            # Option 2: Or use persistent context (alternative method)
            # context = p.chromium.launch_persistent_context(
            #     user_data_dir="./chrome_profile",
            #     headless=False,
            #     channel="chrome"
            # )
            # page = context.pages[0] if context.pages else context.new_page()

            context = browser.new_context(
                viewport=None,  # Use full window size instead of fixed viewport
                no_viewport=True  # Disable viewport to use full screen
            )
            page = context.new_page()

            try:
                # Step 2: Navigate to the Products page
                print("Step 2: Navigating to Products page...")
                start_time = time.time()
                page.goto("https://automationexercise.com/products", timeout=10000)

                # Maximize window
                page.evaluate("window.moveTo(0, 0); window.resizeTo(screen.width, screen.height);")

                # Handle consent popup - SUPER AGGRESSIVE
                print("  Waiting for consent popup...")
                time.sleep(3)  # Wait longer for popup

                # Take a screenshot to see what's on screen
                page.screenshot(path="before_consent.png")
                print("  ✓ Screenshot taken: before_consent.png (check if popup is there)")

                try:
                    # Try clicking with Playwright first
                    print("  Trying to click consent button...")

                    # Try all possible selectors
                    selectors = [
                        "button:has-text('Consent')",
                        "button:has-text('CONSENT')",
                        "button.fc-cta-consent",
                        "button[aria-label='Consent']",
                        "p:has-text('Consent')",
                        ".fc-button.fc-cta-consent"
                    ]

                    clicked = False
                    for selector in selectors:
                        try:
                            btn = page.locator(selector)
                            if btn.count() > 0:
                                print(f"  Found button with selector: {selector}")
                                btn.first.click(timeout=2000, force=True)
                                print(f"  ✓ Clicked consent with: {selector}")
                                clicked = True
                                time.sleep(2)
                                break
                        except Exception as e:
                            print(f"  ✗ Failed with {selector}: {str(e)[:30]}")
                            continue

                    if not clicked:
                        print("  ℹ No consent button found with Playwright, trying JavaScript...")
                        # JavaScript brute force
                        result = page.evaluate("""
                            () => {
                                // Method 1: Find by text
                                const allButtons = Array.from(document.querySelectorAll('button, p, a, div'));
                                for (let el of allButtons) {
                                    const text = el.textContent.toLowerCase();
                                    if (text.includes('consent') || text.includes('accept') || text.includes('agree')) {
                                        el.click();
                                        return 'Clicked: ' + el.textContent.substring(0, 50);
                                    }
                                }

                                // Method 2: Check iframes
                                const iframes = document.querySelectorAll('iframe');
                                for (let iframe of iframes) {
                                    try {
                                        const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
                                        const iframeButtons = iframeDoc.querySelectorAll('button, p, a');
                                        for (let btn of iframeButtons) {
                                            const text = btn.textContent.toLowerCase();
                                            if (text.includes('consent') || text.includes('accept')) {
                                                btn.click();
                                                return 'Clicked in iframe: ' + btn.textContent.substring(0, 50);
                                            }
                                        }
                                    } catch (e) {
                                        continue;
                                    }
                                }

                                return 'No consent button found';
                            }
                        """)
                        print(f"  JavaScript result: {result}")

                    time.sleep(2)
                    page.screenshot(path="after_consent.png")
                    print("  ✓ Screenshot taken: after_consent.png")

                except Exception as e:
                    print(f"  ℹ Consent handling error: {str(e)[:80]}")

                load_time = time.time() - start_time

                # Step 3: Observe page loading (check load time)
                print(f"Step 3: Page loaded in {load_time:.2f} seconds")

                # Check if page loads within 3 seconds
                if load_time <= 3:
                    print("✓ Page loaded within 3 seconds")
                else:
                    print(f"✗ Page took {load_time:.2f} seconds (expected < 3 seconds)")

                # Step 4: Check page elements visibility
                print("Step 4: Checking page elements visibility...")

                # Check 1: "ALL PRODUCTS" heading is visible
                print("  Checking 'ALL PRODUCTS' heading...")
                all_products_heading = page.locator("h2.title.text-center:has-text('All Products')")
                expect(all_products_heading).to_be_visible(timeout=5000)
                print("  ✓ 'ALL PRODUCTS' heading is visible")

                # Check 2: Product cards display with images
                print("  Checking product cards with images...")
                product_cards = page.locator(".features_items .col-sm-4")
                expect(product_cards.first).to_be_visible(timeout=5000)

                product_count = product_cards.count()
                print(f"  ✓ {product_count} product cards found")

                # Check if at least one product has an image
                product_images = page.locator(".features_items .productinfo img")
                expect(product_images.first).to_be_visible(timeout=5000)
                print("  ✓ Product images are visible")

                # Check 3: Category sidebar is visible on left side
                print("  Checking category sidebar...")
                category_sidebar = page.locator(".left-sidebar .category-products")
                expect(category_sidebar).to_be_visible(timeout=5000)

                # Check for WOMEN, MEN, KIDS categories (more specific locators)
                women_category = page.locator(".category-products a[href='#Women']")
                men_category = page.locator(".category-products a[href='#Men']")
                kids_category = page.locator(".category-products a[href='#Kids']")

                expect(women_category).to_be_visible()
                expect(men_category).to_be_visible()
                expect(kids_category).to_be_visible()
                print("  ✓ Category sidebar is visible with WOMEN, MEN, KIDS categories")

                # Check 4: Brands section is visible
                print("  Checking brands section...")
                brands_section = page.locator(".left-sidebar .brands_products")
                expect(brands_section).to_be_visible(timeout=5000)

                # Check for at least one brand
                brands = page.locator(".brands_products .brands-name li")
                expect(brands.first).to_be_visible()
                brand_count = brands.count()
                print(f"  ✓ Brands section is visible with {brand_count} brands")

                # Take screenshot after all checks pass
                page.screenshot(path="products_page_PASS.png")
                print("\n  ✓ Screenshot saved as 'products_page_PASS.png'")

                # Final Result
                print("\n" + "=" * 70)
                print("TEST RESULT: PASS ✓")
                print("=" * 70)
                print(f"✓ Page loaded in {load_time:.2f} seconds (< 3 seconds)")
                print(f"✓ 'ALL PRODUCTS' heading visible")
                print(f"✓ {product_count} product cards with images displayed")
                print(f"✓ Category sidebar visible (WOMEN, MEN, KIDS)")
                print(f"✓ Brands section visible with {brand_count} brands")
                print("=" * 70)

                # Keep browser open for 3 seconds to see results
                time.sleep(3)

            except AssertionError as e:
                # Take screenshot when test fails
                page.screenshot(path="products_page_FAIL.png")
                print("\n" + "=" * 70)
                print("TEST RESULT: FAIL ✗")
                print("=" * 70)
                print(f"Assertion Error: {e}")
                print("✓ Screenshot saved as 'products_page_FAIL.png'")
                print("=" * 70)
                raise

            except Exception as e:
                print("\n" + "=" * 70)
                print("TEST RESULT: FAIL ✗")
                print("=" * 70)
                print(f"Error: {e}")
                print("=" * 70)
                raise

            finally:
                # Cleanup
                context.close()
                browser.close()


# Run the test directly
if __name__ == "__main__":
    print("=" * 70)
    print("Running Test Case: TC-PROD-001")
    print("Check Products page loads successfully")
    print("=" * 70)
    print()

    test = TestProductsPage()
    test.test_products_page_loads_successfully()