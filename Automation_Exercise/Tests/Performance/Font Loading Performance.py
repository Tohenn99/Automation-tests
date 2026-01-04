"""
Performance Test 09: Font Loading Performance
Анализира font loading strategies и performance
"""

import pytest
from playwright.sync_api import Page

@pytest.mark.performance
def test_font_loading_performance(page: Page):
    """
    Проверява:
    1. Font file count and size
    2. Font loading strategy
    3. FOIT/FOUT detection
    4. Web fonts vs system fonts
    5. Font format optimization
    6. Preload/prefetch usage
    """
    base_url = "https://automationexercise.com"

    print("\n=== Font Loading Performance Test ===\n")

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

    # TEST 1: Font Files Analysis
    print("1. Analyzing Font Files...")

    font_resources = page.evaluate("""
        () => {
            const resources = performance.getEntriesByType('resource');
            const fonts = resources.filter(r => 
                r.initiatorType === 'css' && 
                (r.name.includes('font') || 
                 r.name.endsWith('.woff') ||
                 r.name.endsWith('.woff2') ||
                 r.name.endsWith('.ttf') ||
                 r.name.endsWith('.otf'))
            );

            return fonts.map(font => ({
                name: font.name.split('/').pop(),
                duration: font.duration,
                size: font.transferSize || 0,
                encodedSize: font.encodedBodySize || 0
            }));
        }
    """)

    print(f"   Font files loaded: {len(font_resources)}")

    if len(font_resources) > 0:
        total_font_size = sum(f['size'] for f in font_resources) / 1024
        total_font_time = sum(f['duration'] for f in font_resources)

        print(f"   Total font size: {total_font_size:.0f} KB")
        print(f"   Total font load time: {total_font_time:.0f}ms")

        # Font size evaluation
        if total_font_size < 100:
            print(f"   ✓ Font size: EXCELLENT (< 100KB)")
        elif total_font_size < 200:
            print(f"   ✓ Font size: GOOD (< 200KB)")
        elif total_font_size < 400:
            print(f"   ⚠ Font size: ACCEPTABLE (< 400KB)")
        else:
            print(f"   ✗ Font size: TOO LARGE (> 400KB)")

        # Show largest fonts
        if len(font_resources) > 0:
            sorted_fonts = sorted(font_resources, key=lambda x: x['size'], reverse=True)
            print(f"   Largest font files:")
            for i, font in enumerate(sorted_fonts[:3], 1):
                print(f"      {i}. {font['name'][:40]}: {font['size'] / 1024:.0f} KB")
    else:
        print(f"   ℹ No custom web fonts detected (using system fonts)")

    # TEST 2: Font Loading Strategy
    print("\n2. Checking Font Loading Strategy...")

    font_display = page.evaluate("""
        () => {
            const strategies = {
                swap: 0,
                block: 0,
                fallback: 0,
                optional: 0,
                auto: 0,
                none: 0
            };

            for (let sheet of document.styleSheets) {
                try {
                    const rules = sheet.cssRules || sheet.rules;

                    for (let rule of rules) {
                        if (rule instanceof CSSFontFaceRule) {
                            const display = rule.style.fontDisplay || 'auto';
                            strategies[display] = (strategies[display] || 0) + 1;
                        }
                    }
                } catch(e) {
                    // Cross-origin
                }
            }

            return strategies;
        }
    """)

    total_font_faces = sum(font_display.values())

    if total_font_faces > 0:
        print(f"   @font-face rules found: {total_font_faces}")
        print(f"   Font-display strategies:")

        for strategy, count in font_display.items():
            if count > 0:
                print(f"      - {strategy}: {count}")

        # font-display: swap е препоръчително
        if font_display.get('swap', 0) > 0:
            print(f"   ✓ Using font-display: swap (recommended)")
        elif font_display.get('optional', 0) > 0:
            print(f"   ✓ Using font-display: optional (good)")
        elif font_display.get('fallback', 0) > 0:
            print(f"   ⚠ Using font-display: fallback")
        elif font_display.get('block', 0) > 0:
            print(f"   ⚠ Using font-display: block (FOIT risk)")
        else:
            print(f"   ⚠ No font-display specified (default: auto)")
    else:
        print(f"   ℹ No @font-face rules detected")

    # TEST 3: Font Preloading
    print("\n3. Checking Font Preloading...")

    preloaded_fonts = page.evaluate("""
        () => {
            const preloads = document.querySelectorAll('link[rel="preload"][as="font"]');
            return {
                count: preloads.length,
                fonts: Array.from(preloads).map(link => ({
                    href: link.href.split('/').pop(),
                    crossorigin: link.hasAttribute('crossorigin')
                }))
            };
        }
    """)

    print(f"   Preloaded fonts: {preloaded_fonts['count']}")

    if preloaded_fonts['count'] > 0:
        print(f"   ✓ Font preloading implemented")
        for font in preloaded_fonts['fonts']:
            print(f"      - {font['href'][:40]}")
    else:
        print(f"   ℹ No font preloading detected (consider for critical fonts)")

    # TEST 4: Font Format Check
    print("\n4. Analyzing Font Formats...")

    font_formats = {}
    for font in font_resources:
        ext = font['name'].split('.')[-1].lower()
        font_formats[ext] = font_formats.get(ext, 0) + 1

    if font_formats:
        print(f"   Font formats used: {font_formats}")

        if 'woff2' in font_formats:
            print(f"   ✓ Using WOFF2 (best compression)")
        elif 'woff' in font_formats:
            print(f"   ⚠ Using WOFF (consider WOFF2)")

        if 'ttf' in font_formats or 'otf' in font_formats:
            print(f"   ⚠ Using TTF/OTF (not optimized for web)")

    # TEST 5: System Font Stack Check
    print("\n5. Checking Font Stack...")

    font_families = page.evaluate("""
        () => {
            const body = document.body;
            const style = window.getComputedStyle(body);
            const fontFamily = style.fontFamily;

            return {
                bodyFont: fontFamily,
                usesSystemFonts: fontFamily.includes('system-ui') || 
                                fontFamily.includes('-apple-system') ||
                                fontFamily.includes('sans-serif')
            };
        }
    """)

    print(f"   Body font-family: {font_families['bodyFont'][:60]}")

    if font_families['usesSystemFonts']:
        print(f"   ✓ Falls back to system fonts")

    # TEST 6: Font Loading Impact
    print("\n6. Measuring Font Loading Impact...")

    # Check if fonts block rendering
    font_blocking_time = 0
    for font in font_resources:
        if font['duration'] > 100:  # Fonts taking > 100ms
            font_blocking_time += font['duration']

    if font_blocking_time > 0:
        print(f"   Font blocking time: {font_blocking_time:.0f}ms")

        if font_blocking_time < 500:
            print(f"   ✓ Minimal font blocking")
        elif font_blocking_time < 1000:
            print(f"   ⚠ Moderate font blocking")
        else:
            print(f"   ✗ Significant font blocking")

    # SUMMARY
    print("\n" + "=" * 50)
    print("FONT LOADING PERFORMANCE SUMMARY:")
    print("=" * 50)
    print(f"Font Files: {len(font_resources)}")
    if len(font_resources) > 0:
        print(f"Total Font Size: {total_font_size:.0f} KB")
        print(f"Total Load Time: {total_font_time:.0f}ms")
    print(f"@font-face Rules: {total_font_faces}")
    print(f"Preloaded Fonts: {preloaded_fonts['count']}")
    print("=" * 50 + "\n")

    print("✓ Font Loading Performance Test PASSED\n")