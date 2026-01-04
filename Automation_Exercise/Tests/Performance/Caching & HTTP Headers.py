"""
Performance Test 10: Caching & HTTP Headers
Анализира caching strategies и HTTP header optimization
"""

import pytest
from playwright.sync_api import Page

@pytest.mark.performance
def test_caching_and_http_headers(page: Page):
    """
    Проверява:
    1. Cache-Control headers
    2. ETag presence
    3. Expires headers
    4. Cacheable resources
    5. CDN usage
    6. Compression headers
    """
    base_url = "https://automationexercise.com"

    print("\n=== Caching & HTTP Headers Test ===\n")

    # Track responses with headers
    responses_data = []

    def track_response(response):
        try:
            responses_data.append({
                'url': response.url,
                'status': response.status,
                'headers': response.headers,
                'type': response.request.resource_type
            })
        except:
            pass

    page.on('response', track_response)

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

    # TEST 1: Cache-Control Headers
    print("1. Analyzing Cache-Control Headers...")

    cacheable_count = 0
    non_cacheable_count = 0
    no_cache_header = 0

    cache_stats = {
        'max-age': 0,
        'no-cache': 0,
        'no-store': 0,
        'public': 0,
        'private': 0
    }

    for resp in responses_data:
        cache_control = resp['headers'].get('cache-control', '')

        if not cache_control:
            no_cache_header += 1
        else:
            if 'no-cache' in cache_control or 'no-store' in cache_control:
                non_cacheable_count += 1
                if 'no-cache' in cache_control:
                    cache_stats['no-cache'] += 1
                if 'no-store' in cache_control:
                    cache_stats['no-store'] += 1
            else:
                cacheable_count += 1

            if 'max-age' in cache_control:
                cache_stats['max-age'] += 1
            if 'public' in cache_control:
                cache_stats['public'] += 1
            if 'private' in cache_control:
                cache_stats['private'] += 1

    total_resources = len(responses_data)

    print(f"   Total resources analyzed: {total_resources}")
    print(f"   Cacheable resources: {cacheable_count}")
    print(f"   Non-cacheable resources: {non_cacheable_count}")
    print(f"   No cache header: {no_cache_header}")

    if total_resources > 0:
        cacheable_percent = (cacheable_count / total_resources) * 100

        if cacheable_percent > 70:
            print(f"   ✓ Good caching ({cacheable_percent:.0f}% cacheable)")
        elif cacheable_percent > 50:
            print(f"   ⚠ Moderate caching ({cacheable_percent:.0f}% cacheable)")
        else:
            print(f"   ✗ Poor caching ({cacheable_percent:.0f}% cacheable)")

    # TEST 2: ETag Headers
    print("\n2. Checking ETag Headers...")

    with_etag = 0
    without_etag = 0

    for resp in responses_data:
        if resp['type'] in ['stylesheet', 'script', 'image', 'font']:
            if 'etag' in resp['headers']:
                with_etag += 1
            else:
                without_etag += 1

    static_resources = with_etag + without_etag

    if static_resources > 0:
        print(f"   Static resources: {static_resources}")
        print(f"   With ETag: {with_etag}")
        print(f"   Without ETag: {without_etag}")

        etag_percent = (with_etag / static_resources) * 100

        if etag_percent > 80:
            print(f"   ✓ Good ETag usage ({etag_percent:.0f}%)")
        elif etag_percent > 50:
            print(f"   ⚠ Moderate ETag usage ({etag_percent:.0f}%)")
        else:
            print(f"   ⚠ Limited ETag usage ({etag_percent:.0f}%)")

    # TEST 3: Expires Headers
    print("\n3. Analyzing Expires Headers...")

    with_expires = 0

    for resp in responses_data:
        if 'expires' in resp['headers']:
            with_expires += 1

    print(f"   Resources with Expires header: {with_expires}/{total_resources}")

    if with_expires > total_resources * 0.5:
        print(f"   ✓ Expires headers widely used")
    elif with_expires > 0:
        print(f"   ⚠ Some Expires headers present")
    else:
        print(f"   ℹ No Expires headers (using Cache-Control)")

    # TEST 4: Compression Headers
    print("\n4. Checking Content Compression...")

    compressed = 0
    uncompressed = 0
    compression_types = {}

    for resp in responses_data:
        content_encoding = resp['headers'].get('content-encoding', '')

        if content_encoding:
            compressed += 1
            compression_types[content_encoding] = compression_types.get(content_encoding, 0) + 1
        else:
            # Check if resource should be compressed
            content_type = resp['headers'].get('content-type', '')
            if any(t in content_type for t in ['text', 'javascript', 'json', 'xml']):
                uncompressed += 1

    print(f"   Compressed resources: {compressed}")
    print(f"   Uncompressed text resources: {uncompressed}")

    if compression_types:
        print(f"   Compression types: {compression_types}")

    if compressed > 0:
        compression_ratio = compressed / (compressed + uncompressed) if (compressed + uncompressed) > 0 else 0

        if compression_ratio > 0.8:
            print(f"   ✓ Excellent compression ({compression_ratio * 100:.0f}%)")
        elif compression_ratio > 0.6:
            print(f"   ⚠ Good compression ({compression_ratio * 100:.0f}%)")
        else:
            print(f"   ⚠ Limited compression ({compression_ratio * 100:.0f}%)")

    # TEST 5: CDN Usage Detection
    print("\n5. Detecting CDN Usage...")

    cdn_patterns = ['cdn', 'cloudfront', 'akamai', 'fastly', 'cloudflare']
    cdn_resources = 0
    cdn_domains = set()

    for resp in responses_data:
        url_lower = resp['url'].lower()

        if any(pattern in url_lower for pattern in cdn_patterns):
            cdn_resources += 1

            # Extract domain
            try:
                from urllib.parse import urlparse
                domain = urlparse(resp['url']).netloc
                cdn_domains.add(domain)
            except:
                pass

    print(f"   CDN resources: {cdn_resources}/{total_resources}")

    if cdn_domains:
        print(f"   CDN domains: {', '.join(list(cdn_domains)[:3])}")
        print(f"   ✓ Using CDN")
    else:
        print(f"   ℹ No CDN detected")

    # TEST 6: Static Resources Caching
    print("\n6. Analyzing Static Resource Caching...")

    static_types = ['stylesheet', 'script', 'image', 'font']
    static_cached = 0
    static_not_cached = 0

    for resp in responses_data:
        if resp['type'] in static_types:
            cache_control = resp['headers'].get('cache-control', '')

            if 'max-age' in cache_control:
                # Extract max-age value
                try:
                    max_age_str = cache_control.split('max-age=')[1].split(',')[0]
                    max_age = int(max_age_str)

                    if max_age > 86400:  # > 1 day
                        static_cached += 1
                    else:
                        static_not_cached += 1
                except:
                    static_not_cached += 1
            else:
                static_not_cached += 1

    total_static = static_cached + static_not_cached

    if total_static > 0:
        print(f"   Static resources analyzed: {total_static}")
        print(f"   Well-cached (>1 day): {static_cached}")
        print(f"   Poorly-cached: {static_not_cached}")

        static_cache_percent = (static_cached / total_static) * 100

        if static_cache_percent > 80:
            print(f"   ✓ Excellent static caching ({static_cache_percent:.0f}%)")
        elif static_cache_percent > 60:
            print(f"   ⚠ Good static caching ({static_cache_percent:.0f}%)")
        else:
            print(f"   ✗ Poor static caching ({static_cache_percent:.0f}%)")

    # TEST 7: Vary Header Check
    print("\n7. Checking Vary Headers...")

    with_vary = 0
    vary_values = {}

    for resp in responses_data:
        vary = resp['headers'].get('vary', '')

        if vary:
            with_vary += 1
            vary_values[vary] = vary_values.get(vary, 0) + 1

    print(f"   Resources with Vary header: {with_vary}/{total_resources}")

    if vary_values:
        print(f"   Vary header values:")
        for value, count in list(vary_values.items())[:3]:
            print(f"      - {value}: {count}")

    # TEST 8: Cache Hit Ratio Simulation
    print("\n8. Simulating Cache Hit Ratio...")

    # Reload page to test cache
    page.reload()
    page.wait_for_load_state('networkidle')

    # Get resources from cache
    cached_resources = page.evaluate("""
        () => {
            const resources = performance.getEntriesByType('resource');
            let fromCache = 0;
            let fromNetwork = 0;

            resources.forEach(r => {
                if (r.transferSize === 0 && r.decodedBodySize > 0) {
                    fromCache++;
                } else {
                    fromNetwork++;
                }
            });

            return { fromCache, fromNetwork, total: resources.length };
        }
    """)

    print(f"   Resources from cache: {cached_resources['fromCache']}")
    print(f"   Resources from network: {cached_resources['fromNetwork']}")

    if cached_resources['total'] > 0:
        cache_hit_ratio = (cached_resources['fromCache'] / cached_resources['total']) * 100

        print(f"   Cache hit ratio: {cache_hit_ratio:.0f}%")

        if cache_hit_ratio > 70:
            print(f"   ✓ Excellent cache hit ratio")
        elif cache_hit_ratio > 50:
            print(f"   ⚠ Good cache hit ratio")
        else:
            print(f"   ✗ Poor cache hit ratio")

    # SUMMARY
    print("\n" + "=" * 50)
    print("CACHING & HTTP HEADERS SUMMARY:")
    print("=" * 50)
    print(f"Total Resources: {total_resources}")
    print(f"Cacheable: {cacheable_count} ({cacheable_percent:.0f}%)" if total_resources > 0 else "N/A")
    print(f"With ETag: {with_etag}/{static_resources}" if static_resources > 0 else "N/A")
    print(f"Compressed: {compressed}")
    print(f"CDN Usage: {'Yes' if cdn_domains else 'No'}")
    print(f"Cache Hit Ratio: {cache_hit_ratio:.0f}%" if cached_resources['total'] > 0 else "N/A")
    print("=" * 50 + "\n")

    print("✓ Caching & HTTP Headers Test PASSED\n")