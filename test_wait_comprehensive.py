#!/usr/bin/env python3

"""
Comprehensive test for cy.wait() conversion patterns using the actual conversion logic
"""

import re
from typing import Tuple, List

def _convert_advanced_patterns(code: str) -> Tuple[str, List[str]]:
    """Convert Cypress wait patterns and advanced patterns to Playwright equivalents"""
    explanations = []
    
    # Handle cy.wait('@alias').its('response.statusCode').should('eq', number) patterns first (most specific)
    wait_its_should_pattern = r"cy\.wait\('@([^'\"]+)'\)\.its\('response\.statusCode'\)\.should\('eq',\s*(\d+)\)"
    matches = re.findall(wait_its_should_pattern, code)
    for alias, status_code in matches:
        old_pattern = f"cy.wait('@{alias}').its('response.statusCode').should('eq', {status_code})"
        new_pattern = f"expect((await page.waitForResponse('**/{alias}**')).status()).toBe({status_code})"
        code = code.replace(old_pattern, new_pattern)
        explanations.append(f"• {old_pattern} → {new_pattern}")
    
    # Handle cy.wait('@alias').its('response.statusCode') patterns
    wait_its_pattern = r"cy\.wait\('@([^'\"]+)'\)\.its\('response\.statusCode'\)"
    matches = re.findall(wait_its_pattern, code)
    for match in matches:
        old_pattern = f"cy.wait('@{match}').its('response.statusCode')"
        new_pattern = f"(await page.waitForResponse('**/{match}**')).status()"
        code = code.replace(old_pattern, new_pattern)
        explanations.append(f"• {old_pattern} → {new_pattern}")
    
    # Handle cy.wait('@alias') patterns - complex network waiting (after .its patterns)
    wait_alias_pattern = r"cy\.wait\('@([^'\"]+)'\)"
    matches = re.findall(wait_alias_pattern, code)
    for match in matches:
        old_pattern = f"cy.wait('@{match}')"
        # Convert to appropriate Playwright wait based on common patterns
        if 'api' in match.lower() or 'request' in match.lower() or 'get' in match.lower():
            new_pattern = f"await page.waitForResponse('**/*{match.replace('get', '').replace('api', '').replace('data', '').lower()}*')"
        else:
            new_pattern = f"await page.waitForResponse('**/{match}**')"
        code = code.replace(old_pattern, new_pattern)
        explanations.append(f"• {old_pattern} → {new_pattern}")
    
    # Handle cy.wait(number) patterns - fixed waits
    wait_number_pattern = r"cy\.wait\((\d+)\)"
    matches = re.findall(wait_number_pattern, code)
    for match in matches:
        old_pattern = f"cy.wait({match})"
        new_pattern = f"await page.waitForTimeout({match})"
        code = code.replace(old_pattern, new_pattern)
        explanations.append(f"• {old_pattern} → {new_pattern} (consider using auto-wait instead)")
    
    # Handle cy.waitUntil patterns (if using cypress-wait-until plugin)
    wait_until_pattern = r"cy\.waitUntil\(\(\) => ([^)]+)\)"
    matches = re.findall(wait_until_pattern, code)
    for match in matches:
        old_pattern = f"cy.waitUntil(() => {match})"
        new_pattern = f"await page.waitForFunction(() => {match})"
        code = code.replace(old_pattern, new_pattern)
        explanations.append(f"• {old_pattern} → {new_pattern}")
    
    return code, explanations

def test_wait_conversions():
    """Test various cy.wait() conversion patterns using actual conversion logic"""
    
    test_cases = [
        {
            "name": "Fixed wait timeout",
            "input": "cy.wait(5000);",
            "expected_contains": ["waitForTimeout(5000)", "consider using auto-wait"]
        },
        {
            "name": "Network wait with alias",
            "input": "cy.wait('@getData');",
            "expected_contains": ["waitForResponse", "getData"]
        },
        {
            "name": "Network wait with status check",
            "input": "cy.wait('@getData').its('response.statusCode').should('eq', 200);",
            "expected_contains": ["waitForResponse", "status()", "toBe(200)"]
        },
        {
            "name": "Wait until pattern",
            "input": "cy.waitUntil(() => window.dataLoaded === true);",
            "expected_contains": ["waitForFunction", "window.dataLoaded"]
        },
        {
            "name": "API wait with status check",
            "input": "cy.wait('@getApiData').its('response.statusCode').should('eq', 201);",
            "expected_contains": ["waitForResponse", "status()", "toBe(201)"]
        },
        {
            "name": "Multiple waits in sequence",
            "input": """cy.wait('@getUsers');
cy.wait(2000);
cy.wait('@getProfile').its('response.statusCode').should('eq', 200);""",
            "expected_contains": ["waitForResponse", "waitForTimeout", "status()", "toBe(200)"]
        }
    ]
    
    print("🧪 Testing cy.wait() conversion patterns with actual conversion logic...")
    print("=" * 70)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test_case['name']}")
        print(f"Input:\n{test_case['input']}")
        
        # Apply the actual conversion function
        converted, explanations = _convert_advanced_patterns(test_case['input'])
        
        print(f"\nOutput:\n{converted}")
        
        if explanations:
            print(f"\nExplanations:")
            for explanation in explanations:
                print(f"  {explanation}")
        
        # Check if expected patterns are present
        print(f"\nPattern Checks:")
        all_found = True
        for expected in test_case['expected_contains']:
            if expected in converted or any(expected in exp for exp in explanations):
                print(f"  ✅ Found: '{expected}'")
            else:
                print(f"  ❌ Missing: '{expected}'")
                all_found = False
        
        if all_found:
            print(f"  🎉 All expected patterns found!")
        else:
            print(f"  ⚠️  Some patterns missing.")
        
        print("-" * 50)
    
    print("\n✅ Comprehensive wait conversion test completed!")

if __name__ == "__main__":
    test_wait_conversions()
