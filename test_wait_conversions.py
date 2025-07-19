#!/usr/bin/env python3

"""
Test script for cy.wait() conversion patterns
"""

def test_wait_conversions():
    """Test various cy.wait() conversion patterns"""
    
    test_cases = [
        # Basic fixed wait
        {
            "input": "cy.wait(5000);",
            "expected_contains": ["waitForTimeout(5000)", "consider using auto-wait"]
        },
        
        # Network wait with alias
        {
            "input": "cy.wait('@getData');",
            "expected_contains": ["waitForResponse", "getData"]
        },
        
        # Network wait with status check
        {
            "input": "cy.wait('@getData').its('response.statusCode').should('eq', 200);",
            "expected_contains": ["waitForResponse", "status()", "=== 200"]
        },
        
        # Wait until pattern
        {
            "input": "cy.waitUntil(() => window.dataLoaded === true);",
            "expected_contains": ["waitForFunction", "window.dataLoaded"]
        },
        
        # Complex wait with API
        {
            "input": "cy.wait('@getApiData').its('response.statusCode').should('eq', 200);",
            "expected_contains": ["waitForResponse", "status()", "=== 200"]
        }
    ]
    
    # Import the conversion patterns
    import sys
    sys.path.append('/Users/faustosiqueira/playwright-cypress')
    
    # Since the function is inside the interface, we'll test the patterns manually
    basic_conversions = {
        "cy.wait(": "await page.waitForTimeout(",
        "cy.wait('@": "await page.waitForResponse(",
    }
    
    waiting_conversions = {
        "cy.wait(": "await page.waitForTimeout(",
        "cy.wait('@": "await page.waitForResponse(",
        ".should('be.visible')": "await expect(locator).toBeVisible()",
        ".should('exist')": "await expect(locator).toBeAttached()",
        ".should('not.exist')": "await expect(locator).not.toBeAttached()",
        "cy.get(": "await page.locator(",
        "cy.waitUntil(": "await page.waitForFunction(",
        "cy.wait().then(": "// Use direct async/await instead",
    }
    
    print("🧪 Testing cy.wait() conversion patterns...")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}:")
        print(f"Input: {test_case['input']}")
        
        # Apply basic conversions
        converted = test_case['input']
        for cypress_pattern, playwright_pattern in waiting_conversions.items():
            if cypress_pattern in converted:
                converted = converted.replace(cypress_pattern, playwright_pattern)
                print(f"✅ Applied: {cypress_pattern} → {playwright_pattern}")
        
        print(f"Output: {converted}")
        
        # Check if expected patterns are present
        for expected in test_case['expected_contains']:
            if expected in converted:
                print(f"✅ Contains expected pattern: '{expected}'")
            else:
                print(f"❌ Missing expected pattern: '{expected}'")
    
    print("\n" + "=" * 50)
    print("✅ Test completed! Check conversion patterns above.")

if __name__ == "__main__":
    test_wait_conversions()
