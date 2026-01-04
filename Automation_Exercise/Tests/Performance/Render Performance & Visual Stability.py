"""
Performance Test 06: Render Performance & Visual Stability
Tests rendering speed, repaints, reflows, visual stability
"""

import pytest
from playwright.sync_api import Page


@pytest.mark.performance
def test_render_performance_and_visual_stability(page: Page):
    """
    Verifies:
    1. First Paint & First Contentful Paint
    2. Layout shifts (CLS)
    3. Repaints and reflows
    4. Critical rendering path
    5. Above-the-fold content
    6. Render-blocking resources
    """
    base_url = "https://automationexercise.com"

    print("\n=== Render Performance & Visual Stability Test ===\n")

    # Navigate to page
    page.goto(base_url)
    page.wait_for_load_state('domcontentloaded')

    # TEST 1: Paint Timing Metrics
    print("1. Measuring Paint Timing Metrics...")

    paint_metrics = page.evaluate("""
        () => {
            const paints = performance.getEntriesByType('paint');
            const fp = paints.find(p => p.name === 'first-paint');
            const fcp = paints.find(p => p.name === 'first-contentful-paint');

            // Get navigation timing
            const nav = performance.getEntriesByType('navigation')[0];

            return {
                firstPaint: fp ? fp.startTime : null,
                firstContentfulPaint: fcp ? fcp.startTime : null,
                domInteractive: nav ? nav.domInteractive : null,
                domContentLoaded: nav ? nav.domContentLoadedEventEnd - nav.domContentLoadedEventStart : null,
                domComplete: nav ? nav.domComplete : null
            };
        }
    """)

    if paint_metrics['firstPaint']:
        print(f"   First Paint: {paint_metrics['firstPaint']:.0f}ms")

    if paint_metrics['firstContentfulPaint']:
        fcp = paint_metrics['firstContentfulPaint']
        print(f"   First Contentful Paint: {fcp:.0f}ms")

        if fcp < 1800:
            print(f"   ✓ FCP: GOOD 🟢")
        elif fcp < 3000:
            print(f"   ⚠ FCP: NEEDS IMPROVEMENT 🟡")
        else:
            print(f"   ✗ FCP: POOR 🔴")

    if paint_metrics['domInteractive']:
        print(f"   DOM Interactive: {paint_metrics['domInteractive']:.0f}ms")

    if paint_metrics['domComplete']:
        print(f"   DOM Complete: {paint_metrics['domComplete']:.0f}ms")

    # TEST 2: Cumulative Layout Shift (CLS) - Visual Stability
    print("\n2. Measuring Visual Stability (CLS)...")

    # Wait for page to settle
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(3000)

    cls_data = page.evaluate("""
        () => {
            return new Promise((resolve) => {
                let clsScore = 0;
                const shifts = [];

                const observer = new PerformanceObserver((list) => {
                    for (const entry of list.getEntries()) {
                        if (!entry.hadRecentInput) {
                            clsScore += entry.value;
                            shifts.push({
                                value: entry.value,
                                time: entry.startTime,
                                sources: entry.sources ? entry.sources.length : 0
                            });
                        }
                    }
                });

                observer.observe({ type: 'layout-shift', buffered: true });

                setTimeout(() => {
                    observer.disconnect();
                    resolve({ clsScore, shifts, shiftCount: shifts.length });
                }, 2500);
            });
        }
    """)

    print(f"   Cumulative Layout Shift: {cls_data['clsScore']:.4f}")
    print(f"   Layout shift events: {cls_data['shiftCount']}")

    if cls_data['shiftCount'] > 0:
        largest_shift = max(cls_data['shifts'], key=lambda x: x['value'])
        print(f"   Largest shift: {largest_shift['value']:.4f} at {largest_shift['time']:.0f}ms")

    # Google CLS thresholds
    if cls_data['clsScore'] < 0.1:
        print(f"   ✓ CLS: GOOD 🟢 (< 0.1)")
    elif cls_data['clsScore'] < 0.25:
        print(f"   ⚠ CLS: NEEDS IMPROVEMENT 🟡 (< 0.25)")
    else:
        print(f"   ✗ CLS: POOR 🔴 (> 0.25)")

    assert cls_data['clsScore'] < 0.5, f"CLS too high: {cls_data['clsScore']}"

    # TEST 3: Render-Blocking Resources
    print("\n3. Analyzing Render-Blocking Resources...")

    blocking_resources = page.evaluate("""
        () => {
            const resources = performance.getEntriesByType('resource');

            const blocking = {
                css: [],
                js: [],
                count: 0
            };

            resources.forEach(r => {
                // Check CSS files
                if (r.initiatorType === 'link' && r.name.includes('.css')) {
                    blocking.css.push({
                        name: r.name.split('/').pop(),
                        duration: r.duration,
                        size: r.transferSize || 0
                    });
                    blocking.count++;
                }

                // Check synchronous JS (not async/defer)
                if (r.initiatorType === 'script' && r.name.includes('.js')) {
                    // Can't reliably detect async/defer from performance API
                    // but we can see if it blocks
                    if (r.startTime < 1000) {  // Early loading = potentially blocking
                        blocking.js.push({
                            name: r.name.split('/').pop(),
                            duration: r.duration,
                            size: r.transferSize || 0
                        });
                        blocking.count++;
                    }
                }
            });

            return blocking;
        }
    """)

    print(f"   Potential render-blocking CSS: {len(blocking_resources['css'])}")
    print(f"   Early-loading JS: {len(blocking_resources['js'])}")

    if len(blocking_resources['css']) > 0:
        print(f"   CSS files:")
        for css in blocking_resources['css'][:3]:
            print(f"      - {css['name'][:40]}: {css['duration']:.0f}ms")

    if len(blocking_resources['js']) > 0:
        print(f"   JS files:")
        for js in blocking_resources['js'][:3]:
            print(f"      - {js['name'][:40]}: {js['duration']:.0f}ms")

    # Blocking resources should be minimized
    if blocking_resources['count'] < 5:
        print(f"   ✓ Render-blocking resources: GOOD")
    elif blocking_resources['count'] < 10:
        print(f"   ⚠ Render-blocking resources: ACCEPTABLE")
    else:
        print(f"   ✗ Too many render-blocking resources")

    # TEST 4: Critical Rendering Path Analysis
    print("\n4. Analyzing Critical Rendering Path...")

    critical_path = page.evaluate("""
        () => {
            const nav = performance.getEntriesByType('navigation')[0];
            if (!nav) return null;

            return {
                // Time to start parsing HTML
                responseEnd: nav.responseEnd,

                // Time to finish parsing HTML (DOM ready)
                domInteractive: nav.domInteractive,

                // Time when all synchronous scripts done
                domContentLoaded: nav.domContentLoadedEventEnd,

                // Time when everything loaded
                loadComplete: nav.loadEventEnd,

                // Critical path length
                criticalPathLength: nav.domInteractive - nav.fetchStart
            };
        }
    """)

    if critical_path:
        print(f"   Response received: {critical_path['responseEnd']:.0f}ms")
        print(f"   DOM Interactive: {critical_path['domInteractive']:.0f}ms")
        print(f"   DOM Content Loaded: {critical_path['domContentLoaded']:.0f}ms")
        print(f"   Load Complete: {critical_path['loadComplete']:.0f}ms")
        print(f"   Critical path length: {critical_path['criticalPathLength']:.0f}ms")

        # Critical path should be < 3000ms
        if critical_path['criticalPathLength'] < 2000:
            print(f"   ✓ Critical path: FAST")
        elif critical_path['criticalPathLength'] < 3000:
            print(f"   ⚠ Critical path: ACCEPTABLE")
        else:
            print(f"   ✗ Critical path: SLOW")

    # TEST 5: Above-the-Fold Content Rendering
    print("\n5. Testing Above-the-Fold Content...")

    # Check if hero section is visible quickly
    viewport_height = page.viewport_size['height']

    # Get elements in viewport
    visible_content = page.evaluate(f"""
        (viewportHeight) => {{
            const elements = document.querySelectorAll('img, h1, h2, p');
            let aboveFold = 0;
            let totalSize = 0;

            elements.forEach(el => {{
                const rect = el.getBoundingClientRect();
                if (rect.top < viewportHeight) {{
                    aboveFold++;

                    // Estimate content size
                    if (el.tagName === 'IMG' && el.complete) {{
                        totalSize += el.naturalWidth * el.naturalHeight / 1000; // rough estimate
                    }}
                }}
            }});

            return {{ aboveFold, totalSize }};
        }}
    """, viewport_height)

    print(f"   Above-the-fold elements: {visible_content['aboveFold']}")

    # Check if images are lazy-loaded
    lazy_images = page.evaluate("""
        () => {
            const images = document.querySelectorAll('img');
            let lazyCount = 0;

            images.forEach(img => {
                if (img.loading === 'lazy') {
                    lazyCount++;
                }
            });

            return { total: images.length, lazy: lazyCount };
        }
    """)

    print(f"   Lazy-loaded images: {lazy_images['lazy']}/{lazy_images['total']}")

    if lazy_images['lazy'] > 0:
        print(f"   ✓ Lazy loading in use")
    else:
        print(f"   ℹ No lazy loading detected (all images load eagerly)")

    # TEST 6: Reflow/Repaint Detection
    print("\n6. Testing for Excessive Reflows...")

    # Trigger some interactions to check stability
    page.mouse.move(400, 400)
    page.wait_for_timeout(500)

    page.evaluate("window.scrollBy(0, 300)")
    page.wait_for_timeout(500)

    page.evaluate("window.scrollBy(0, -300)")
    page.wait_for_timeout(500)

    # Check if there were layout shifts during interaction
    interaction_cls = page.evaluate("""
        () => {
            return new Promise((resolve) => {
                let clsScore = 0;

                const observer = new PerformanceObserver((list) => {
                    for (const entry of list.getEntries()) {
                        if (!entry.hadRecentInput) {
                            clsScore += entry.value;
                        }
                    }
                });

                observer.observe({ type: 'layout-shift', buffered: false });

                setTimeout(() => {
                    observer.disconnect();
                    resolve(clsScore);
                }, 1000);
            });
        }
    """)

    if interaction_cls > 0:
        print(f"   ⚠ Layout shifts during interaction: {interaction_cls:.4f}")
    else:
        print(f"   ✓ No layout shifts during interaction")

    # TEST 7: Font Loading Strategy
    print("\n7. Analyzing Font Loading...")

    fonts = page.evaluate("""
        () => {
            if (!document.fonts) return null;

            const loadedFonts = [];
            document.fonts.forEach(font => {
                loadedFonts.push({
                    family: font.family,
                    status: font.status,
                    weight: font.weight,
                    style: font.style
                });
            });

            return {
                count: loadedFonts.length,
                fonts: loadedFonts
            };
        }
    """)

    if fonts:
        print(f"   Loaded fonts: {fonts['count']}")

        # Check font-display property
        font_display = page.evaluate("""
            () => {
                const styles = document.styleSheets;
                let hasSwap = false;

                try {
                    for (let sheet of styles) {
                        const rules = sheet.cssRules || [];
                        for (let rule of rules) {
                            if (rule.style && rule.style.fontDisplay === 'swap') {
                                hasSwap = true;
                                break;
                            }
                        }
                    }
                } catch(e) {
                    // CORS or other error
                }

                return hasSwap;
            }
        """)

        if font_display:
            print(f"   ✓ font-display: swap detected (prevents FOIT)")
        else:
            print(f"   ℹ font-display strategy not detected")

    # TEST 8: Skeleton Screens / Content Placeholders
    print("\n8. Checking for Loading States...")

    # Reload and check for loading indicators
    page.goto(base_url)

    # Quick check for loading indicators
    page.wait_for_timeout(100)

    loading_indicators = page.evaluate("""
        () => {
            const hasSpinner = document.querySelector('.spinner, .loader, .loading') !== null;
            const hasSkeleton = document.querySelector('.skeleton, .placeholder') !== null;
            const hasProgressBar = document.querySelector('progress, [role="progressbar"]') !== null;

            return {
                hasSpinner,
                hasSkeleton,
                hasProgressBar,
                hasAny: hasSpinner || hasSkeleton || hasProgressBar
            };
        }
    """)

    page.wait_for_load_state('networkidle')

    if loading_indicators['hasAny']:
        print(f"   ✓ Loading indicators found")
        if loading_indicators['hasSkeleton']:
            print(f"      - Skeleton screens detected")
        if loading_indicators['hasSpinner']:
            print(f"      - Spinner/loader detected")
    else:
        print(f"   ℹ No loading indicators (content may appear abruptly)")

    # TEST 9: Image Rendering Performance
    print("\n9. Analyzing Image Rendering...")

    image_stats = page.evaluate("""
        () => {
            const images = document.querySelectorAll('img');
            let withDimensions = 0;
            let withoutDimensions = 0;
            let total = images.length;

            images.forEach(img => {
                if (img.width && img.height) {
                    withDimensions++;
                } else {
                    withoutDimensions++;
                }
            });

            return { total, withDimensions, withoutDimensions };
        }
    """)

    print(f"   Total images: {image_stats['total']}")
    print(f"   Images with dimensions: {image_stats['withDimensions']}")
    print(f"   Images without dimensions: {image_stats['withoutDimensions']}")

    if image_stats['withoutDimensions'] > 0:
        print(f"   ⚠ {image_stats['withoutDimensions']} images lack width/height (may cause layout shifts)")
    else:
        print(f"   ✓ All images have dimensions specified")

    # SUMMARY
    print("\n" + "=" * 50)
    print("RENDER PERFORMANCE SUMMARY:")
    print("=" * 50)
    if paint_metrics['firstContentfulPaint']:
        print(f"FCP: {paint_metrics['firstContentfulPaint']:.0f}ms")
    print(f"CLS: {cls_data['clsScore']:.4f}")
    print(f"Layout Shifts: {cls_data['shiftCount']}")
    print(f"Render-blocking: {blocking_resources['count']} resources")
    if critical_path:
        print(f"Critical Path: {critical_path['criticalPathLength']:.0f}ms")
    print("=" * 50 + "\n")

    print("✓ Render Performance & Visual Stability Test PASSED\n")
