"""
Performance Test 01: Page Load Time & Core Web Vitals
Measures key page performance metrics
"""

import pytest
from playwright.sync_api import Page
import time


@pytest.mark.performance
def test_page_load_time_and_core_web_vitals(page: Page):
    """
    Measures:
    1. Total Page Load Time
    2. DOMContentLoaded time
    3. First Contentful Paint (FCP)
    4. Largest Contentful Paint (LCP)
    5. Time to Interactive (TTI)
    6. Cumulative Layout Shift (CLS)
    """
    base_url = "https://automationexercise.com"

    print("\n=== Page Load Time & Core Web Vitals Test ===\n")

    # TEST 1: Total Page Load Time
    print("1. Measuring Total Page Load Time...")

    start_time = time.time()
    page.goto(base_url)
    page.wait_for_load_state('domcontentloaded')
    dom_loaded_time = time.time() - start_time

    # Handle cookie consent if it appears
    try:
        consent_button = page.locator('.fc-button.fc-cta-consent').first
        consent_button.wait_for(state='visible', timeout=3000)
        consent_button.click()
        consent_button.wait_for(state='hidden', timeout=2000)
    except:
        pass

    page.wait_for_load_state('load')
    load_time = time.time() - start_time

    page.wait_for_load_state('networkidle')
    network_idle_time = time.time() - start_time

    print(f"   DOMContentLoaded: {dom_loaded_time:.2f}s")
    print(f"   Window Load: {load_time:.2f}s")
    print(f"   Network Idle: {network_idle_time:.2f}s")

    # Assertion: Page should load in < 5 seconds
    assert load_time < 5.0, f"Page load too slow: {load_time:.2f}s"
    print(f"   ✓ Page load time acceptable: {load_time:.2f}s")

    # TEST 2: Performance Navigation Timing
    print("\n2. Analyzing Performance Navigation Timing...")

    navigation_timing = page.evaluate("""
        () => {
            const timing = performance.timing;
            const navigation = performance.getEntriesByType('navigation')[0];

            return {
                redirectTime: timing.redirectEnd - timing.redirectStart,
                dnsTime: timing.domainLookupEnd - timing.domainLookupStart,
                tcpTime: timing.connectEnd - timing.connectStart,
                ttfb: timing.responseStart - timing.requestStart,
                downloadTime: timing.responseEnd - timing.responseStart,
                domProcessing: timing.domComplete - timing.domLoading,
                domInteractive: timing.domInteractive - timing.navigationStart,
                domComplete: timing.domComplete - timing.navigationStart,
                loadComplete: timing.loadEventEnd - timing.navigationStart,
                transferSize: navigation ? navigation.transferSize : 0,
                encodedBodySize: navigation ? navigation.encodedBodySize : 0,
                decodedBodySize: navigation ? navigation.decodedBodySize : 0
            };
        }
    """)

    print(f"   DNS Lookup: {navigation_timing['dnsTime']}ms")
    print(f"   TCP Connection: {navigation_timing['tcpTime']}ms")
    print(f"   TTFB (Time to First Byte): {navigation_timing['ttfb']}ms")
    print(f"   Download Time: {navigation_timing['downloadTime']}ms")
    print(f"   DOM Processing: {navigation_timing['domProcessing']}ms")
    print(f"   DOM Interactive: {navigation_timing['domInteractive']}ms")

    # TTFB rating
    ttfb = navigation_timing['ttfb']
    if ttfb < 600:
        print(f"   ✓ TTFB: EXCELLENT 🟢 ({ttfb}ms)")
        ttfb_rating = "EXCELLENT"
    elif ttfb < 1000:
        print(f"   ✓ TTFB: GOOD 🟡 ({ttfb}ms)")
        ttfb_rating = "GOOD"
    elif ttfb < 1500:
        print(f"   ⚠ TTFB: FAIR 🟠 ({ttfb}ms)")
        ttfb_rating = "FAIR"
    else:
        print(f"   ✗ TTFB: POOR 🔴 ({ttfb}ms)")
        ttfb_rating = "POOR"

    assert ttfb < 1500, f"TTFB too slow: {ttfb}ms"

    # TEST 3: Core Web Vitals – Paint Metrics
    print("\n3. Measuring Paint Metrics (Core Web Vitals)...")

    paint_metrics = page.evaluate("""
        () => {
            const paints = performance.getEntriesByType('paint');
            const fcp = paints.find(p => p.name === 'first-contentful-paint');
            const fp = paints.find(p => p.name === 'first-paint');

            return {
                firstPaint: fp ? fp.startTime : null,
                firstContentfulPaint: fcp ? fcp.startTime : null
            };
        }
    """)

    if paint_metrics['firstPaint']:
        print(f"   First Paint (FP): {paint_metrics['firstPaint']:.0f}ms")

    fcp_rating = "N/A"
    if paint_metrics['firstContentfulPaint']:
        fcp = paint_metrics['firstContentfulPaint']
        print(f"   First Contentful Paint (FCP): {fcp:.0f}ms")

        if fcp < 1800:
            print("   ✓ FCP: GOOD 🟢")
            fcp_rating = "GOOD"
        elif fcp < 3000:
            print("   ⚠ FCP: NEEDS IMPROVEMENT 🟡")
            fcp_rating = "NEEDS IMPROVEMENT"
        else:
            print("   ✗ FCP: POOR 🔴")
            fcp_rating = "POOR"

        assert fcp < 4000, f"FCP too slow: {fcp}ms"

    # TEST 4: Largest Contentful Paint (LCP)
    print("\n4. Measuring Largest Contentful Paint (LCP)...")

    page.wait_for_load_state('networkidle')

    lcp_metric = page.evaluate("""
        () => {
            return new Promise((resolve) => {
                let lcp = 0;

                const observer = new PerformanceObserver((list) => {
                    const entries = list.getEntries();
                    const lastEntry = entries[entries.length - 1];
                    lcp = lastEntry.renderTime || lastEntry.loadTime;
                });

                observer.observe({ type: 'largest-contentful-paint', buffered: true });

                setTimeout(() => {
                    observer.disconnect();
                    resolve(lcp);
                }, 1000);
            });
        }
    """)

    lcp_rating = "N/A"
    if lcp_metric > 0:
        print(f"   Largest Contentful Paint (LCP): {lcp_metric:.0f}ms")

        if lcp_metric < 2500:
            print("   ✓ LCP: GOOD 🟢")
            lcp_rating = "GOOD"
        elif lcp_metric < 4000:
            print("   ⚠ LCP: NEEDS IMPROVEMENT 🟡")
            lcp_rating = "NEEDS IMPROVEMENT"
        else:
            print("   ✗ LCP: POOR 🔴")
            lcp_rating = "POOR"

        assert lcp_metric < 5000, f"LCP too slow: {lcp_metric}ms"
    else:
        print("   ℹ LCP metric not available")

    # TEST 5: Time to Interactive (TTI)
    print("\n5. Measuring Time to Interactive...")

    tti = page.evaluate("""
        () => {
            return new Promise((resolve) => {
                if (document.readyState === 'complete') {
                    resolve(performance.now());
                } else {
                    window.addEventListener('load', () => {
                        requestIdleCallback(() => {
                            resolve(performance.now());
                        }, { timeout: 5000 });
                    });
                }
            });
        }
    """)

    print(f"   Time to Interactive (TTI): {tti:.0f}ms")

    if tti < 3800:
        print("   ✓ TTI: GOOD 🟢")
        tti_rating = "GOOD"
    elif tti < 7300:
        print("   ⚠ TTI: NEEDS IMPROVEMENT 🟡")
        tti_rating = "NEEDS IMPROVEMENT"
    else:
        print("   ✗ TTI: POOR 🔴")
        tti_rating = "POOR"

    # TEST 6: Cumulative Layout Shift (CLS)
    print("\n6. Measuring Cumulative Layout Shift (CLS)...")

    page.wait_for_load_state('networkidle')

    cls_score = page.evaluate("""
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

                observer.observe({ type: 'layout-shift', buffered: true });

                setTimeout(() => {
                    observer.disconnect();
                    resolve(clsScore);
                }, 2000);
            });
        }
    """)

    print(f"   Cumulative Layout Shift (CLS): {cls_score:.3f}")

    if cls_score < 0.1:
        print("   ✓ CLS: GOOD 🟢")
        cls_rating = "GOOD"
    elif cls_score < 0.25:
        print("   ⚠ CLS: NEEDS IMPROVEMENT 🟡")
        cls_rating = "NEEDS IMPROVEMENT"
    else:
        print("   ✗ CLS: POOR 🔴")
        cls_rating = "POOR"

    # SUMMARY
    print("\n" + "=" * 50)
    print("CORE WEB VITALS SUMMARY:")
    print("=" * 50)
    print(f"Page Load Time: {load_time:.2f}s")
    print(f"TTFB: {ttfb}ms - {ttfb_rating}")
    if paint_metrics['firstContentfulPaint']:
        print(f"FCP: {paint_metrics['firstContentfulPaint']:.0f}ms - {fcp_rating}")
    if lcp_metric > 0:
        print(f"LCP: {lcp_metric:.0f}ms - {lcp_rating}")
    print(f"TTI: {tti:.0f}ms - {tti_rating}")
    print(f"CLS: {cls_score:.3f} - {cls_rating}")

    # Overall score calculation
    scores = []
    if ttfb_rating in ["EXCELLENT", "GOOD"]:
        scores.append(1)
    elif ttfb_rating == "FAIR":
        scores.append(0.5)
    else:
        scores.append(0)

    if fcp_rating == "GOOD":
        scores.append(1)
    elif fcp_rating == "NEEDS IMPROVEMENT":
        scores.append(0.5)
    elif fcp_rating == "POOR":
        scores.append(0)

    if lcp_rating == "GOOD":
        scores.append(1)
    elif lcp_rating == "NEEDS IMPROVEMENT":
        scores.append(0.5)
    elif lcp_rating == "POOR":
        scores.append(0)

    if tti_rating == "GOOD":
        scores.append(1)
    elif tti_rating == "NEEDS IMPROVEMENT":
        scores.append(0.5)
    elif tti_rating == "POOR":
        scores.append(0)

    if cls_rating == "GOOD":
        scores.append(1)
    elif cls_rating == "NEEDS IMPROVEMENT":
        scores.append(0.5)
    elif cls_rating == "POOR":
        scores.append(0)

    overall_score = (sum(scores) / len(scores)) * 100 if scores else 0

    print(f"\nOverall Performance Score: {overall_score:.0f}/100")

    if overall_score >= 90:
        print("Overall Rating: EXCELLENT 🟢")
    elif overall_score >= 70:
        print("Overall Rating: GOOD 🟡")
    elif overall_score >= 50:
        print("Overall Rating: FAIR 🟠")
    else:
        print("Overall Rating: NEEDS IMPROVEMENT 🔴")

    print("=" * 50 + "\n")

    print("✓ Page Load Time & Core Web Vitals Test PASSED\n")
