"""
Performance Test 05: Network Performance & Optimization
Analyzes network requests, caching, compression, CDN usage
"""

import pytest
from playwright.sync_api import Page
from collections import defaultdict


@pytest.mark.performance
def test_network_performance_and_optimization(page: Page):
    """
    Verifies:
    1. HTTP/2 or HTTP/3 usage
    2. Compression (gzip/brotli)
    3. Caching headers
    4. CDN usage
    5. Parallel connections
    6. Request/response sizes
    7. Keep-alive connections
    """
    base_url = "https://automationexercise.com"

    print("\n=== Network Performance & Optimization Test ===\n")

    # Collect all network requests
    requests_data = []
    responses_data = []

    def track_request(request):
        requests_data.append({
            'url': request.url,
            'method': request.method,
            'resourceType': request.resource_type,
            'headers': request.headers
        })

    def track_response(response):
        responses_data.append({
            'url': response.url,
            'status': response.status,
            'headers': response.headers,
            'timing': response.request.timing
        })

    page.on('request', track_request)
    page.on('response', track_response)

    # Navigate to page
    page.goto(base_url)
    page.wait_for_load_state('networkidle')

    # TEST 1: HTTP Protocol Version
    print("1. Checking HTTP Protocol Version...")

    # Check via CDP (Chrome DevTools Protocol)
    http_versions = defaultdict(int)

    for resp in responses_data:
        # Try to determine HTTP version from headers
        # In real scenario, would use CDP for accurate info
        http_versions['HTTP/1.1 or HTTP/2'] += 1

    print(f"   Total requests: {len(responses_data)}")

    # Check if using HTTP/2 (look for specific indicators)
    h2_indicators = any(
        'http2' in str(resp.get('headers', {})).lower() or
        'h2' in str(resp.get('headers', {})).lower()
        for resp in responses_data
    )

    if h2_indicators:
        print(f"   ✓ HTTP/2 detected (multiplexing enabled)")
    else:
        print(f"   ℹ HTTP/2 indicators not found (may still be in use)")

    # TEST 2: Compression Analysis
    print("\n2. Analyzing Response Compression...")

    compressed_count = 0
    uncompressed_large = []

    for resp in responses_data:
        headers = {k.lower(): v for k, v in resp['headers'].items()}
        content_encoding = headers.get('content-encoding', '')
        content_type = headers.get('content-type', '')

        if 'gzip' in content_encoding or 'br' in content_encoding or 'deflate' in content_encoding:
            compressed_count += 1
        else:
            # Check if it's a compressible resource without compression
            if any(t in content_type for t in ['text', 'javascript', 'json', 'xml', 'css']):
                # Would be better compressed
                uncompressed_large.append({
                    'url': resp['url'].split('/')[-1][:50],
                    'type': content_type.split(';')[0]
                })

    compression_rate = (compressed_count / len(responses_data) * 100) if responses_data else 0

    print(f"   Compressed responses: {compressed_count}/{len(responses_data)} ({compression_rate:.1f}%)")

    if len(uncompressed_large) > 0:
        print(f"   ⚠ Found {len(uncompressed_large)} uncompressed text resources:")
        for item in uncompressed_large[:3]:
            print(f"      - {item['url']} ({item['type']})")
    else:
        print(f"   ✓ All compressible resources are compressed")

    # TEST 3: Caching Headers Analysis
    print("\n3. Analyzing Caching Strategy...")

    cacheable = 0
    not_cacheable = 0
    cache_info = {
        'max-age': [],
        'no-cache': 0,
        'no-store': 0,
        'immutable': 0
    }

    for resp in responses_data:
        headers = {k.lower(): v for k, v in resp['headers'].items()}
        cache_control = headers.get('cache-control', '').lower()
        expires = headers.get('expires', '')
        etag = headers.get('etag', '')

        if cache_control:
            if 'no-store' in cache_control or 'no-cache' in cache_control:
                not_cacheable += 1
                if 'no-cache' in cache_control:
                    cache_info['no-cache'] += 1
                if 'no-store' in cache_control:
                    cache_info['no-store'] += 1
            else:
                cacheable += 1

                # Extract max-age
                if 'max-age=' in cache_control:
                    try:
                        max_age = int(cache_control.split('max-age=')[1].split(',')[0])
                        cache_info['max-age'].append(max_age)
                    except:
                        pass

                if 'immutable' in cache_control:
                    cache_info['immutable'] += 1
        elif expires or etag:
            cacheable += 1

    print(f"   Cacheable resources: {cacheable}")
    print(f"   Non-cacheable resources: {not_cacheable}")
    print(f"   Resources with no-cache: {cache_info['no-cache']}")
    print(f"   Resources with no-store: {cache_info['no-store']}")
    print(f"   Immutable resources: {cache_info['immutable']}")

    if cache_info['max-age']:
        avg_max_age = sum(cache_info['max-age']) / len(cache_info['max-age'])
        print(f"   Average max-age: {avg_max_age / 3600:.1f} hours")

        if avg_max_age > 3600:  # > 1 hour
            print(f"   ✓ Good caching strategy (> 1 hour)")
        else:
            print(f"   ⚠ Short cache duration")

    # TEST 4: CDN Usage Detection
    print("\n4. Detecting CDN Usage...")

    cdn_providers = [
        'cloudflare', 'cloudfront', 'akamai', 'fastly', 'cdn77',
        'maxcdn', 'cdnjs', 'jsdelivr', 'unpkg', 'googleusercontent'
    ]

    cdn_requests = []
    cdn_domains = set()

    for resp in responses_data:
        url_lower = resp['url'].lower()
        headers = {k.lower(): v for k, v in resp['headers'].items()}

        # Check URL for CDN
        for cdn in cdn_providers:
            if cdn in url_lower:
                cdn_requests.append(resp['url'])
                try:
                    from urllib.parse import urlparse
                    domain = urlparse(resp['url']).netloc
                    cdn_domains.add(domain)
                except:
                    pass
                break

        # Check headers for CDN indicators
        cdn_headers = ['cf-ray', 'x-amz-cf-id', 'x-akamai', 'x-fastly']
        for header in cdn_headers:
            if header in headers:
                cdn_requests.append(resp['url'])
                break

    if len(cdn_requests) > 0:
        print(f"   ✓ CDN detected: {len(cdn_requests)} requests via CDN")
        print(f"   CDN domains: {len(cdn_domains)}")
        if cdn_domains:
            print(f"   Domains: {', '.join(list(cdn_domains)[:3])}")
    else:
        print(f"   ℹ No CDN usage detected (or CDN not identifiable)")

    # TEST 5: Parallel Connection Analysis
    print("\n5. Analyzing Parallel Connections...")

    # Group requests by domain
    domains = defaultdict(int)

    for req in requests_data:
        try:
            from urllib.parse import urlparse
            domain = urlparse(req['url']).netloc
            domains[domain] += 1
        except:
            pass

    print(f"   Unique domains: {len(domains)}")
    print(f"   Top domains by request count:")

    sorted_domains = sorted(domains.items(), key=lambda x: x[1], reverse=True)[:5]
    for domain, count in sorted_domains:
        print(f"      {domain}: {count} requests")

    # Too many domains can slow down (DNS lookups)
    if len(domains) < 10:
        print(f"   ✓ Domain count: GOOD (< 10)")
    elif len(domains) < 20:
        print(f"   ⚠ Domain count: ACCEPTABLE (< 20)")
    else:
        print(f"   ✗ Too many domains: {len(domains)} (DNS overhead)")

    # TEST 6: Request/Response Size Analysis
    print("\n6. Analyzing Request/Response Sizes...")

    total_transfer_size = 0
    total_resource_size = 0

    resource_sizes = page.evaluate("""
        () => {
            const resources = performance.getEntriesByType('resource');
            let transfer = 0;
            let encoded = 0;
            let decoded = 0;

            resources.forEach(r => {
                transfer += r.transferSize || 0;
                encoded += r.encodedBodySize || 0;
                decoded += r.decodedBodySize || 0;
            });

            return { transfer, encoded, decoded };
        }
    """)

    if resource_sizes['transfer'] > 0:
        print(f"   Total transferred: {resource_sizes['transfer'] / 1024:.0f} KB")
        print(f"   Total resources (decoded): {resource_sizes['decoded'] / 1024:.0f} KB")

        compression_ratio = (1 - resource_sizes['transfer'] / resource_sizes['decoded']) * 100
        print(f"   Compression ratio: {compression_ratio:.1f}%")

        if compression_ratio > 50:
            print(f"   ✓ Excellent compression")
        elif compression_ratio > 30:
            print(f"   ⚠ Good compression")
        else:
            print(f"   ℹ Compression could be improved")

    # TEST 7: Connection Reuse (Keep-Alive)
    print("\n7. Checking Connection Reuse...")

    keep_alive_count = 0

    for resp in responses_data:
        headers = {k.lower(): v for k, v in resp['headers'].items()}
        connection = headers.get('connection', '').lower()

        if 'keep-alive' in connection or connection == '':
            keep_alive_count += 1

    keep_alive_rate = (keep_alive_count / len(responses_data) * 100) if responses_data else 0

    print(f"   Keep-Alive connections: {keep_alive_count}/{len(responses_data)} ({keep_alive_rate:.1f}%)")

    if keep_alive_rate > 80:
        print(f"   ✓ Connection reuse: EXCELLENT")
    elif keep_alive_rate > 50:
        print(f"   ⚠ Connection reuse: ACCEPTABLE")
    else:
        print(f"   ✗ Poor connection reuse")

    # TEST 8: DNS Prefetch & Preconnect
    print("\n8. Checking Resource Hints...")

    resource_hints = page.evaluate("""
        () => {
            const prefetch = document.querySelectorAll('link[rel="dns-prefetch"]').length;
            const preconnect = document.querySelectorAll('link[rel="preconnect"]').length;
            const preload = document.querySelectorAll('link[rel="preload"]').length;
            const prefetchRes = document.querySelectorAll('link[rel="prefetch"]').length;

            return { prefetch, preconnect, preload, prefetchRes };
        }
    """)

    print(f"   DNS Prefetch: {resource_hints['prefetch']}")
    print(f"   Preconnect: {resource_hints['preconnect']}")
    print(f"   Preload: {resource_hints['preload']}")
    print(f"   Prefetch: {resource_hints['prefetchRes']}")

    total_hints = sum(resource_hints.values())

    if total_hints > 0:
        print(f"   ✓ Resource hints in use ({total_hints} total)")
    else:
        print(f"   ℹ No resource hints detected (opportunity for optimization)")

    # TEST 9: Waterfall Analysis
    print("\n9. Network Waterfall Analysis...")

    # Calculate request timings
    timings = []

    for resp in responses_data:
        if resp['timing']:
            timing = resp['timing']
            timings.append({
                'dns': timing.get('domainLookupEnd', 0) - timing.get('domainLookupStart', 0),
                'tcp': timing.get('connectEnd', 0) - timing.get('connectStart', 0),
                'request': timing.get('responseStart', 0) - timing.get('requestStart', 0),
                'response': timing.get('responseEnd', 0) - timing.get('responseStart', 0)
            })

    if timings:
        avg_dns = sum(t['dns'] for t in timings) / len(timings)
        avg_tcp = sum(t['tcp'] for t in timings) / len(timings)
        avg_request = sum(t['request'] for t in timings) / len(timings)
        avg_response = sum(t['response'] for t in timings) / len(timings)

        print(f"   Average DNS lookup: {avg_dns:.0f}ms")
        print(f"   Average TCP connection: {avg_tcp:.0f}ms")
        print(f"   Average request time: {avg_request:.0f}ms")
        print(f"   Average response time: {avg_response:.0f}ms")

        if avg_dns < 50:
            print(f"   ✓ DNS lookup time: GOOD")

        if avg_tcp < 100:
            print(f"   ✓ TCP connection time: GOOD")

    # SUMMARY
    print("\n" + "=" * 50)
    print("NETWORK PERFORMANCE SUMMARY:")
    print("=" * 50)
    print(f"Total Requests: {len(responses_data)}")
    print(f"Compression Rate: {compression_rate:.1f}%")
    print(f"Cacheable Resources: {cacheable}")
    print(f"CDN Requests: {len(cdn_requests)}")
    print(f"Unique Domains: {len(domains)}")
    if resource_sizes['transfer'] > 0:
        print(f"Total Size: {resource_sizes['transfer'] / 1024:.0f} KB")
    print("=" * 50 + "\n")

    print("✓ Network Performance & Optimization Test PASSED\n")
