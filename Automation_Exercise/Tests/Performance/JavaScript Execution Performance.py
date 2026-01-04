"""
Performance Test 04: JavaScript Execution Performance
Analyzes JavaScript performance, long tasks and CPU usage
"""

import pytest
from playwright.sync_api import Page


@pytest.mark.performance
def test_javascript_execution_performance(page: Page):
    """
    Verifies:
    1. Total JavaScript execution time
    2. Long tasks (blocking main thread)
    3. Script parse/compile time
    4. Number of JavaScript files
    5. JavaScript errors
    6. Main thread blocking time
    """
    base_url = "https://automationexercise.com"

    print("\n=== JavaScript Execution Performance Test ===\n")

    # Collect JavaScript errors
    js_errors = []
    page.on('pageerror', lambda err: js_errors.append(str(err)))

    # Collect console errors
    console_errors = []
    def handle_console(msg):
        if msg.type == 'error':
            console_errors.append(msg.text)

    page.on('console', handle_console)

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

    # TEST 1: JavaScript Execution Time
    print("1. Measuring JavaScript Execution Time...")

    js_timing = page.evaluate("""
        () => {
            const resources = performance.getEntriesByType('resource');
            const scripts = resources.filter(r => 
                r.initiatorType === 'script' || 
                r.name.endsWith('.js')
            );
            
            let totalDuration = 0;
            let maxDuration = 0;
            let minDuration = Infinity;
            
            scripts.forEach(script => {
                totalDuration += script.duration;
                if (script.duration > maxDuration) maxDuration = script.duration;
                if (script.duration < minDuration) minDuration = script.duration;
            });
            
            return {
                scriptCount: scripts.length,
                totalDuration: totalDuration,
                avgDuration: scripts.length > 0 ? totalDuration / scripts.length : 0,
                maxDuration: maxDuration,
                minDuration: minDuration === Infinity ? 0 : minDuration
            };
        }
    """)

    print(f"   JavaScript files loaded: {js_timing['scriptCount']}")
    print(f"   Total JS load time: {js_timing['totalDuration']:.0f}ms")
    print(f"   Average JS load time: {js_timing['avgDuration']:.0f}ms")
    print(f"   Max JS load time: {js_timing['maxDuration']:.0f}ms")

    # Total JS load time evaluation
    if js_timing['totalDuration'] < 2000:
        print(f"   ✓ JS load time: GOOD")
    elif js_timing['totalDuration'] < 5000:
        print(f"   ⚠ JS load time: ACCEPTABLE")
    else:
        print(f"   ✗ JS load time: SLOW")

    assert js_timing['totalDuration'] < 10000, \
        f"JS load time too slow: {js_timing['totalDuration']}ms"

    # TEST 2: Long Tasks Detection (Main Thread Blocking)
    print("\n2. Detecting Long Tasks (Main Thread Blocking)...")

    page.wait_for_load_state('networkidle')

    long_tasks = page.evaluate("""
        () => {
            return new Promise((resolve) => {
                const tasks = [];
                
                try {
                    const observer = new PerformanceObserver((list) => {
                        for (const entry of list.getEntries()) {
                            if (entry.duration > 50) {  // > 50ms is considered "long"
                                tasks.push({
                                    name: entry.name,
                                    duration: entry.duration,
                                    startTime: entry.startTime
                                });
                            }
                        }
                    });
                    
                    observer.observe({ type: 'longtask', buffered: true });
                    
                    setTimeout(() => {
                        observer.disconnect();
                        resolve(tasks);
                    }, 2000);
                } catch(e) {
                    resolve([]);
                }
            });
        }
    """)

    if len(long_tasks) > 0:
        print(f"   ⚠ Found {len(long_tasks)} long tasks (> 50ms):")

        total_blocking_time = sum(task['duration'] for task in long_tasks)
        print(f"   Total blocking time: {total_blocking_time:.0f}ms")

        sorted_tasks = sorted(long_tasks, key=lambda x: x['duration'], reverse=True)
        for i, task in enumerate(sorted_tasks[:3], 1):
            print(f"      {i}. {task['name']}: {task['duration']:.0f}ms")

        # Google recommendation: < 300ms total blocking time
        if total_blocking_time < 300:
            print(f"   ✓ Total blocking time: ACCEPTABLE")
        else:
            print(f"   ✗ Total blocking time: TOO HIGH")
    else:
        print(f"   ℹ Long Task API not available or no long tasks detected")

    # TEST 3: JavaScript Parse/Compile Time
    print("\n3. Analyzing Script Parse/Compile Time...")

    script_timing = page.evaluate("""
        () => {
            const entries = performance.getEntriesByType('measure');
            const scriptMeasures = entries.filter(e => 
                e.name.includes('script') || 
                e.name.includes('parse') ||
                e.name.includes('compile')
            );
            
            return scriptMeasures.map(m => ({
                name: m.name,
                duration: m.duration
            }));
        }
    """)

    if len(script_timing) > 0:
        total_parse = sum(s['duration'] for s in script_timing)
        print(f"   Script parsing measures found: {len(script_timing)}")
        print(f"   Total parse time: {total_parse:.0f}ms")
    else:
        print(f"   ℹ No explicit parse/compile measures available")

    # TEST 4: JavaScript Bundle Size Analysis
    print("\n4. Analyzing JavaScript Bundle Sizes...")

    js_files = page.evaluate("""
        () => {
            const resources = performance.getEntriesByType('resource');
            const scripts = resources.filter(r => 
                r.initiatorType === 'script' || r.name.endsWith('.js')
            );
            
            return scripts.map(s => ({
                name: s.name.split('/').pop(),
                transferSize: s.transferSize || 0,
                encodedSize: s.encodedBodySize || 0,
                decodedSize: s.decodedBodySize || 0,
                duration: s.duration
            }));
        }
    """)

    if len(js_files) > 0:
        total_js_size = sum(f['decodedSize'] for f in js_files) / 1024
        print(f"   Total JavaScript size: {total_js_size:.0f} KB")

        large_files = sorted(js_files, key=lambda x: x['decodedSize'], reverse=True)[:3]
        print(f"   Largest JavaScript files:")
        for i, file in enumerate(large_files, 1):
            if file['decodedSize'] > 0:
                print(f"      {i}. {file['name'][:40]}: {file['decodedSize']/1024:.0f} KB")

        # Best practice guideline
        if total_js_size < 300:
            print(f"   ✓ JS bundle size: GOOD (< 300KB)")
        elif total_js_size < 500:
            print(f"   ⚠ JS bundle size: ACCEPTABLE (< 500KB)")
        else:
            print(f"   ✗ JS bundle size: TOO LARGE (> 500KB)")

    # TEST 5: JavaScript Errors Check
    print("\n5. Checking JavaScript Errors...")

    page.wait_for_load_state('domcontentloaded')

    total_errors = len(js_errors) + len(console_errors)

    if total_errors > 0:
        print(f"   ⚠ Found {total_errors} JavaScript errors:")

        if js_errors:
            print(f"   Page Errors: {len(js_errors)}")
            for i, err in enumerate(js_errors[:3], 1):
                print(f"      {i}. {err[:80]}")

        if console_errors:
            print(f"   Console Errors: {len(console_errors)}")
            for i, err in enumerate(console_errors[:3], 1):
                print(f"      {i}. {err[:80]}")
    else:
        print(f"   ✓ No JavaScript errors detected")

    # Error evaluation
    if total_errors == 0:
        print(f"   ✓ Error count: EXCELLENT")
    elif total_errors < 5:
        print(f"   ⚠ Error count: ACCEPTABLE")
    elif total_errors < 10:
        print(f"   ⚠ Error count: CONCERNING")
    else:
        print(f"   ✗ Error count: TOO MANY")

    assert total_errors < 20, f"Too many JS errors: {total_errors}"

    # TEST 6: Event Loop Performance
    print("\n6. Testing Event Loop Performance...")

    event_loop_delay = page.evaluate("""
        () => {
            return new Promise((resolve) => {
                let delays = [];
                let count = 0;
                const maxTests = 10;
                
                function testDelay() {
                    const testStart = performance.now();
                    
                    setTimeout(() => {
                        const delay = performance.now() - testStart;
                        delays.push(delay);
                        count++;
                        
                        if (count < maxTests) {
                            testDelay();
                        } else {
                            const avgDelay = delays.reduce((a,b) => a+b, 0) / delays.length;
                            const maxDelay = Math.max(...delays);
                            resolve({ avgDelay, maxDelay, delays: delays.length });
                        }
                    }, 0);
                }
                
                testDelay();
            });
        }
    """)

    print(f"   Average event loop delay: {event_loop_delay['avgDelay']:.1f}ms")
    print(f"   Max event loop delay: {event_loop_delay['maxDelay']:.1f}ms")

    if event_loop_delay['avgDelay'] < 10:
        print(f"   ✓ Event loop: RESPONSIVE")
    elif event_loop_delay['avgDelay'] < 50:
        print(f"   ⚠ Event loop: ACCEPTABLE")
    else:
        print(f"   ✗ Event loop: SLOW")

    # TEST 7: Third-Party Scripts Analysis
    print("\n7. Analyzing Third-Party Scripts...")

    third_party = page.evaluate("""
        () => {
            const resources = performance.getEntriesByType('resource');
            const currentDomain = window.location.hostname;
            
            const thirdParty = resources.filter(r => 
                (r.initiatorType === 'script' || r.name.endsWith('.js')) &&
                !r.name.includes(currentDomain)
            );
            
            return {
                count: thirdParty.length,
                domains: [...new Set(thirdParty.map(r => {
                    try {
                        return new URL(r.name).hostname;
                    } catch {
                        return 'unknown';
                    }
                }))],
                totalDuration: thirdParty.reduce((sum, r) => sum + r.duration, 0)
            };
        }
    """)

    if third_party['count'] > 0:
        print(f"   Third-party scripts: {third_party['count']}")
        print(f"   Third-party domains: {len(third_party['domains'])}")
        print(f"   Total 3rd party load time: {third_party['totalDuration']:.0f}ms")

        if len(third_party['domains']) > 0:
            print(f"   Domains: {', '.join(third_party['domains'][:5])}")

        if third_party['totalDuration'] < 2000:
            print(f"   ✓ Third-party impact: ACCEPTABLE")
        else:
            print(f"   ⚠ Third-party scripts slowing down page")
    else:
        print(f"   ✓ No third-party scripts detected")

    # TEST 8: Animation Frame Performance
    print("\n8. Testing Animation Frame Rate...")

    fps_test = page.evaluate("""
        () => {
            return new Promise((resolve) => {
                const frames = [];
                let lastTime = performance.now();
                let frameCount = 0;
                const maxFrames = 60;
                
                function measureFrame() {
                    const currentTime = performance.now();
                    const delta = currentTime - lastTime;
                    frames.push(delta);
                    lastTime = currentTime;
                    frameCount++;
                    
                    if (frameCount < maxFrames) {
                        requestAnimationFrame(measureFrame);
                    } else {
                        const avgFrameTime = frames.reduce((a,b) => a+b, 0) / frames.length;
                        const fps = 1000 / avgFrameTime;
                        const droppedFrames = frames.filter(f => f > 16.67).length;
                        
                        resolve({ 
                            fps: fps, 
                            avgFrameTime: avgFrameTime,
                            droppedFrames: droppedFrames,
                            totalFrames: frames.length
                        });
                    }
                }
                
                requestAnimationFrame(measureFrame);
            });
        }
    """)

    print(f"   Average FPS: {fps_test['fps']:.1f}")
    print(f"   Average frame time: {fps_test['avgFrameTime']:.1f}ms")
    print(f"   Dropped frames: {fps_test['droppedFrames']}/{fps_test['totalFrames']}")

    if fps_test['fps'] >= 55:
        print(f"   ✓ Frame rate: EXCELLENT")
    elif fps_test['fps'] >= 30:
        print(f"   ⚠ Frame rate: ACCEPTABLE")
    else:
        print(f"   ✗ Frame rate: POOR")

    # SUMMARY
    print("\n" + "="*50)
    print("JAVASCRIPT PERFORMANCE SUMMARY:")
    print("="*50)
    print(f"JS Files: {js_timing['scriptCount']}")
    print(f"Total JS Load Time: {js_timing['totalDuration']:.0f}ms")
    print(f"Long Tasks: {len(long_tasks)}")
    print(f"JS Errors: {total_errors}")
    print(f"Average FPS: {fps_test['fps']:.1f}")
    print("="*50 + "\n")

    print("✓ JavaScript Execution Performance Test PASSED\n")
