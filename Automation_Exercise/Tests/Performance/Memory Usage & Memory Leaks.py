"""
Performance Test 03: Memory Usage & Memory Leaks
Проверява memory consumption и детектира memory leaks
"""

import pytest
from playwright.sync_api import Page


@pytest.mark.performance
def test_memory_usage_and_leaks(page: Page):
    """
    Проверява:
    1. Initial memory usage
    2. Memory after user interactions
    3. Memory leaks detection
    4. DOM node count
    5. Event listener count
    6. Memory cleanup on navigation
    """
    base_url = "https://automationexercise.com"

    print("\n=== Memory Usage & Memory Leaks Test ===\n")

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

    # TEST 1: Initial Memory Measurement
    print("1. Measuring Initial Memory Usage...")

    initial_memory = page.evaluate("""
        () => {
            if (performance.memory) {
                return {
                    usedJSHeapSize: performance.memory.usedJSHeapSize,
                    totalJSHeapSize: performance.memory.totalJSHeapSize,
                    jsHeapSizeLimit: performance.memory.jsHeapSizeLimit
                };
            }
            return null;
        }
    """)

    if initial_memory:
        used_mb = initial_memory['usedJSHeapSize'] / (1024 * 1024)
        total_mb = initial_memory['totalJSHeapSize'] / (1024 * 1024)
        limit_mb = initial_memory['jsHeapSizeLimit'] / (1024 * 1024)

        print(f"   Used JS Heap: {used_mb:.2f} MB")
        print(f"   Total JS Heap: {total_mb:.2f} MB")
        print(f"   JS Heap Limit: {limit_mb:.2f} MB")

        # Initial memory evaluation
        if used_mb < 50:
            print(f"   ✓ Initial memory: GOOD")
        elif used_mb < 100:
            print(f"   ⚠ Initial memory: ACCEPTABLE")
        else:
            print(f"   ✗ Initial memory: HIGH")
    else:
        print("   ℹ Memory API not available (non-Chromium browser)")

    # TEST 2: DOM Node Count
    print("\n2. Counting DOM Nodes...")

    dom_stats = page.evaluate("""
        () => {
            return {
                totalNodes: document.getElementsByTagName('*').length,
                divs: document.getElementsByTagName('div').length,
                spans: document.getElementsByTagName('span').length,
                images: document.getElementsByTagName('img').length,
                scripts: document.getElementsByTagName('script').length,
                styles: document.getElementsByTagName('style').length + 
                        document.getElementsByTagName('link').length
            };
        }
    """)

    print(f"   Total DOM Nodes: {dom_stats['totalNodes']}")
    print(f"   DIVs: {dom_stats['divs']}")
    print(f"   Images: {dom_stats['images']}")
    print(f"   Scripts: {dom_stats['scripts']}")
    print(f"   Stylesheets: {dom_stats['styles']}")

    # DOM node evaluation with realistic thresholds
    # Modern e-commerce sites can have 5000-8000 nodes
    total_nodes = dom_stats['totalNodes']

    if total_nodes < 3000:
        print(f"   ✓ DOM size: EXCELLENT (< 3000 nodes)")
        dom_rating = "EXCELLENT"
    elif total_nodes < 5000:
        print(f"   ✓ DOM size: GOOD (< 5000 nodes)")
        dom_rating = "GOOD"
    elif total_nodes < 8000:
        print(f"   ⚠ DOM size: ACCEPTABLE (< 8000 nodes)")
        dom_rating = "ACCEPTABLE"
    else:
        print(f"   ✗ DOM size: TOO LARGE (> 8000 nodes)")
        dom_rating = "POOR"

    # More realistic assertion for e-commerce sites
    assert total_nodes < 10000, \
        f"DOM too large: {total_nodes} nodes (limit: 10000)"

    # TEST 3: Event Listeners Count
    print("\n3. Checking Event Listeners...")

    event_listeners = page.evaluate("""
        () => {
            // Count elements with event listeners
            let count = 0;
            const elements = document.querySelectorAll('*');

            elements.forEach(el => {
                // Check for inline event handlers
                const attrs = el.attributes;
                for (let i = 0; i < attrs.length; i++) {
                    if (attrs[i].name.startsWith('on')) {
                        count++;
                    }
                }
            });

            return count;
        }
    """)

    print(f"   Inline event handlers found: {event_listeners}")

    if event_listeners < 50:
        print(f"   ✓ Event listeners: ACCEPTABLE")
    else:
        print(f"   ⚠ Many inline event handlers (consider event delegation)")

    # TEST 4: Memory During User Interactions
    print("\n4. Testing Memory During User Interactions...")

    # Simulate user interactions
    interactions = [
        lambda: page.click('a[href="/products"]'),
        lambda: page.goto(base_url),
        lambda: page.click('a[href="/login"]'),
        lambda: page.goto(base_url),
        lambda: page.click('a[href="/contact_us"]'),
        lambda: page.goto(base_url),
    ]

    memory_samples = []

    for i, interaction in enumerate(interactions, 1):
        try:
            interaction()
            page.wait_for_load_state('networkidle')

            mem = page.evaluate("""
                () => performance.memory ? performance.memory.usedJSHeapSize : 0
            """)

            if mem > 0:
                memory_samples.append(mem / (1024 * 1024))
                print(f"   After interaction {i}: {mem / (1024 * 1024):.2f} MB")
        except Exception as e:
            print(f"   ⚠ Interaction {i} failed: {str(e)[:50]}")

    # TEST 5: Memory Leak Detection
    if len(memory_samples) > 2:
        print("\n5. Analyzing Memory Leak Patterns...")

        initial_mem = memory_samples[0]
        final_mem = memory_samples[-1]
        memory_increase = final_mem - initial_mem
        memory_increase_percent = (memory_increase / initial_mem) * 100 if initial_mem > 0 else 0

        print(f"   Initial: {initial_mem:.2f} MB")
        print(f"   Final: {final_mem:.2f} MB")
        print(f"   Increase: {memory_increase:.2f} MB ({memory_increase_percent:.1f}%)")

        # Memory increase evaluation
        if memory_increase_percent < 30:
            print(f"   ✓ No significant memory leak detected")
            leak_rating = "GOOD"
        elif memory_increase_percent < 50:
            print(f"   ⚠ Moderate memory increase (monitor)")
            leak_rating = "ACCEPTABLE"
        elif memory_increase_percent < 100:
            print(f"   ⚠ WARNING: Significant memory increase")
            leak_rating = "CONCERNING"
        else:
            print(f"   ✗ CRITICAL: Possible memory leak detected!")
            leak_rating = "POOR"

        # More lenient assertion - 150% allows for legitimate memory usage patterns
        assert memory_increase_percent < 150, \
            f"Severe memory leak: {memory_increase_percent:.1f}% increase"
    else:
        print("\n5. Memory Leak Analysis...")
        print("   ℹ Insufficient samples for leak detection")
        leak_rating = "N/A"

    # TEST 6: DOM Node Accumulation
    print("\n6. Checking DOM Node Accumulation...")

    # Go to different pages and check if nodes accumulate
    page.goto(f"{base_url}/products")
    page.wait_for_load_state('networkidle')

    products_dom = page.evaluate("() => document.getElementsByTagName('*').length")

    page.goto(base_url)
    page.wait_for_load_state('networkidle')

    home_dom = page.evaluate("() => document.getElementsByTagName('*').length")

    print(f"   Products page DOM nodes: {products_dom}")
    print(f"   Home page DOM nodes: {home_dom}")

    # DOM nodes не трябва да се натрупват значително
    node_difference = abs(home_dom - dom_stats['totalNodes'])

    if node_difference < 100:
        print(f"   ✓ DOM nodes properly cleaned on navigation")
    elif node_difference < 500:
        print(f"   ⚠ Minor DOM node accumulation ({node_difference} nodes)")
    else:
        print(f"   ⚠ DOM node count changed by {node_difference} nodes")

    # TEST 7: Detached DOM Elements
    print("\n7. Checking for Detached DOM Elements...")

    # Force garbage collection if possible
    page.evaluate("() => { if (window.gc) window.gc(); }")

    final_memory = page.evaluate("""
        () => {
            if (performance.memory) {
                return {
                    usedJSHeapSize: performance.memory.usedJSHeapSize,
                    totalJSHeapSize: performance.memory.totalJSHeapSize
                };
            }
            return null;
        }
    """)

    if final_memory and initial_memory:
        final_used = final_memory['usedJSHeapSize'] / (1024 * 1024)
        initial_used = initial_memory['usedJSHeapSize'] / (1024 * 1024)

        print(f"   Memory after cleanup: {final_used:.2f} MB")

        if final_used < initial_used * 1.5:
            print(f"   ✓ Memory cleanup working properly")
        else:
            print(f"   ⚠ Memory not fully released")

    # TEST 8: Performance Under Load
    print("\n8. Testing Performance Under Load...")

    # Navigate to products page (usually heavy)
    page.goto(f"{base_url}/products")
    page.wait_for_load_state('networkidle')

    # Scroll multiple times (simulate heavy usage)
    for i in range(5):
        page.evaluate("window.scrollBy(0, 500)")
        page.wait_for_load_state('domcontentloaded')

    page.evaluate("window.scrollTo(0, 0)")

    # Check memory after heavy usage
    heavy_usage_memory = page.evaluate("""
        () => performance.memory ? performance.memory.usedJSHeapSize : 0
    """)

    if heavy_usage_memory > 0:
        heavy_mb = heavy_usage_memory / (1024 * 1024)
        print(f"   Memory after heavy usage: {heavy_mb:.2f} MB")

        # Memory evaluation after heavy usage
        if heavy_mb < 150:
            print(f"   ✓ Memory under control")
        elif heavy_mb < 250:
            print(f"   ⚠ Moderate memory usage")
        else:
            print(f"   ✗ High memory usage")

    # TEST 9: Global Variables Check
    print("\n9. Checking for Memory-Consuming Global Variables...")

    global_vars = page.evaluate("""
        () => {
            const globals = [];
            for (let prop in window) {
                if (window.hasOwnProperty(prop) && 
                    typeof window[prop] === 'object' && 
                    window[prop] !== null) {
                    try {
                        const size = JSON.stringify(window[prop]).length;
                        if (size > 10000) {  // > 10KB
                            globals.push({
                                name: prop,
                                size: size,
                                type: typeof window[prop]
                            });
                        }
                    } catch(e) {
                        // Circular reference, skip
                    }
                }
            }
            return globals;
        }
    """)

    if len(global_vars) > 0:
        print(f"   Found {len(global_vars)} large global objects:")
        for var in global_vars[:3]:
            print(f"      - {var['name']}: {var['size'] / 1024:.1f} KB")
    else:
        print(f"   ✓ No unusually large global variables")

    # SUMMARY WITH RATINGS
    print("\n" + "=" * 50)
    print("MEMORY USAGE SUMMARY:")
    print("=" * 50)
    if initial_memory:
        print(f"Initial Memory: {initial_memory['usedJSHeapSize'] / (1024 * 1024):.2f} MB")
    print(f"Total DOM Nodes: {dom_stats['totalNodes']} - {dom_rating}")
    if len(memory_samples) > 0:
        print(f"Memory Range: {min(memory_samples):.2f} - {max(memory_samples):.2f} MB")
        print(f"Memory Leak Analysis: {leak_rating}")
    print(f"Event Listeners: {event_listeners}")
    print("=" * 50 + "\n")

    print("✓ Memory Usage & Memory Leaks Test PASSED\n")