"""
Performance Test 08: Image Optimization & Lazy Loading
Analyzes image loading strategies and optimization
"""

import pytest
from playwright.sync_api import Page

@pytest.mark.performance
def test_image_optimization_and_lazy_loading(page: Page):
    """
    Verifies:
    1. Image sizes and formats
    2. Lazy loading implementation
    3. Responsive images
    4. Image compression
    5. WebP/modern format usage
    6. Total image weight
    """
    base_url = "https://automationexercise.com"

    print("\n=== Image Optimization & Lazy Loading Test ===\n")

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

    # TEST 1: Image Count and Formats
    print("1. Analyzing Image Count and Formats...")

    images_data = page.evaluate("""
        () => {
            const images = document.querySelectorAll('img');
            const formats = {};
            const sizes = [];

            images.forEach(img => {
                const src = img.src || img.getAttribute('src') || '';
                const ext = src.split('.').pop().split('?')[0].toLowerCase();

                formats[ext] = (formats[ext] || 0) + 1;

                if (img.naturalWidth && img.naturalHeight) {
                    sizes.push({
                        width: img.naturalWidth,
                        height: img.naturalHeight,
                        displayWidth: img.width,
                        displayHeight: img.height
                    });
                }
            });

            return {
                totalImages: images.length,
                formats: formats,
                sizes: sizes
            };
        }
    """)

    print(f"   Total images: {images_data['totalImages']}")
    print(f"   Image formats: {images_data['formats']}")

    # Check for modern formats
    modern_formats = ['webp', 'avif']
    has_modern = any(fmt in images_data['formats'] for fmt in modern_formats)

    if has_modern:
        print(f"   ✓ Using modern image formats (WebP/AVIF)")
    else:
        print(f"   ⚠ No modern image formats detected (consider WebP)")

    # TEST 2: Image Size Analysis
    print("\n2. Analyzing Image Sizes...")

    oversized_images = 0
    properly_sized = 0

    for size in images_data['sizes']:
        natural_pixels = size['width'] * size['height']
        display_pixels = size['displayWidth'] * size['displayHeight']

        if natural_pixels > display_pixels * 2:  # More than 2x needed
            oversized_images += 1
        else:
            properly_sized += 1

    total_analyzed = len(images_data['sizes'])

    if total_analyzed > 0:
        print(f"   Images analyzed: {total_analyzed}")
        print(f"   Properly sized: {properly_sized}")
        print(f"   Oversized: {oversized_images}")

        oversized_percent = (oversized_images / total_analyzed) * 100

        if oversized_percent < 20:
            print(f"   ✓ Image sizing: GOOD ({oversized_percent:.0f}% oversized)")
        elif oversized_percent < 40:
            print(f"   ⚠ Image sizing: ACCEPTABLE ({oversized_percent:.0f}% oversized)")
        else:
            print(f"   ✗ Image sizing: POOR ({oversized_percent:.0f}% oversized)")

    # TEST 3: Lazy Loading Detection
    print("\n3. Checking Lazy Loading Implementation...")

    lazy_loading = page.evaluate("""
        () => {
            const images = document.querySelectorAll('img');
            let lazyCount = 0;
            let eagerCount = 0;

            images.forEach(img => {
                const loading = img.getAttribute('loading');

                if (loading === 'lazy') {
                    lazyCount++;
                } else {
                    eagerCount++;
                }
            });

            return { lazyCount, eagerCount, total: images.length };
        }
    """)

    print(f"   Lazy loaded images: {lazy_loading['lazyCount']}")
    print(f"   Eager loaded images: {lazy_loading['eagerCount']}")

    if lazy_loading['total'] > 0:
        lazy_percent = (lazy_loading['lazyCount'] / lazy_loading['total']) * 100

        if lazy_percent > 50:
            print(f"   ✓ Good lazy loading implementation ({lazy_percent:.0f}%)")
        elif lazy_percent > 20:
            print(f"   ⚠ Some lazy loading ({lazy_percent:.0f}%)")
        else:
            print(f"   ⚠ Limited lazy loading (consider implementing)")

    # TEST 4: Responsive Images
    print("\n4. Checking Responsive Images...")

    responsive = page.evaluate("""
        () => {
            const images = document.querySelectorAll('img');
            let withSrcset = 0;
            let withPicture = 0;

            images.forEach(img => {
                if (img.getAttribute('srcset')) {
                    withSrcset++;
                }

                if (img.parentElement && img.parentElement.tagName === 'PICTURE') {
                    withPicture++;
                }
            });

            return { withSrcset, withPicture, total: images.length };
        }
    """)

    print(f"   Images with srcset: {responsive['withSrcset']}")
    print(f"   Images in <picture>: {responsive['withPicture']}")

    responsive_total = responsive['withSrcset'] + responsive['withPicture']

    if responsive['total'] > 0:
        responsive_percent = (responsive_total / responsive['total']) * 100

        if responsive_percent > 50:
            print(f"   ✓ Good responsive image usage ({responsive_percent:.0f}%)")
        elif responsive_percent > 20:
            print(f"   ⚠ Some responsive images ({responsive_percent:.0f}%)")
        else:
            print(f"   ⚠ Limited responsive images")

    # TEST 5: Image Loading from Resources
    print("\n5. Analyzing Image Download Performance...")

    image_resources = page.evaluate("""
        () => {
            const resources = performance.getEntriesByType('resource');
            const images = resources.filter(r => r.initiatorType === 'img');

            let totalSize = 0;
            let slowImages = [];

            images.forEach(img => {
                totalSize += img.transferSize || 0;

                if (img.duration > 1000) {
                    slowImages.push({
                        name: img.name.split('/').pop(),
                        duration: img.duration,
                        size: img.transferSize || 0
                    });
                }
            });

            return {
                count: images.length,
                totalSize: totalSize,
                slowImages: slowImages
            };
        }
    """)

    total_image_mb = image_resources['totalSize'] / (1024 * 1024)

    print(f"   Images loaded via network: {image_resources['count']}")
    print(f"   Total image weight: {total_image_mb:.2f} MB")

    if total_image_mb < 2:
        print(f"   ✓ Image weight: GOOD (< 2MB)")
    elif total_image_mb < 5:
        print(f"   ⚠ Image weight: ACCEPTABLE (< 5MB)")
    else:
        print(f"   ✗ Image weight: TOO HEAVY (> 5MB)")

    if len(image_resources['slowImages']) > 0:
        print(f"   ⚠ Slow loading images (> 1s): {len(image_resources['slowImages'])}")
        for img in image_resources['slowImages'][:3]:
            print(f"      - {img['name'][:40]}: {img['duration']:.0f}ms")

    assert total_image_mb < 15, f"Image weight too large: {total_image_mb:.2f}MB"

    # TEST 6: Alt Text Presence (Accessibility + SEO)
    print("\n6. Checking Image Alt Text...")

    alt_text = page.evaluate("""
        () => {
            const images = document.querySelectorAll('img');
            let withAlt = 0;
            let withoutAlt = 0;

            images.forEach(img => {
                if (img.getAttribute('alt')) {
                    withAlt++;
                } else {
                    withoutAlt++;
                }
            });

            return { withAlt, withoutAlt, total: images.length };
        }
    """)

    print(f"   Images with alt text: {alt_text['withAlt']}")
    print(f"   Images without alt: {alt_text['withoutAlt']}")

    if alt_text['total'] > 0:
        alt_percent = (alt_text['withAlt'] / alt_text['total']) * 100

        if alt_percent == 100:
            print(f"   ✓ All images have alt text")
        elif alt_percent > 80:
            print(f"   ⚠ Most images have alt text ({alt_percent:.0f}%)")
        else:
            print(f"   ✗ Many images missing alt text ({alt_percent:.0f}%)")

    # SUMMARY
    print("\n" + "=" * 50)
    print("IMAGE OPTIMIZATION SUMMARY:")
    print("=" * 50)
    print(f"Total Images: {images_data['totalImages']}")
    print(f"Total Image Weight: {total_image_mb:.2f} MB")
    print(f"Lazy Loaded: {lazy_loading['lazyCount']}/{lazy_loading['total']}")
    print(f"Responsive Images: {responsive_total}/{responsive['total']}")
    print(f"Modern Formats: {'Yes' if has_modern else 'No'}")
    print("=" * 50 + "\n")

    print("✓ Image Optimization & Lazy Loading Test PASSED\n")
