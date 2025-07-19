#!/usr/bin/env python3
"""
Test script to verify advanced Cypress to Playwright conversion patterns
"""

import sys
sys.path.append('/Users/faustosiqueira/playwright-cypress')

from components.interfaces import convert_cypress_code

def test_advanced_conversions():
    """Test advanced conversion patterns"""
    
    # Test cases with various advanced Cypress patterns
    test_cases = [
        {
            "name": "Network Interception",
            "cypress": """cy.intercept('GET', '/api/data', { fixture: 'data.json' }).as('getData');
cy.wait('@getData').its('response.statusCode').should('eq', 200);""",
            "type": "advanced"
        },
        {
            "name": "API Request",
            "cypress": """cy.request('POST', '/api/login', { username, password });""",
            "type": "advanced"
        },
        {
            "name": "Custom Commands",
            "cypress": """Cypress.Commands.add('loginByApi', () => {
    cy.request({ method: 'POST', url: '/api/login' });
});""",
            "type": "advanced"
        },
        {
            "name": "Environment Variables",
            "cypress": """const username = Cypress.env('username');
const password = Cypress.env('password');""",
            "type": "advanced"
        },
        {
            "name": "Local Storage",
            "cypress": """window.localStorage.setItem('authToken', response.body.token);
const token = window.localStorage.getItem('authToken');""",
            "type": "advanced"
        },
        {
            "name": "Aliases and Each",
            "cypress": """cy.get('.dashboard-item').as('items');
cy.get('@items').should('have.length', 3);
cy.get('@items').each(($item, index) => {
    cy.wrap($item).find('h3').should('not.be.empty');
});""",
            "type": "advanced"
        },
        {
            "name": "URL Assertions",
            "cypress": """cy.url().should('include', '/dashboard');
cy.url().should('eq', 'https://example.com/page');
cy.url().should('contain', 'success');""",
            "type": "url_navigation"
        }
    ]
    
    print("🧪 Testing Advanced Cypress to Playwright Conversion Patterns")
    print("=" * 70)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing {test_case['name']}:")
        print("-" * 50)
        print("Input Cypress Code:")
        print(test_case['cypress'])
        print("\nConverted Playwright Code:")
        
        converted_code, explanation = convert_cypress_code(test_case['cypress'], test_case['type'])
        print(converted_code)
        print("\nExplanation:")
        print(explanation)
        print("\n" + "="*70)

if __name__ == "__main__":
    test_advanced_conversions()
