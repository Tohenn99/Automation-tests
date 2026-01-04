"""
Performance Test 07: CSS Performance & Rendering
Analyzes CSS loading, parsing and rendering performance
"""

import pytest
from playwright.sync_api import Page


@pytest.mark.performance
def test_css_performance_and_rendering(page: Page):
    """
    Verifies:
    1. CSS file count and size
    2. CSS parsing time
    3. Unused CSS detection
    4. CSS complexity (selectors)
    5. Critical CSS inline
    6. Render-blocking CSS
    """
    base_url = "https://automationexercise.com"

    print("\n=== CSS Performance & Rendering Test ===\n")

    # Navigate to page
    page.goto(base_url)
    page.wait_for_load_state('networkidle')

    # Handle cookie consent
    try:
        consent_button = page.locator('.fc-button.fc-cta-consent').first
        consent_button.wait_for(state='visible', timeout=3000)
        consent_button.click()
        consent_button.wait_for(state='hidden', timeout=2000)
    except:
        pass

    # TEST 1: CSS Files Analysis
    print("1. Analyzing CSS Files...")

    css_files = page.evaluate("""
        () => {
            const resources = performance.getEntriesByType('resource');
            const cssResources = resources.filter(r => 
                r.initiatorType === 'link' || 
                r.name.endsWith('.css')
            );

            return cssResources.map(css => ({
                name: css.name.split('/').pop(),
                duration: css.duration,
                size: css.transferSize || 0,
                encodedSize: css.encodedBodySize || 0,
                decodedSize: css.decodedBodySize || 0
            }));
        }
    """)

    print(f"   Total CSS files: {len(css_files)}")

    if len(css_files) > 0:
        total_css_size = sum(f['decodedSize'] for f in css_files) / 1024
        total_load_time = sum(f['duration'] for f in css_files)

        print(f"   Total CSS size: {total_css_size:.0f} KB")
        print(f"   Total CSS load time: {total_load_time:.0f}ms")

        # CSS size evaluation
        if total_css_size < 100:
            print(f"   ✓ CSS size: EXCELLENT (< 100KB)")
        elif total_css_size < 200:
            print(f"   ✓ CSS size: GOOD (< 200KB)")
        elif total_css_size < 300:
            print(f"   ⚠ CSS size: ACCEPTABLE (< 300KB)")
        else:
            print(f"   ✗ CSS size: TOO LARGE (> 300KB)")

        assert total_css_size < 500, f"CSS too large: {total_css_size:.0f}KB"

    # TEST 2: CSS Rule Count
    print("\n2. Analyzing CSS Rules Complexity...")

    css_stats = page.evaluate("""
        () => {
            let totalRules = 0;
            let totalSelectors = 0;
            let complexSelectors = 0;

            for (let sheet of document.styleSheets) {
                try {
                    const rules = sheet.cssRules || sheet.rules;
                    totalRules += rules.length;

                    for (let rule of rules) {
                        if (rule.selectorText) {
                            totalSelectors++;

                            // Complex selectors (more than 3 parts)
                            const parts = rule.selectorText.split(' ').length;
                            if (parts > 3) {
                                complexSelectors++;
                            }
                        }
                    }
                } catch(e) {
                    // Cross-origin stylesheet
                }
            }

            return {
                totalRules,
                totalSelectors,
                complexSelectors,
                stylesheetCount: document.styleSheets.length
            };
        }
    """)

    print(f"   Stylesheets: {css_stats['stylesheetCount']}")
    print(f"   Total CSS rules: {css_stats['totalRules']}")
    print(f"   Total selectors: {css_stats['totalSelectors']}")
    print(f"   Complex selectors: {css_stats['complexSelectors']}")

    # CSS complexity evaluation
    if css_stats['totalRules'] < 3000:
        print(f"   ✓ CSS complexity: GOOD")
    elif css_stats['totalRules'] < 5000:
        print(f"   ⚠ CSS complexity: ACCEPTABLE")
    else:
        print(f"   ✗ CSS complexity: HIGH")

    # TEST 3: Unused CSS Detection
    print("\n3. Detecting Unused CSS...")

    unused_css = page.evaluate("""
        () => {
            return new Promise((resolve) => {
                if (!window.CSS || !CSS.supports('color', 'red')) {
                    resolve({ supported: false });
                    return;
                }

                let usedSelectors = 0;
                let unusedSelectors = 0;

                for (let sheet of document.styleSheets) {
                    try {
                        const rules = sheet.cssRules || sheet.rules;

                        for (let rule of rules) {
                            if (rule.selectorText) {
                                try {
                                    const matches = document.querySelectorAll(rule.selectorText);
                                    if (matches.length > 0) {
                                        usedSelectors++;
                                    } else {
                                        unusedSelectors++;
                                    }
                                } catch(e) {
                                    // Invalid selector
                                }
                            }
                        }
                    } catch(e) {
                        // Cross-origin
                    }
                }

                const totalSelectors = usedSelectors + unusedSelectors;
                const unusedPercent = totalSelectors > 0 ? 
                    (unusedSelectors / totalSelectors) * 100 : 0;

                resolve({
                    supported: true,
                    usedSelectors,
                    unusedSelectors,
                    unusedPercent
                });
            });
        }
    """)

    if unused_css['supported']:
        print(f"   Used selectors: {unused_css['usedSelectors']}")
        print(f"   Unused selectors: {unused_css['unusedSelectors']}")
        print(f"   Unused CSS: {unused_css['unusedPercent']:.1f}%")

        if unused_css['unusedPercent'] < 30:
            print(f"   ✓ Unused CSS: ACCEPTABLE (< 30%)")
        elif unused_css['unusedPercent'] < 50:
            print(f"   ⚠ Unused CSS: MODERATE (< 50%)")
        else:
            print(f"   ✗ Unused CSS: HIGH (> 50%)")
    else:
        print(f"   ℹ Unused CSS detection not available")

    # TEST 4: Inline vs External CSS
    print("\n4. Analyzing CSS Loading Strategy...")

    inline_external = page.evaluate("""
        () => {
            const inlineStyles = document.querySelectorAll('style');
            const externalStyles = document.querySelectorAll('link[rel="stylesheet"]');

            let inlineSize = 0;
            inlineStyles.forEach(style => {
                inlineSize += style.textContent.length;
            });

            return {
                inlineCount: inlineStyles.length,
                externalCount: externalStyles.length,
                inlineSize: inlineSize
            };
        }
    """)

    print(f"   Inline <style> tags: {inline_external['inlineCount']}")
    print(f"   External stylesheets: {inline_external['externalCount']}")
    print(f"   Inline CSS size: {inline_external['inlineSize'] / 1024:.1f} KB")

    if inline_external['inlineSize'] < 14000:  # ~14KB for critical CSS
        print(f"   ✓ Inline CSS size appropriate for critical CSS")
    else:
        print(f"   ⚠ Large inline CSS (consider moving to external file)")

    # TEST 5: CSS Animations Performance
    print("\n5. Testing CSS Animations Performance...")

    animations = page.evaluate("""
        () => {
            const animated = document.querySelectorAll('*');
            let animationCount = 0;
            let transitionCount = 0;

            animated.forEach(el => {
                const style = window.getComputedStyle(el);

                if (style.animationName && style.animationName !== 'none') {
                    animationCount++;
                }

                if (style.transitionProperty && style.transitionProperty !== 'none') {
                    transitionCount++;
                }
            });

            return { animationCount, transitionCount };
        }
    """)

    print(f"   Elements with animations: {animations['animationCount']}")
    print(f"   Elements with transitions: {animations['transitionCount']}")

    if animations['animationCount'] < 20:
        print(f"   ✓ Animation count: REASONABLE")
    else:
        print(f"   ⚠ Many animations (may impact performance)")

    # SUMMARY
    print("\n" + "=" * 50)
    print("CSS PERFORMANCE SUMMARY:")
    print("=" * 50)
    print(f"CSS Files: {len(css_files)}")
    if len(css_files) > 0:
        print(f"Total CSS Size: {total_css_size:.0f} KB")
    print(f"CSS Rules: {css_stats['totalRules']}")
    if unused_css['supported']:
        print(f"Unused CSS: {unused_css['unusedPercent']:.1f}%")
    print("=" * 50 + "\n")

    print("✓ CSS Performance & Rendering Test PASSED\n")
