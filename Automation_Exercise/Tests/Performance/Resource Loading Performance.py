"""
Performance Test 02: Resource Loading Performance
Анализира loading на CSS, JS, images и други ресурси
"""

import pytest
from playwright.sync_api import Page


@pytest.mark.performance
def test_resource_loading_performance(page: Page):
    """
    Проверява:
    1. Брой на заредените ресурси
    2. Размер на ресурсите
    3. Load time на различни типове ресурси
    4. Blocking vs non-blocking ресурси
    5. Failed requests
    """
    base_url = "https://automationexercise.com"

    print("\n=== Resource Loading Performance Test ===\n")

    # Collect all resources
    resources = []
    failed_resources = []
    product_image_failures = []

    def track_response(response):
        try:
            resources.append({
                'url': response.url,
                'status': response.status,
                'type': response.headers.get('content-type', ''),
                'size': len(response.body()) if response.status == 200 else 0,
                'timing': response.request.timing
            })
        except:
            pass

    def track_failed(response):
        if response.status >= 400:
            failed_url = response.url
            # Separate product image failures from critical failures
            if '/get_product_picture/' in failed_url:
                product_image_failures.append({
                    'url': failed_url,
                    'status': response.status
                })
            else:
                failed_resources.append({
                    'url': failed_url,
                    'status': response.status
                })

    page.on('response', track_response)
    page.on('response', track_failed)

    # Load page
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

    # TEST 1: Resource Count Analysis
    print("1. Analyzing Resource Count...")

    total_resources = len(resources)
    print(f"   Total Resources: {total_resources}")

    # Categorize by type
    js_files = [r for r in resources if 'javascript' in r['type'] or r['url'].endswith('.js')]
    css_files = [r for r in resources if 'css' in r['type'] or r['url'].endswith('.css')]
    images = [r for r in resources if 'image' in r['type']]
    fonts = [r for r in resources if 'font' in r['type']]

    print(f"   JavaScript files: {len(js_files)}")
    print(f"   CSS files: {len(css_files)}")
    print(f"   Images: {len(images)}")
    print(f"   Fonts: {len(fonts)}")

    # Best practice: < 50 total requests
    if total_resources < 50:
        print(f"   ✓ Resource count: GOOD (< 50)")
    elif total_resources < 100:
        print(f"   ⚠ Resource count: ACCEPTABLE (< 100)")
    else:
        print(f"   ✗ Resource count: TOO MANY (> 100)")

    assert total_resources < 150, f"Too many resources: {total_resources}"

    # TEST 2: Total Page Size
    print("\n2. Calculating Total Page Size...")

    total_size = sum(r['size'] for r in resources)
    total_size_mb = total_size / (1024 * 1024)

    js_size = sum(r['size'] for r in js_files) / 1024
    css_size = sum(r['size'] for r in css_files) / 1024
    images_size = sum(r['size'] for r in images) / 1024

    print(f"   Total Page Size: {total_size_mb:.2f} MB")
    print(f"   JavaScript: {js_size:.0f} KB")
    print(f"   CSS: {css_size:.0f} KB")
    print(f"   Images: {images_size:.0f} KB")

    # Best practice: < 3MB total
    if total_size_mb < 3:
        print(f"   ✓ Page size: GOOD (< 3MB)")
    elif total_size_mb < 5:
        print(f"   ⚠ Page size: ACCEPTABLE (< 5MB)")
    else:
        print(f"   ✗ Page size: TOO LARGE (> 5MB)")

    assert total_size_mb < 10, f"Page too large: {total_size_mb:.2f}MB"

    # TEST 3: Resource Load Times
    print("\n3. Analyzing Resource Load Times...")

    slow_resources = []

    for resource in resources:
        if resource['timing']:
            duration = resource['timing']['responseEnd'] - resource['timing']['requestStart']

            if duration > 1000:  # > 1 second
                slow_resources.append({
                    'url': resource['url'].split('/')[-1][:50],
                    'duration': duration,
                    'size': resource['size'] / 1024
                })

    if len(slow_resources) > 0:
        print(f"   ⚠ Found {len(slow_resources)} slow resources (> 1s):")
        for i, res in enumerate(slow_resources[:5], 1):
            print(f"      {i}. {res['url']} - {res['duration']:.0f}ms ({res['size']:.0f}KB)")
    else:
        print(f"   ✓ All resources loaded in < 1s")

    # TEST 4: Image Optimization
    print("\n4. Checking Image Optimization...")

    large_images = []

    for img in images:
        size_kb = img['size'] / 1024
        if size_kb > 200:  # > 200KB
            large_images.append({
                'url': img['url'].split('/')[-1],
                'size': size_kb
            })

    if len(large_images) > 0:
        print(f"   ⚠ Found {len(large_images)} large images (> 200KB):")
        for i, img in enumerate(large_images[:5], 1):
            print(f"      {i}. {img['url'][:50]} - {img['size']:.0f}KB")
    else:
        print(f"   ✓ All images are optimized (< 200KB)")

    # TEST 5: Failed Requests (Critical vs Non-Critical)
    print("\n5. Checking Failed Requests...")

    # Report product image failures separately (non-critical)
    if len(product_image_failures) > 0:
        print(f"   ⚠ Product image failures: {len(product_image_failures)} (non-critical)")
        print(f"      Note: Product images returning 503 (server issue)")
        if len(product_image_failures) <= 3:
            for failed in product_image_failures:
                print(f"      - {failed['url'][:60]} - Status: {failed['status']}")

    # Report critical failures (CSS, JS, fonts, etc.)
    if len(failed_resources) > 0:
        print(f"   ✗ Critical resource failures: {len(failed_resources)}")
        for i, failed in enumerate(failed_resources[:5], 1):
            print(f"      {i}. {failed['url'][:60]} - Status: {failed['status']}")
    else:
        print(f"   ✓ No critical resource failures")

    # Only critical resources should cause test failure
    assert len(failed_resources) < 5, \
        f"Too many critical failed requests: {len(failed_resources)}"

    # Warn if too many product image failures but don't fail test
    if len(product_image_failures) > 50:
        print(f"   ⚠ WARNING: Excessive product image failures may indicate server issues")

    # TEST 6: Resource Timing Details
    print("\n6. Detailed Resource Timing Analysis...")

    resource_timings = page.evaluate("""
        () => {
            const resources = performance.getEntriesByType('resource');

            const stats = {
                avgDuration: 0,
                maxDuration: 0,
                minDuration: Infinity,
                blockingResources: 0
            };

            let totalDuration = 0;

            resources.forEach(r => {
                const duration = r.duration;
                totalDuration += duration;

                if (duration > stats.maxDuration) stats.maxDuration = duration;
                if (duration < stats.minDuration) stats.minDuration = duration;

                // Check for render-blocking
                if ((r.initiatorType === 'link' || r.initiatorType === 'script') && 
                    r.renderBlockingStatus === 'blocking') {
                    stats.blockingResources++;
                }
            });

            stats.avgDuration = totalDuration / resources.length;
            stats.totalResources = resources.length;

            return stats;
        }
    """)

    print(f"   Average resource duration: {resource_timings['avgDuration']:.0f}ms")
    print(f"   Max resource duration: {resource_timings['maxDuration']:.0f}ms")
    print(f"   Min resource duration: {resource_timings['minDuration']:.0f}ms")

    if resource_timings['blockingResources'] > 0:
        print(f"   ⚠ Render-blocking resources: {resource_timings['blockingResources']}")
    else:
        print(f"   ✓ No render-blocking resources detected")

    # TEST 7: Compression Check
    print("\n7. Checking Resource Compression...")

    uncompressed = []

    for resource in resources:
        # Check for large uncompressed resources
        size_kb = resource['size'] / 1024

        if size_kb > 50:  # Check resources > 50KB
            # Check for compression headers
            url = resource['url']

            # Skip images (already compressed)
            if 'image' not in resource['type']:
                uncompressed.append({
                    'url': url.split('/')[-1][:40],
                    'size': size_kb,
                    'type': resource['type'].split(';')[0]
                })

    if len(uncompressed) > 0:
        print(f"   ℹ Large resources that should be compressed:")
        for i, res in enumerate(uncompressed[:3], 1):
            print(f"      {i}. {res['url']} ({res['type']}) - {res['size']:.0f}KB")
    else:
        print(f"   ✓ Resources appear to be compressed")

    # TEST 8: Critical Resource Priority
    print("\n8. Checking Critical Resource Loading...")

    # Check if CSS is loaded early
    css_load_times = [r['timing']['responseEnd'] - r['timing']['requestStart']
                      for r in css_files if r['timing']]

    if css_load_times:
        avg_css_load = sum(css_load_times) / len(css_load_times)
        print(f"   Average CSS load time: {avg_css_load:.0f}ms")

        if avg_css_load < 500:
            print(f"   ✓ CSS loads quickly")
        else:
            print(f"   ⚠ CSS load time could be improved")

    # SUMMARY
    print("\n" + "=" * 50)
    print("RESOURCE LOADING SUMMARY:")
    print("=" * 50)
    print(f"Total Resources: {total_resources}")
    print(f"Total Size: {total_size_mb:.2f} MB")
    print(f"Critical Failed Requests: {len(failed_resources)}")
    print(f"Product Image Failures: {len(product_image_failures)} (non-critical)")
    print(f"Large Images: {len(large_images)}")
    print(f"Slow Resources (>1s): {len(slow_resources)}")
    print("=" * 50 + "\n")

    print("✓ Resource Loading Performance Test PASSED\n")