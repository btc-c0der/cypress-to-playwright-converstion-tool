import gradio as gr
from typing import Dict, Any, List, Tuple

def create_migration_interface() -> gr.Interface:
    """Create the Cypress to Playwright migration interface"""
    
    def convert_cypress_code(cypress_code: str, conversion_type: str) -> Tuple[str, str]:
        """Convert Cypress code to Playwright"""
        
        # Basic conversion patterns
        conversions = {
            "basic_syntax": {
                "cy.get(": "page.locator(",
                "cy.visit(": "await page.goto(",
                "cy.url()": "page.url()",
                ".type(": ".fill(",
                ".click()": ".click()",
                ".should('be.visible')": "await expect(...).toBeVisible()",
                ".should('contain',": "await expect(...).toContainText(",
                "describe(": "test.describe(",
                "it(": "test(",
                "beforeEach(": "test.beforeEach(async ({ page }) => {",
            },
            "assertions": {
                "cy.url().should('include',": "await expect(page).toHaveURL(/.*",
                "cy.url().should('eq',": "await expect(page).toHaveURL(",
                "cy.url().should('equal',": "await expect(page).toHaveURL(",
                "cy.url().should('contain',": "await expect(page).toHaveURL(/.*",
                "cy.url().should('match',": "await expect(page).toHaveURL(",
                ".should('be.visible')": "await expect(locator).toBeVisible()",
                ".should('not.exist')": "await expect(locator).not.toBeVisible()",
                ".should('contain',": "await expect(locator).toContainText(",
                ".should('have.text',": "await expect(locator).toHaveText(",
                ".should('have.value',": "await expect(locator).toHaveValue(",
                ".should('have.length',": "await expect(locator).toHaveCount(",
                ".should('be.empty')": "await expect(locator).toBeEmpty()",
                ".should('be.enabled')": "await expect(locator).toBeEnabled()",
                ".should('be.disabled')": "await expect(locator).toBeDisabled()",
                ".should('have.class',": "await expect(locator).toHaveClass(",
            },
            "commands": {
                "cy.get(": "page.locator(",
                "cy.visit(": "await page.goto(",
                "cy.url()": "page.url()",
                "cy.intercept(": "await page.route(",
                "cy.fixture(": "// Use test data factory instead",
                "cy.wrap(": "// Use direct variable assignment instead",
                "cy.contains(": "page.getByText(",
                ".each(": ".map(async (element, index) => {",
                ".as('": "// Use variable assignment instead of alias",
                # Note: cy.wait() patterns are handled by _convert_advanced_patterns()
            },
            "waiting": {
                ".should('be.visible')": "await expect(locator).toBeVisible()",
                ".should('exist')": "await expect(locator).toBeAttached()",
                ".should('not.exist')": "await expect(locator).not.toBeAttached()",
                "cy.get(": "await page.locator(",
                "cy.waitUntil(": "await page.waitForFunction(",
                "cy.wait().then(": "// Use direct async/await instead",
                # Note: cy.wait() patterns are handled by _convert_advanced_patterns()
            },
            "advanced": {
                "cy.request(": "await request.newContext().request(",
                "cy.intercept('GET',": "await page.route('GET', ",
                "cy.intercept('POST',": "await page.route('POST', ",
                "cy.intercept('PUT',": "await page.route('PUT', ",
                "cy.intercept('DELETE',": "await page.route('DELETE', ",
                "cy.wait('@": "await page.waitForResponse(",
                "cy.task(": "// Use custom functions or direct Node.js code",
                "Cypress.Commands.add(": "// Convert to Page Object Model method",
                "Cypress.env(": "process.env.",
                "window.localStorage.setItem(": "await page.evaluate(() => localStorage.setItem(",
                "window.localStorage.getItem(": "await page.evaluate(() => localStorage.getItem(",
                ".its('response.statusCode')": "// Use response object directly",
                ".fixture(": "// Use JSON import or test data factory",
            },
            "url_navigation": {
                "cy.visit(": "await page.goto(",
                "cy.url()": "page.url()",
                "cy.go('back')": "await page.goBack()",
                "cy.go('forward')": "await page.goForward()",
                "cy.reload()": "await page.reload()",
                "cy.url().should('include',": "await expect(page).toHaveURL(/.*",
                "cy.url().should('eq',": "await expect(page).toHaveURL(",
                "cy.url().should('equal',": "await expect(page).toHaveURL(",
                "cy.url().should('contain',": "await expect(page).toHaveURL(/.*",
                "cy.url().should('match',": "await expect(page).toHaveURL(",
                "cy.location('search').should('include',": "await expect(page).toHaveURL(/.*",
                "cy.location('pathname').should('include',": "await expect(page).toHaveURL(/.*",
                "cy.location('hash').should('include',": "await expect(page).toHaveURL(/.*",
            },
            "architectural": {
                "cy.window().then(": "await page.evaluate(",
                "cy.window().its(": "await page.evaluate(() => window.",
                "cy.window()": "await page.evaluate(() => window)",
                "Cypress.Commands.add(": "// Convert to Page Object Model method or helper function",
                ".invoke(": "await page.evaluate(",
                ".its(": "// Use page.evaluate() for property access",
                "cy.stub(": "// Use page.route() for network mocking instead",
                "cy.spy(": "// Use page.evaluate() for function monitoring",
                "cy.wrap(": "// Use direct async/await instead of wrapping",
                ".as('": "// Use variable assignment: const alias = ",
                "cy.get('@": "// Use the stored variable directly",
                ".should('have.property',": "// Use page.evaluate() to check properties",
                ".should('have.been.called": "// Use page.route() with callback tracking",
            },
            "fixtures_commands": {
                "cy.fixture(": "// Import JSON directly or use data loading utility",
                "Cypress.Commands.add(": "// Convert to helper function or Page Object method",
                "cy.task(": "// Use direct function calls or utility classes",
                "Cypress.env(": "process.env.",
                ".as('": "// Use variable assignment instead of alias",
                "cy.get('@": "// Use the stored variable directly",
                "beforeEach(": "test.beforeEach(async ({ page }) => {",
                "before(": "test.beforeAll(async ({ browser }) => {",
            }
        }
        
        converted_code = cypress_code
        explanation_parts = []
        
        if conversion_type == "full_conversion":
            # Apply all conversion patterns in the correct order for full conversion
            categories_to_apply = ["basic_syntax", "assertions", "commands", "waiting", "advanced", "url_navigation", "architectural", "fixtures_commands"]
            
            for category in categories_to_apply:
                if category in conversions:
                    for cypress_pattern, playwright_pattern in conversions[category].items():
                        if cypress_pattern in converted_code:
                            converted_code = converted_code.replace(cypress_pattern, playwright_pattern)
                            explanation_parts.append(f"• {cypress_pattern} → {playwright_pattern}")
            
            # Apply advanced patterns for full conversion
            converted_code, url_explanations = _convert_advanced_patterns(converted_code)
            explanation_parts.extend(url_explanations)
            
        elif conversion_type in conversions:
            # Apply specific category conversions
            for cypress_pattern, playwright_pattern in conversions[conversion_type].items():
                if cypress_pattern in converted_code:
                    converted_code = converted_code.replace(cypress_pattern, playwright_pattern)
                    explanation_parts.append(f"• {cypress_pattern} → {playwright_pattern}")
            
            # Always apply advanced patterns for context-specific conversions
            converted_code, url_explanations = _convert_advanced_patterns(converted_code)
            explanation_parts.extend(url_explanations)
        
        # Add async/await if not present
        if "await " not in converted_code and ("page." in converted_code or "expect(" in converted_code):
            converted_code = f"// Add async/await syntax\n{converted_code}"
            explanation_parts.append("• Added async/await syntax requirement")
        
        # Add import statement for full conversion
        if conversion_type == "full_conversion" and ("test(" in converted_code or "expect(" in converted_code):
            if not converted_code.startswith("import"):
                converted_code = "import { test, expect } from '@playwright/test';\n\n" + converted_code
                explanation_parts.append("• Added required Playwright imports")
        
        explanation = "**Conversion Changes:**\n" + "\n".join(explanation_parts) if explanation_parts else "No direct conversions needed."
        
        # Prevent accidental 'test.test.beforeEach' due to repeated replacement
        if "test.test.beforeEach" in converted_code:
            converted_code = converted_code.replace("test.test.beforeEach", "test.beforeEach")
            explanation_parts.append("• Fixed accidental 'test.test.beforeEach' to 'test.beforeEach'")
        return converted_code, explanation
    
    def _convert_advanced_patterns(code: str) -> Tuple[str, List[str]]:
        """Convert Cypress URL assertions, wait patterns, and advanced patterns to Playwright equivalents"""
        import re
        explanations = []
        
        # Handle cy.contains() patterns - multiple variations
        contains_basic_pattern = r"cy\.contains\(['\"]([^'\"]+)['\"]\)"
        matches = re.findall(contains_basic_pattern, code)
        for match in matches:
            old_pattern = f"cy.contains('{match}')"
            new_pattern = f"page.getByText('{match}')"
            code = code.replace(old_pattern, new_pattern)
            explanations.append(f"• {old_pattern} → {new_pattern}")
        
        # Handle cy.contains() with selector patterns
        contains_selector_pattern = r"cy\.contains\(['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]\)"
        matches = re.findall(contains_selector_pattern, code)
        for selector, text in matches:
            old_pattern = f"cy.contains('{selector}', '{text}')"
            new_pattern = f"page.locator('{selector}').getByText('{text}')"
            code = code.replace(old_pattern, new_pattern)
            explanations.append(f"• {old_pattern} → {new_pattern}")
        
        # Handle unidentified cy.* commands (potential custom commands)
        # This should run after all known patterns have been processed
        unidentified_cy_pattern = r"(cy\.[a-zA-Z][a-zA-Z0-9]*\([^)]*\))"
        
        # Find all cy.* patterns that haven't been converted yet
        remaining_cy_commands = re.findall(unidentified_cy_pattern, code)
        
        # Filter out known patterns that we intentionally handle elsewhere
        known_patterns = [
            'cy.get(', 'cy.visit(', 'cy.url(', 'cy.wait(', 'cy.intercept(', 
            'cy.contains(', 'cy.fixture(', 'cy.wrap(', 'cy.window(', 'cy.location(',
            'cy.go(', 'cy.reload(', 'cy.request(', 'cy.task(', 'cy.stub(',
            'cy.spy(', 'cy.waitUntil('
        ]
        
        for cy_command in remaining_cy_commands:
            # Check if this is truly unidentified (not in our known patterns)
            is_unidentified = True
            for known in known_patterns:
                if cy_command.startswith(known):
                    is_unidentified = False
                    break
            
            if is_unidentified and cy_command in code:
                # Add TODO comment for manual review
                new_pattern = f"// TODO: Manual review needed - possible custom command: {cy_command}"
                code = code.replace(cy_command, new_pattern)
                explanations.append(f"• {cy_command} → {new_pattern}")
        
        # Handle cy.location('search').should('include', 'param') patterns
        location_search_pattern = r"cy\.location\('search'\)\.should\('include',\s*['\"]([^'\"]+)['\"]\)"
        matches = re.findall(location_search_pattern, code)
        for match in matches:
            old_pattern = f"cy.location('search').should('include', '{match}')"
            new_pattern = f"await expect(page).toHaveURL(/.*\\?.*{re.escape(match)}.*/)"
            code = code.replace(old_pattern, new_pattern)
            explanations.append(f"• {old_pattern} → {new_pattern}")
        
        # Handle cy.location('pathname').should('include', 'path') patterns
        location_pathname_pattern = r"cy\.location\('pathname'\)\.should\('include',\s*['\"]([^'\"]+)['\"]\)"
        matches = re.findall(location_pathname_pattern, code)
        for match in matches:
            old_pattern = f"cy.location('pathname').should('include', '{match}')"
            new_pattern = f"await expect(page).toHaveURL(/.*{re.escape(match)}.*/)"
            code = code.replace(old_pattern, new_pattern)
            explanations.append(f"• {old_pattern} → {new_pattern}")
        
        # Handle cy.location('hash').should('include', 'hash') patterns
        location_hash_pattern = r"cy\.location\('hash'\)\.should\('include',\s*['\"]([^'\"]+)['\"]\)"
        matches = re.findall(location_hash_pattern, code)
        for match in matches:
            old_pattern = f"cy.location('hash').should('include', '{match}')"
            new_pattern = f"await expect(page).toHaveURL(/.*#{re.escape(match)}.*/)"
            code = code.replace(old_pattern, new_pattern)
            explanations.append(f"• {old_pattern} → {new_pattern}")
        
        # Handle cy.url().should('include', 'text') patterns
        include_pattern = r"cy\.url\(\)\.should\('include',\s*['\"]([^'\"]+)['\"]\)"
        matches = re.findall(include_pattern, code)
        for match in matches:
            old_pattern = f"cy.url().should('include', '{match}')"
            new_pattern = f"await expect(page).toHaveURL(/.*{re.escape(match)}.*/)"
            code = code.replace(old_pattern, new_pattern)
            explanations.append(f"• {old_pattern} → {new_pattern}")
        
        # Handle cy.url().should('eq', 'exact-url') patterns  
        eq_pattern = r"cy\.url\(\)\.should\('eq',\s*['\"]([^'\"]+)['\"]\)"
        matches = re.findall(eq_pattern, code)
        for match in matches:
            old_pattern = f"cy.url().should('eq', '{match}')"
            new_pattern = f"await expect(page).toHaveURL('{match}')"
            code = code.replace(old_pattern, new_pattern)
            explanations.append(f"• {old_pattern} → {new_pattern}")
            
        # Handle cy.url().should('contain', 'text') patterns
        contain_pattern = r"cy\.url\(\)\.should\('contain',\s*['\"]([^'\"]+)['\"]\)"
        matches = re.findall(contain_pattern, code)
        for match in matches:
            old_pattern = f"cy.url().should('contain', '{match}')"
            new_pattern = f"await expect(page).toHaveURL(/.*{re.escape(match)}.*/)"
            code = code.replace(old_pattern, new_pattern)
            explanations.append(f"• {old_pattern} → {new_pattern}")
        
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
        
        # Handle remaining .its('response.statusCode') patterns that might be left
        its_response_pattern = r"\.its\('response\.statusCode'\)"
        if re.search(its_response_pattern, code):
            code = re.sub(its_response_pattern, ".status()", code)
            explanations.append("• .its('response.statusCode') → .status()")
        
        # Handle .should('eq', 200) after status() calls
        status_should_pattern = r"\.status\(\)\.should\('eq',\s*(\d+)\)"
        matches = re.findall(status_should_pattern, code)
        for match in matches:
            old_pattern = f".status().should('eq', {match})"
            new_pattern = f".status()).toBe({match})"
            code = code.replace(old_pattern, new_pattern)
            explanations.append(f"• {old_pattern} → expect(...{new_pattern}")
        
        # Handle remaining .should('eq', number) patterns
        should_eq_pattern = r"\.should\('eq',\s*(\d+)\)"
        matches = re.findall(should_eq_pattern, code)
        for match in matches:
            old_pattern = f".should('eq', {match})"
            new_pattern = f" === {match}"
            code = code.replace(old_pattern, new_pattern)
            explanations.append(f"• {old_pattern} → {new_pattern} (direct comparison)")
        
        # Handle cy.waitUntil patterns (if using cypress-wait-until plugin)
        wait_until_pattern = r"cy\.waitUntil\(\(\) => ([^)]+)\)"
        matches = re.findall(wait_until_pattern, code)
        for match in matches:
            old_pattern = f"cy.waitUntil(() => {match})"
            new_pattern = f"await page.waitForFunction(() => {match})"
            code = code.replace(old_pattern, new_pattern)
            explanations.append(f"• {old_pattern} → {new_pattern}")
        
        # Handle .as('alias') patterns
        alias_pattern = r"\.as\(['\"]([^'\"]+)['\"]\)"
        matches = re.findall(alias_pattern, code)
        for match in matches:
            old_pattern = f".as('{match}')"
            new_pattern = f"// Store in variable: const {match} = "
            code = code.replace(old_pattern, new_pattern)
            explanations.append(f"• Alias .as('{match}') → Use variable assignment")
        
        # Handle cy.get('@alias') patterns
        get_alias_pattern = r"cy\.get\('@([^'\"]+)'\)"
        matches = re.findall(get_alias_pattern, code)
        for match in matches:
            old_pattern = f"cy.get('@{match}')"
            new_pattern = f"{match}"
            code = code.replace(old_pattern, new_pattern)
            explanations.append(f"• {old_pattern} → Use variable {match}")
        
        # Handle .each() patterns
        each_pattern = r"\.each\(\(\$([^,]+),\s*([^)]+)\)\s*=>\s*\{"
        if re.search(each_pattern, code):
            explanations.append("• .each() → Use for loop with locator.count() and locator.nth()")
        
        # Handle cy.wrap() patterns
        wrap_pattern = r"cy\.wrap\(\$([^)]+)\)"
        matches = re.findall(wrap_pattern, code)
        for match in matches:
            old_pattern = f"cy.wrap(${match})"
            new_pattern = f"// Use direct locator methods on {match}"
            code = code.replace(old_pattern, new_pattern)
            explanations.append(f"• cy.wrap(${match}) → Use direct locator operations")
        
        return code, explanations
    
    def get_migration_tips(topic: str) -> str:
        """Get migration tips for specific topics"""
        tips = {
            "full_conversion": """
**Complete Cypress to Playwright Conversion:**

🎯 **What it does**: Applies ALL conversion patterns simultaneously for comprehensive transformation

**🔄 Conversion Categories Applied:**
1. **Basic Syntax**: Core commands (cy.get → page.locator, cy.visit → page.goto)
2. **Assertions**: Should statements → expect() assertions
3. **Commands**: Advanced commands (cy.intercept, cy.fixture, etc.)
4. **Waiting**: All cy.wait() patterns → Playwright wait strategies
5. **Advanced**: Network interception, custom commands, aliases
6. **URL Navigation**: URL assertions and navigation commands

**📋 Features:**
- ✅ **Auto-imports**: Adds necessary Playwright imports
- ✅ **Async/await**: Converts to proper async syntax
- ✅ **Smart patterns**: Context-aware conversions
- ✅ **Best practices**: Follows Playwright conventions

**💡 Best for:**
- Complete test file migrations
- Learning comprehensive conversion patterns
- Production-ready code transformation

**⚠️ Note**: Review output carefully for complex scenarios
            """,
            "selectors": """
**Selector Migration Tips:**

1. **Priority Order:**
   - Use `page.getByRole()` for accessibility
   - Use `page.getByTestId()` for test-specific elements
   - Use `page.getByText()` for unique text content
   - Avoid CSS selectors when possible

2. **Examples:**
   ```javascript
   // Cypress → Playwright
   cy.get('[data-cy="submit"]') → page.getByTestId('submit')
   cy.get('button').contains('Submit') → page.getByRole('button', { name: 'Submit' })
   cy.get('.error-message') → page.locator('.error-message')
   ```

3. **Best Practices:**
   - Use semantic selectors
   - Avoid brittle CSS selectors
   - Test selectors for stability
            """,
            "url_navigation": """
**URL and Navigation Migration:**

1. **URL Assertions:**
   ```javascript
   // Cypress → Playwright
   cy.url().should('include', '/dashboard') → await expect(page).toHaveURL(/.*dashboard.*/)
   cy.url().should('eq', 'https://example.com/page') → await expect(page).toHaveURL('https://example.com/page')
   cy.url().should('contain', 'success') → await expect(page).toHaveURL(/.*success.*/)
   ```

2. **Navigation:**
   ```javascript
   // Cypress → Playwright
   cy.visit('/login') → await page.goto('/login')
   cy.go('back') → await page.goBack()
   cy.go('forward') → await page.goForward()
   cy.reload() → await page.reload()
   ```

3. **URL Retrieval:**
   ```javascript
   // Cypress → Playwright
   cy.url().then(url => console.log(url)) → console.log(page.url())
   ```

4. **Best Practices:**
   - Use regex patterns for partial URL matches
   - Prefer toHaveURL() over manual URL comparisons
   - Consider baseURL configuration for relative paths
            """,
            "waiting": """
**Waiting Strategies Migration:**

1. **Network Waiting:**
   ```javascript
   // Cypress → Playwright
   cy.wait('@apiCall') → await page.waitForResponse('**/api/**')
   cy.wait('@getData').its('response.statusCode').should('eq', 200) → 
     expect((await page.waitForResponse('**/data**')).status()).toBe(200)
   ```

2. **Fixed Timeouts (Discouraged):**
   ```javascript
   // Cypress → Playwright
   cy.wait(5000) → await page.waitForTimeout(5000)
   // Better: Use auto-wait with expect() assertions
   ```

3. **Element State Waiting:**
   ```javascript
   // Cypress → Playwright
   cy.get('.button').should('be.visible') → await expect(page.locator('.button')).toBeVisible()
   cy.get('.loading').should('not.exist') → await expect(page.locator('.loading')).not.toBeVisible()
   ```

4. **Custom Conditions:**
   ```javascript
   // Cypress → Playwright
   cy.waitUntil(() => window.dataLoaded) → await page.waitForFunction(() => window.dataLoaded)
   ```

5. **Best Practices:**
   - Trust Playwright's auto-waiting mechanism
   - Use expect() assertions instead of manual waits
   - Replace cy.wait('@alias') with waitForResponse()
   - Avoid fixed timeouts unless absolutely necessary
            """,
            "assertions": """
**Assertion Migration:**

1. **Syntax Changes:**
   ```javascript
   // Cypress → Playwright
   .should('be.visible') → await expect(locator).toBeVisible()
   .should('contain', 'text') → await expect(locator).toContainText('text')
   .should('have.text', 'exact') → await expect(locator).toHaveText('exact')
   .should('have.length', 3) → await expect(locator).toHaveCount(3)
   ```

2. **Async Nature:**
   - All Playwright assertions are async
   - Use await with expect()
   - Built-in auto-waiting

3. **Negation:**
   ```javascript
   .should('not.exist') → await expect(locator).not.toBeVisible()
   ```
            """,
            "commands": """
**Command Migration:**

1. **Basic Commands:**
   ```javascript
   // Cypress → Playwright
   cy.get('.selector') → page.locator('.selector')
   cy.visit('/path') → await page.goto('/path')
   cy.contains('text') → page.getByText('text')
   cy.contains('button', 'Submit') → page.locator('button').getByText('Submit')
   ```

2. **Text and Content:**
   ```javascript
   // Cypress → Playwright
   cy.contains('Welcome') → page.getByText('Welcome')
   cy.contains('exact text') → page.getByText('exact text', { exact: true })
   cy.get('button').contains('Click') → page.getByRole('button', { name: 'Click' })
   ```

3. **Navigation:**
   ```javascript
   // Cypress → Playwright
   cy.visit('/login') → await page.goto('/login')
   cy.go('back') → await page.goBack()
   cy.go('forward') → await page.goForward()
   cy.reload() → await page.reload()
   ```

4. **Network and Data:**
   ```javascript
   // Cypress → Playwright
   cy.intercept('GET', '/api/data') → await page.route('/api/data', ...)
   cy.fixture('users.json') → // Use JSON import or test data factory
   cy.request('POST', '/api/login') → await request.post('/api/login', ...)
   ```

5. **Custom Commands:**
   - Convert to Page Object Model methods
   - Use helper functions instead of chained commands
   - Unidentified cy.* commands get TODO comments for manual review

6. **Best Practices:**
   - Use semantic selectors (getByRole, getByText)
   - Avoid CSS selectors when possible
   - Convert custom commands to reusable functions
            """,
            "advanced": """
**Advanced Features Migration:**

1. **Network Interception:**
   ```javascript
   // Cypress → Playwright
   cy.intercept('GET', '/api/data', { fixture: 'data.json' }).as('getData');
   cy.wait('@getData');
   
   // Becomes:
   await page.route('/api/data', route => {
       route.fulfill({ path: 'fixtures/data.json' });
   });
   const response = await page.waitForResponse('/api/data');
   ```

2. **HTTP Requests:**
   ```javascript
   // Cypress → Playwright
   cy.request('POST', '/api/login', { username, password });
   
   // Becomes:
   const response = await request.post('/api/login', {
       data: { username, password }
   });
   ```

3. **Custom Commands → Page Objects:**
   ```javascript
   // Cypress Custom Command
   Cypress.Commands.add('loginByApi', () => { ... });
   
   // Playwright Page Object Method
   class AuthHelper {
       async loginByApi(username, password) { ... }
   }
   ```

4. **Aliases → Variables:**
   ```javascript
   // Cypress → Playwright
   cy.get('.item').as('items');
   cy.get('@items').should('have.length', 3);
   
   // Becomes:
   const items = page.locator('.item');
   await expect(items).toHaveCount(3);
   ```

5. **Environment Variables:**
   ```javascript
   // Cypress → Playwright
   Cypress.env('username') → process.env.USERNAME
   ```

6. **Local Storage:**
   ```javascript
   // Cypress → Playwright
   window.localStorage.setItem('token', value);
   
   // Becomes:
   await page.evaluate((value) => {
       localStorage.setItem('token', value);
   }, value);
   ```
            """,
            "configuration": """
**Configuration Migration:**

1. **File Structure:**
   - `cypress.config.js` → `playwright.config.js`
   - Different configuration options
   - Built-in multi-browser support

2. **Key Differences:**
   ```javascript
   // Cypress
   baseUrl: 'http://localhost:3000'
   
   // Playwright
   use: { baseURL: 'http://localhost:3000' }
   ```

3. **Projects Setup:**
   - Configure multiple browsers
   - Environment-specific configs
   - Parallel execution settings
            """,
            "architectural": """
**Architectural Differences - The Most Challenging Conversions:**

🚨 **Critical Challenge**: Converting from Cypress's implicit command queue to Playwright's explicit async/await

## 1. Asynchronicity: Command Queue vs async/await

**The Biggest Hurdle**: Cypress appears synchronous but uses an implicit command queue. Playwright requires explicit async/await for every browser interaction.

```javascript
// Cypress (looks synchronous, but isn't)
cy.get('#username').type('user');
cy.get('#password').type('pass');
cy.get('#submit').click();
cy.url().should('include', '/dashboard');

// Playwright (explicitly asynchronous)
await page.locator('#username').fill('user');
await page.locator('#password').fill('pass');
await page.locator('#submit').click();
await expect(page).toHaveURL(/.*dashboard/);
```

## 2. Custom Commands vs Helper Functions

**Challenge**: Cypress's fluent DSL with custom commands cannot be replicated directly.

```javascript
// Cypress (fluent chaining)
Cypress.Commands.add('login', (user, pass) => {
    cy.get('#username').type(user);
    cy.get('#password').type(pass);
    cy.get('#submit').click();
});
cy.login('testuser', 'secret').url().should('include', '/dashboard');

// Playwright (helper functions/Page Objects)
async function login(page, user, password) {
    await page.locator('#username').fill(user);
    await page.locator('#password').fill(password);
    await page.locator('#submit').click();
}
await login(page, 'testuser', 'secret');
await expect(page).toHaveURL(/.*dashboard/);
```

## 3. Direct Application Access vs Evaluation

**Challenge**: Cypress runs inside the browser, Playwright operates out-of-process.

```javascript
// Cypress (direct access)
cy.window().then((win) => {
    win.myApp.resetState();
});
cy.window().then((win) => cy.stub(win.myApp, 'calculateTotal').returns(0));

// Playwright (indirect via evaluation)
await page.evaluate(() => window.myApp.resetState());
await page.evaluate(() => { window.myApp.calculateTotal = () => 0; });
```

## 4. Architectural Migration Strategy

**Key Principles:**
- 🔄 **Rewrite, don't translate**: Line-by-line conversion won't work
- 🏗️ **Use Page Object Model**: Replace custom commands with structured classes
- 🎯 **Focus on user behavior**: Move away from internal state manipulation
- 🌐 **Mock at network level**: Replace direct function stubbing with route interception
- ⏱️ **Trust auto-waiting**: Replace manual waits with Playwright's built-in waiting

## 5. Common Refactoring Patterns

```javascript
// Alias pattern conversion
// Cypress
cy.get('.items').as('itemList');
cy.get('@itemList').should('have.length', 3);

// Playwright
const itemList = page.locator('.items');
await expect(itemList).toHaveCount(3);

// Window property access
// Cypress
cy.window().its('dataLayer').should('exist');

// Playwright
const dataLayer = await page.evaluate(() => window.dataLayer);
expect(dataLayer).toBeDefined();
```

**💡 Success Strategy**: Plan for complete test restructuring, not just syntax replacement.
            """,
            "fixtures_commands": """
**Fixtures and Custom Commands Migration - The Complete Guide:**

## 🗂️ Cypress Fixtures vs Playwright Data Management

### 1. Static Data Loading (JSON files)

**Cypress Approach:**
```javascript
// cypress/fixtures/users.json
{
  "admin": { "username": "adminUser", "password": "adminPassword" },
  "standard": { "username": "standardUser", "password": "standardPassword" }
}

// Test usage
cy.fixture('users.json').then((users) => {
  cy.get('#username').type(users.admin.username);
  cy.get('#password').type(users.admin.password);
});
```

**Playwright Approach - Option 1 (Direct Import):**
```javascript
// tests/data/users.json (same structure)
import * as usersData from './data/users.json';

test('login test', async ({ page }) => {
  await page.fill('#username', usersData.admin.username);
  await page.fill('#password', usersData.admin.password);
});
```

**Playwright Approach - Option 2 (Utility Function):**
```javascript
// tests/utils/data-loader.ts
export function loadFixture<T>(fixtureName: string): T {
  const filePath = path.join(__dirname, '..', 'data', `${fixtureName}.json`);
  return JSON.parse(fs.readFileSync(filePath, 'utf-8')) as T;
}

// Test usage
const users = loadFixture<UserData>('users');
await page.fill('#username', users.admin.username);
```

### 2. Environment Setup with Custom Fixtures

**Playwright's Advanced Fixture System:**
```javascript
// tests/fixtures/auth-fixtures.ts
export const test = base.extend<{ loggedInPage: Page }>({
  loggedInPage: async ({ page }, use) => {
    // Setup: Perform login
    await page.goto('/login');
    await page.fill('#username', 'testuser');
    await page.fill('#password', 'testpassword');
    await page.click('#loginButton');
    await page.waitForURL('/dashboard');

    await use(page); // Use logged-in page in test

    // Teardown: Optional cleanup
    // await page.click('#logoutButton');
  },
});

// Test usage
test('dashboard test', async ({ loggedInPage }) => {
  // loggedInPage is already authenticated
  await expect(loggedInPage.locator('.welcome')).toBeVisible();
});
```

## 🛠️ Custom Commands Migration Strategies

### 1. Helper Functions (Recommended)

**Cypress Custom Command:**
```javascript
// cypress/support/commands.js
Cypress.Commands.add('login', (username, password) => {
  cy.visit('/login');
  cy.get('#username').type(username);
  cy.get('#password').type(password);
  cy.get('#loginButton').click();
  cy.url().should('include', '/dashboard');
});

// Usage: cy.login('user', 'pass');
```

**Playwright Helper Function:**
```javascript
// tests/utils/auth.ts
export async function login(page: Page, username: string, password: string) {
  await page.goto('/login');
  await page.fill('#username', username);
  await page.fill('#password', password);
  await page.click('#loginButton');
  await page.waitForURL('/dashboard');
}

// Usage: await login(page, 'user', 'pass');
```

### 2. Page Object Model (POM)

**Structured Approach:**
```javascript
// tests/pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}

  async navigate() {
    await this.page.goto('/login');
  }

  async fillCredentials(username: string, password: string) {
    await this.page.fill('#username', username);
    await this.page.fill('#password', password);
  }

  async submit() {
    await this.page.click('#loginButton');
  }

  async login(username: string, password: string) {
    await this.navigate();
    await this.fillCredentials(username, password);
    await this.submit();
    await this.page.waitForURL('/dashboard');
  }
}

// Usage
const loginPage = new LoginPage(page);
await loginPage.login('user', 'pass');
```

### 3. Combined POM + Fixtures

**Ultimate Reusability:**
```javascript
// tests/fixtures/page-fixtures.ts
export const test = base.extend<{
  loginPage: LoginPage;
  dashboardPage: DashboardPage;
}>({
  loginPage: async ({ page }, use) => {
    await use(new LoginPage(page));
  },
  dashboardPage: async ({ page }, use) => {
    await use(new DashboardPage(page));
  },
});

// Clean test syntax
test('user workflow', async ({ loginPage, dashboardPage }) => {
  await loginPage.login('user', 'pass');
  await dashboardPage.createPost();
});
```

## 🔄 Migration Strategy

### Key Conversion Patterns:
- **`cy.fixture()` → Direct imports or utility functions**
- **`Cypress.Commands.add()` → Helper functions or POM methods**
- **`cy.task()` → Direct function calls or utility classes**
- **`Cypress.env()` → `process.env.VARIABLE_NAME`**
- **Aliases (`.as()`) → Variable assignments**
- **`beforeEach()` → `test.beforeEach(async ({ page }) => {})`**

### Best Practices:
1. **Start with helper functions** for simple reusable actions
2. **Use Page Objects** for complex page interactions
3. **Leverage fixtures** for test environment setup
4. **Import data directly** for static test data
5. **Use TypeScript** for better code organization and type safety

**💡 Pro Tip**: Playwright's approach is more aligned with standard JavaScript patterns, making your test code more maintainable and familiar to developers.
            """
        }
        
        return tips.get(topic, "Select a topic to see migration tips.")
    
    with gr.Blocks(title="Cypress to Playwright Migration") as interface:
        gr.Markdown("## 🔄 Cypress to Playwright Migration Tool")
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("### Input Cypress Code")
                cypress_input = gr.Code(
                    language="javascript",
                    label="Cypress Code"
                )
                
                conversion_type = gr.Dropdown(
                    choices=["full_conversion", "basic_syntax", "assertions", "commands", "waiting", "advanced", "url_navigation", "architectural", "fixtures_commands"],
                    value="full_conversion",
                    label="Conversion Type"
                )
                
                convert_btn = gr.Button("Convert to Playwright", variant="primary")
            
            with gr.Column():
                gr.Markdown("### Playwright Output")
                playwright_output = gr.Code(
                    language="javascript",
                    label="Converted Playwright Code"
                )
                
                explanation_output = gr.Markdown(label="Conversion Explanation")
        
        gr.Markdown("---")
        
        with gr.Row():
            migration_topic = gr.Dropdown(
                choices=["full_conversion", "selectors", "waiting", "url_navigation", "assertions", "commands", "advanced", "configuration", "architectural", "fixtures_commands"],
                value="full_conversion",
                label="Migration Topic"
            )
            
            tips_output = gr.Markdown(value=get_migration_tips("full_conversion"))
        
        # Event handlers
        convert_btn.click(
            fn=convert_cypress_code,
            inputs=[cypress_input, conversion_type],
            outputs=[playwright_output, explanation_output]
        )
        
        migration_topic.change(
            fn=get_migration_tips,
            inputs=[migration_topic],
            outputs=[tips_output]
        )
    
    return interface

def create_best_practices_interface() -> gr.Interface:
    """Create the Playwright best practices interface"""
    
    def get_best_practice_content(category: str, topic: str) -> str:
        """Get best practice content based on category and topic"""
        
        content = {
            "page_objects": {
                "basic": """
## Page Object Model - Basic Implementation

```javascript
class LoginPage {
    constructor(page) {
        this.page = page;
        this.emailInput = page.getByTestId('email');
        this.passwordInput = page.getByTestId('password');
        this.loginButton = page.getByRole('button', { name: 'Login' });
        this.errorMessage = page.locator('.error-message');
    }

    async login(email, password) {
        await this.emailInput.fill(email);
        await this.passwordInput.fill(password);
        await this.loginButton.click();
    }

    async getErrorMessage() {
        return await this.errorMessage.textContent();
    }
}
```

**Benefits:**
- Encapsulation of page elements
- Reusable page interactions
- Easier maintenance
- Clear test intentions
                """,
                "advanced": """
## Advanced Page Object Patterns

```javascript
class BasePage {
    constructor(page) {
        this.page = page;
    }

    async waitForLoad() {
        await this.page.waitForLoadState('networkidle');
    }

    async screenshot(name) {
        await this.page.screenshot({ path: `screenshots/${name}.png` });
    }
}

class ProductPage extends BasePage {
    constructor(page) {
        super(page);
        this.addToCartBtn = page.getByTestId('add-to-cart');
        this.quantityInput = page.getByTestId('quantity');
    }

    async addToCart(quantity = 1) {
        await this.quantityInput.fill(quantity.toString());
        await this.addToCartBtn.click();
        await this.waitForCartUpdate();
    }

    async waitForCartUpdate() {
        await expect(this.page.locator('.cart-notification')).toBeVisible();
    }
}
```
                """
            },
            "selectors": {
                "priority": """
## Selector Priority Order

1. **`getByRole()`** - Most accessible and resilient
2. **`getByTestId()`** - Explicit test identifiers  
3. **`getByLabel()`** - Form elements with labels
4. **`getByText()`** - Unique text content
5. **CSS selectors** - Last resort

```javascript
// Best practices
await page.getByRole('button', { name: 'Submit' });
await page.getByTestId('user-profile');
await page.getByLabel('Email address');
await page.getByText('Welcome back!');

// Avoid when possible
await page.locator('.btn.btn-primary.submit-btn');
```
                """,
                "techniques": """
## Advanced Selector Techniques

```javascript
// Filtering and chaining
await page.getByRole('listitem').filter({ hasText: 'Product 1' });

// Within another element
await page.locator('.sidebar').getByRole('link', { name: 'Settings' });

// Multiple selectors
await page.locator('button, input[type="submit"]');

// Custom attributes
await page.locator('[data-testid="modal"] >> text=Confirm');

// XPath (use sparingly)
await page.locator('xpath=//button[contains(text(), "Submit")]');
```
                """
            },
            "testing": {
                "organization": """
## Test Organization Best Practices

```javascript
test.describe('User Authentication', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto('/login');
    });

    test('should login with valid credentials', async ({ page }) => {
        const loginPage = new LoginPage(page);
        await loginPage.login('user@example.com', 'password123');
        
        await expect(page).toHaveURL('/dashboard');
    });

    test('should show error for invalid credentials', async ({ page }) => {
        const loginPage = new LoginPage(page);
        await loginPage.login('invalid@email.com', 'wrong');
        
        const error = await loginPage.getErrorMessage();
        expect(error).toContain('Invalid credentials');
    });
});
```

**Structure:**
- Group related tests with `describe`
- Use descriptive test names
- Setup common state in `beforeEach`
- Clean, focused test cases
                """,
                "parallel": """
## Parallel Execution Setup

```javascript
// playwright.config.js
export default defineConfig({
    fullyParallel: true,
    workers: process.env.CI ? 2 : 4,
    
    projects: [
        { name: 'chromium', use: devices['Desktop Chrome'] },
        { name: 'firefox', use: devices['Desktop Firefox'] },
        { name: 'webkit', use: devices['Desktop Safari'] },
    ],
});
```

**Best Practices:**
- Use unique test data
- Avoid shared state
- Clean up after tests
- Use `test.serial()` for dependent tests
                """
            }
        }
        
        return content.get(category, {}).get(topic, "Select a category and topic to view content.")
    
    with gr.Blocks(title="Playwright Best Practices") as interface:
        gr.Markdown("## 🎯 Playwright Best Practices Guide")
        
        with gr.Row():
            category = gr.Dropdown(
                choices=["page_objects", "selectors", "testing"],
                value="page_objects",
                label="Category"
            )
            
            topic = gr.Dropdown(
                choices=["basic", "advanced"],
                value="basic",
                label="Topic"
            )
        
        content_output = gr.Markdown(
            value=get_best_practice_content("page_objects", "basic")
        )
        
        def update_topics(selected_category):
            if selected_category == "page_objects":
                return gr.Dropdown(choices=["basic", "advanced"], value="basic")
            elif selected_category == "selectors":
                return gr.Dropdown(choices=["priority", "techniques"], value="priority")
            elif selected_category == "testing":
                return gr.Dropdown(choices=["organization", "parallel"], value="organization")
            return gr.Dropdown(choices=["basic"], value="basic")
        
        # Event handlers
        category.change(
            fn=update_topics,
            inputs=[category],
            outputs=[topic]
        )
        
        category.change(
            fn=lambda cat, top: get_best_practice_content(cat, top),
            inputs=[category, topic],
            outputs=[content_output]
        )
        
        topic.change(
            fn=get_best_practice_content,
            inputs=[category, topic],
            outputs=[content_output]
        )
    
    return interface

def create_principles_interface() -> gr.Interface:
    """Create the OOP and SOLID principles interface"""
    
    def get_principle_content(principle_type: str, principle: str) -> str:
        """Get content for specific principle"""
        
        oop_content = {
            "encapsulation": """
## Encapsulation in Test Automation

**Principle:** Hide internal details and expose only necessary interfaces.

```javascript
class LoginForm {
    constructor(page) {
        this.page = page;
        // Private selectors (encapsulated)
        this._emailField = page.getByTestId('email');
        this._passwordField = page.getByTestId('password');
        this._submitButton = page.getByTestId('submit');
    }

    // Public interface
    async login(email, password) {
        await this._fillEmail(email);
        await this._fillPassword(password);
        await this._submit();
    }

    // Private methods (encapsulated)
    async _fillEmail(email) {
        await this._emailField.fill(email);
    }

    async _fillPassword(password) {
        await this._passwordField.fill(password);
    }

    async _submit() {
        await this._submitButton.click();
    }
}
```

**Benefits:**
- Hides implementation details
- Provides clean public interface
- Reduces coupling
- Easier maintenance
            """,
            "inheritance": """
## Inheritance for Test Base Classes

**Principle:** Share common functionality across related classes.

```javascript
class BasePage {
    constructor(page) {
        this.page = page;
    }

    async waitForLoad() {
        await this.page.waitForLoadState('networkidle');
    }

    async takeScreenshot(name) {
        await this.page.screenshot({ path: `screenshots/${name}.png` });
    }
}

class LoginPage extends BasePage {
    constructor(page) {
        super(page);
        this.emailInput = page.getByTestId('email');
        this.passwordInput = page.getByTestId('password');
    }

    async login(email, password) {
        await this.waitForLoad(); // Inherited method
        await this.emailInput.fill(email);
        await this.passwordInput.fill(password);
        await this.takeScreenshot('before-login'); // Inherited method
    }
}
```

**Benefits:**
- Code reusability
- Consistent setup/teardown
- Shared utility methods
- Hierarchical organization
            """,
            "polymorphism": """
## Polymorphism in Test Frameworks

**Principle:** Objects of different types treated uniformly.

```javascript
class PageInterface {
    async navigate() { throw new Error('Must implement navigate()'); }
    async isLoaded() { throw new Error('Must implement isLoaded()'); }
}

class HomePage extends PageInterface {
    async navigate() { await this.page.goto('/'); }
    async isLoaded() { return await this.page.locator('.hero').isVisible(); }
}

class ProductPage extends PageInterface {
    async navigate() { await this.page.goto('/products'); }
    async isLoaded() { return await this.page.locator('.product-grid').isVisible(); }
}

// Polymorphic usage
async function testPageLoad(pageObject) {
    await pageObject.navigate();
    const loaded = await pageObject.isLoaded();
    expect(loaded).toBe(true);
}

// Works with any page type
await testPageLoad(new HomePage(page));
await testPageLoad(new ProductPage(page));
```
            """,
            "abstraction": """
## Abstraction for Page Objects

**Principle:** Focus on essential features while hiding complexity.

```javascript
class AbstractForm {
    constructor(page) {
        this.page = page;
        this.fields = new Map();
        this.buttons = new Map();
    }

    async fillField(fieldName, value) {
        const field = this.fields.get(fieldName);
        await field.fill(value);
    }

    async clickButton(buttonName) {
        const button = this.buttons.get(buttonName);
        await button.click();
    }

    async submitForm(formData) {
        for (const [field, value] of Object.entries(formData)) {
            await this.fillField(field, value);
        }
        await this.clickButton('submit');
    }
}

class ContactForm extends AbstractForm {
    constructor(page) {
        super(page);
        this.fields.set('name', page.getByTestId('name'));
        this.fields.set('email', page.getByTestId('email'));
        this.buttons.set('submit', page.getByTestId('submit'));
    }
}
```
            """
        }
        
        solid_content = {
            "srp": """
## Single Responsibility Principle

**Principle:** A class should have one reason to change.

```javascript
// GOOD: Separate responsibilities

class UserPage {
    constructor(page) {
        this.page = page;
        this.nameField = page.getByTestId('name');
        this.emailField = page.getByTestId('email');
    }

    async updateProfile(name, email) {
        await this.nameField.fill(name);
        await this.emailField.fill(email);
    }
}

class UserRepository {
    async saveUser(userData) {
        // Database operations only
    }
}

class UserValidator {
    static validateEmail(email) {
        // Validation logic only
    }
}
```

Each class has a single, well-defined responsibility.
            """,
            "ocp": """
## Open/Closed Principle

**Principle:** Open for extension, closed for modification.

```javascript
// Base class (closed for modification)
class ReportGenerator {
    async generateReport(data) {
        throw new Error('Must implement generateReport');
    }
}

// Extensions (open for extension)
class HTMLReportGenerator extends ReportGenerator {
    async generateReport(data) {
        return `<html><body>${JSON.stringify(data)}</body></html>`;
    }
}

class JSONReportGenerator extends ReportGenerator {
    async generateReport(data) {
        return JSON.stringify(data, null, 2);
    }
}

// Easy to add new types without modifying existing code
class XMLReportGenerator extends ReportGenerator {
    async generateReport(data) {
        return `<report>${JSON.stringify(data)}</report>`;
    }
}
```
            """,
            "lsp": """
## Liskov Substitution Principle

**Principle:** Subclasses should be substitutable for their base classes.

```javascript
class BasePage {
    async navigate(url) {
        await this.page.goto(url);
        await this.waitForLoad();
    }

    async waitForLoad() {
        await this.page.waitForLoadState('networkidle');
    }
}

class LoginPage extends BasePage {
    async waitForLoad() {
        // Extends behavior while maintaining contract
        await super.waitForLoad();
        await expect(this.page.locator('.login-form')).toBeVisible();
    }
}

// Both can be used interchangeably
async function testPageNavigation(pageObject, url) {
    await pageObject.navigate(url);
    // Works with BasePage or any subclass
}
```
            """,
            "isp": """
## Interface Segregation Principle

**Principle:** No client should depend on methods it doesn't use.

```javascript
// Segregated interfaces
class Navigatable {
    async navigate(url) { throw new Error('Must implement'); }
    async isLoaded() { throw new Error('Must implement'); }
}

class Searchable {
    async search(query) { throw new Error('Must implement'); }
    async getResults() { throw new Error('Must implement'); }
}

class Shoppable {
    async addToCart(id) { throw new Error('Must implement'); }
}

// Implementations only use needed interfaces
class HomePage extends Navigatable {
    async navigate(url) { await this.page.goto(url); }
    async isLoaded() { return await this.page.locator('.hero').isVisible(); }
}

class ProductPage extends Navigatable {
    async navigate(url) { await this.page.goto(url); }
    async isLoaded() { return await this.page.locator('.product').isVisible(); }
    async addToCart(id) { await this.page.click(`[data-id="${id}"] .add-btn`); }
}
```
            """,
            "dip": """
## Dependency Inversion Principle

**Principle:** Depend on abstractions, not concretions.

```javascript
// Abstraction
class DatabaseInterface {
    async saveResults(results) {
        throw new Error('Must implement saveResults');
    }
}

// Concrete implementations
class MySQLDatabase extends DatabaseInterface {
    async saveResults(results) {
        // MySQL-specific implementation
    }
}

class PostgreSQLDatabase extends DatabaseInterface {
    async saveResults(results) {
        // PostgreSQL-specific implementation
    }
}

// High-level module depends on abstraction
class TestRunner {
    constructor(database) {
        this.database = database; // Depends on interface, not implementation
    }

    async runTests(testSuite) {
        const results = await this.executeTests(testSuite);
        await this.database.saveResults(results); // Uses abstraction
    }
}

// Dependency injection
const testRunner = new TestRunner(new MySQLDatabase());
```
            """
        }
        
        if principle_type == "oop":
            return oop_content.get(principle, "Select an OOP principle to view details.")
        elif principle_type == "solid":
            return solid_content.get(principle, "Select a SOLID principle to view details.")
        
        return "Select a principle type and specific principle."
    
    with gr.Blocks(title="OOP & SOLID Principles") as interface:
        gr.Markdown("## 🏗️ OOP & SOLID Principles in Test Automation")
        
        with gr.Row():
            principle_type = gr.Dropdown(
                choices=["oop", "solid"],
                value="oop",
                label="Principle Type"
            )
            
            principle = gr.Dropdown(
                choices=["encapsulation", "inheritance", "polymorphism", "abstraction"],
                value="encapsulation",
                label="Principle"
            )
        
        content_output = gr.Markdown(
            value=get_principle_content("oop", "encapsulation")
        )
        
        def update_principles(selected_type):
            if selected_type == "oop":
                return gr.Dropdown(
                    choices=["encapsulation", "inheritance", "polymorphism", "abstraction"],
                    value="encapsulation"
                )
            else:  # solid
                return gr.Dropdown(
                    choices=["srp", "ocp", "lsp", "isp", "dip"],
                    value="srp"
                )
        
        # Event handlers
        principle_type.change(
            fn=update_principles,
            inputs=[principle_type],
            outputs=[principle]
        )
        
        principle_type.change(
            fn=lambda ptype, p: get_principle_content(ptype, p),
            inputs=[principle_type, principle],
            outputs=[content_output]
        )
        
        principle.change(
            fn=get_principle_content,
            inputs=[principle_type, principle],
            outputs=[content_output]
        )
    
    return interface

def create_ai_chat_interface() -> gr.Interface:
    """Create the AI-powered chat interface"""
    
    def chat_with_ai(message: str, history: List[List[str]]) -> Tuple[str, List[List[str]]]:
        """Chat with the AI assistant"""
        
        # Import AI service
        try:
            from services.ai_service import ai_service
            response = ai_service.generate_response(message)
        except Exception as e:
            response = f"I'm here to help with Playwright questions! Please ask about:\n\n" \
                      f"• Cypress to Playwright migration\n" \
                      f"• Playwright best practices\n" \
                      f"• OOP principles in testing\n" \
                      f"• SOLID principles\n" \
                      f"• Test automation frameworks\n\n" \
                      f"(Note: AI model not available - {str(e)})"
        
        history.append([message, response])
        return "", history
    
    with gr.Blocks(title="AI Assistant") as interface:
        gr.Markdown("## 🤖 AI-Powered Playwright Assistant")
        gr.Markdown("Ask questions about Playwright, testing best practices, or code conversion!")
        
        chatbot = gr.Chatbot(
            value=[],
            height=500,
            label="Chat with Kimi-K2-Instruct"
        )
        
        with gr.Row():
            msg = gr.Textbox(
                placeholder="Ask me about Playwright, migration, best practices, OOP, SOLID principles...",
                label="Your Question",
                scale=4
            )
            send_btn = gr.Button("Send", variant="primary", scale=1)
        
        clear_btn = gr.Button("Clear Chat")
        
        # Event handlers
        send_btn.click(
            fn=chat_with_ai,
            inputs=[msg, chatbot],
            outputs=[msg, chatbot]
        )
        
        msg.submit(
            fn=chat_with_ai,
            inputs=[msg, chatbot],
            outputs=[msg, chatbot]
        )
        
        clear_btn.click(
            fn=lambda: ([], ""),
            outputs=[chatbot, msg]
        )
    
    return interface


def create_architecture_interface() -> gr.Interface:
    """Create the Playwright architecture analysis interface"""
    
    from data.architecture_analysis import get_architecture_analysis
    
    # Get architecture data
    arch_data = get_architecture_analysis()
    
    def display_architecture_section(section_name: str) -> str:
        """Display specific architecture section content"""
        
        if section_name == "overview":
            data = arch_data["overview"]
            content = f"""
# {data["title"]}

{data["introduction"]}

## {data["sections"][0]["title"]}

{data["sections"][0]["content"]}

{data["sections"][0]["diagram"]}
            """
            
        elif section_name == "communication":
            data = arch_data["communication"]
            content = f"""
# {data["title"]}

{data["overview"]}

## {data["tiers"][0]["name"]}

{data["tiers"][0]["description"]}

**Advantages:**
""" + "\n".join([f"• {adv}" for adv in data["tiers"][0]["advantages"]]) + f"""

## {data["tiers"][1]["name"]}

{data["tiers"][1]["description"]}

**Browser Protocols:**
""" + "\n".join([f"• **{browser}**: {protocol}" for browser, protocol in data["tiers"][1]["protocols"].items()]) + f"""

{data["tiers"][1]["enhancement"]}
            """
            
        elif section_name == "contexts":
            data = arch_data["contexts"]
            content = f"""
# {data["title"]}

{data["overview"]}

## Definition

{data["definition"]}

## Isolation Features
""" + "\n".join([f"• {feature}" for feature in data["isolation_features"]]) + """

## Performance Benefits
""" + "\n".join([f"• {benefit}" for benefit in data["performance_benefits"]]) + """

## Use Cases
""" + "\n".join([f"• {use_case}" for use_case in data["use_cases"]])
            
        elif section_name == "auto_waiting":
            data = arch_data["auto_waiting"]
            content = f"""
# {data["title"]}

## Philosophy

{data["philosophy"]}

## The Five Core Actionability Checks

"""
            for check in data["actionability_checks"]:
                content += f"""
### {check["name"]}
{check["description"]}
*{check["note"]}*

"""
            
            content += f"""
## Actionability Matrix

{data["actionability_matrix"]}
            """
            
        elif section_name == "selectors":
            data = arch_data["selectors"]
            content = f"""
# {data["title"]}

## Locator API Philosophy

{data["locator_api"]}

## Lazy Evaluation

{data["lazy_evaluation"]}

## User-Centric Selectors

""" + "\n".join([f"• {selector}" for selector in data["user_centric_selectors"]]) + """

## CSS Engine Extensions

"""
            for ext in data["css_extensions"]:
                content += f"""
### {ext["category"]}
**Selectors**: {", ".join(ext["selectors"])}
{ext["description"]}

"""
            
        elif section_name == "environment":
            data = arch_data["environment"]
            content = f"""
# {data["title"]}

## Hermetic Approach

{data["hermetic_approach"]}

## Browser Management Features

""" + "\n".join([f"• {feature}" for feature in data["browser_management"]]) + """

## Enterprise Configuration Variables

"""
            for config in data["enterprise_configuration"]:
                content += f"""
### {config["variable"]}
{config["description"]}

"""
            
        elif section_name == "comparison":
            data = arch_data["comparison"]
            content = f"""
# {data["title"]}

| Aspect | Playwright | Selenium | Cypress |
|--------|------------|----------|---------|
| **Communication** | {data["frameworks"]["Playwright"]["communication"]} | {data["frameworks"]["Selenium"]["communication"]} | {data["frameworks"]["Cypress"]["communication"]} |
| **Execution Context** | {data["frameworks"]["Playwright"]["execution_context"]} | {data["frameworks"]["Selenium"]["execution_context"]} | {data["frameworks"]["Cypress"]["execution_context"]} |
| **Isolation Model** | {data["frameworks"]["Playwright"]["isolation"]} | {data["frameworks"]["Selenium"]["isolation"]} | {data["frameworks"]["Cypress"]["isolation"]} |
| **Browser Management** | {data["frameworks"]["Playwright"]["browser_management"]} | {data["frameworks"]["Selenium"]["browser_management"]} | {data["frameworks"]["Cypress"]["browser_management"]} |
| **Philosophy** | {data["frameworks"]["Playwright"]["philosophy"]} | {data["frameworks"]["Selenium"]["philosophy"]} | {data["frameworks"]["Cypress"]["philosophy"]} |
            """
            
        elif section_name == "recommendations":
            data = arch_data["recommendations"]
            content = f"""
# {data["title"]}

## Test Authoring Best Practices

""" + "\n".join([f"• {practice}" for practice in data["test_authoring"]]) + """

## Test Structure Guidelines

""" + "\n".join([f"• {guideline}" for guideline in data["test_structure"]]) + """

## Selector Strategy

""" + "\n".join([f"• {strategy}" for strategy in data["selector_strategy"]]) + """

## Debugging Approach

""" + "\n".join([f"• {approach}" for approach in data["debugging"]]) + """

## CI/CD Environment Setup

""" + "\n".join([f"• {setup}" for setup in data["cicd_environment"]])
            
        else:
            content = "Section not found."
            
        return content
    
    def create_architecture_diagram() -> str:
        """Create ASCII architecture diagram"""
        return """
```
Playwright Architecture Overview
================================

┌─────────────────────────────────────────────────────────────────────────────┐
│                           Playwright Architecture                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────┐    WebSocket/RPC     ┌──────────────────┐              │
│  │  Client Code    │◄────────────────────►│ Playwright Server│              │
│  │                 │     JSON Messages    │   (Node.js)      │              │
│  │ • JavaScript    │                      │                  │              │
│  │ • TypeScript    │                      │ • Command Router │              │
│  │ • Python        │                      │ • State Manager  │              │
│  │ • Java          │                      │ • Event Handler  │              │
│  │ • .NET          │                      │                  │              │
│  └─────────────────┘                      └──────────────────┘              │
│                                                    │                        │
│                                                    │ Native Protocols       │
│                                                    ▼                        │
│  ┌─────────────────────────────────────────────────────────────────────────┐ │
│  │                         Browser Layer                                  │ │
│  │                                                                         │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │ │
│  │  │   Chromium   │  │   Firefox    │  │    WebKit    │                 │ │
│  │  │     CDP+     │  │   Remote     │  │   Remote     │                 │ │
│  │  │   Protocol   │  │   Protocol   │  │   Protocol   │                 │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘                 │ │
│  │           │                │                │                          │ │
│  │           ▼                ▼                ▼                          │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │ │
│  │  │  Browser     │  │  Browser     │  │  Browser     │                 │ │
│  │  │  Context 1   │  │  Context 2   │  │  Context N   │                 │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘                 │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘

Key Architectural Principles:
• Decoupled client-server design for language agnosticism
• Persistent WebSocket communication for low latency
• Native browser protocols for deep control
• BrowserContexts for efficient isolation
• Auto-waiting with actionability checks for reliability
```
        """
    
    with gr.Blocks() as interface:
        gr.Markdown("""
        ## 🏗️ Playwright Architecture Deep Dive
        
        Explore the internal architecture and design principles that make Playwright powerful and reliable.
        """)
        
        # Architecture diagram
        with gr.Tab("📊 Overview Diagram"):
            gr.Markdown(create_architecture_diagram())
        
        # Section selector and content
        with gr.Row():
            with gr.Column(scale=1):
                section_selector = gr.Dropdown(
                    choices=[
                        ("Core Architecture", "overview"),
                        ("Communication System", "communication"), 
                        ("Browser Contexts", "contexts"),
                        ("Auto-Waiting Engine", "auto_waiting"),
                        ("Selector Engine", "selectors"),
                        ("Environment Management", "environment"),
                        ("Framework Comparison", "comparison"),
                        ("Best Practices", "recommendations")
                    ],
                    value="overview",
                    label="Architecture Section",
                    interactive=True
                )
                
                analyze_btn = gr.Button("📖 Load Section", variant="primary")
                
                gr.Markdown("""
                ### 🎯 Quick Navigation
                
                **Core Concepts:**
                - Client-Server Model
                - WebSocket Communication
                - Browser Contexts
                
                **Deep Dive:**
                - Auto-Waiting System
                - Selector Engine
                - Native Protocols
                
                **Practical:**
                - Framework Comparison
                - Best Practices
                - Environment Setup
                """)
            
            with gr.Column(scale=2):
                content_display = gr.Markdown(
                    value=display_architecture_section("overview"),
                    label="Architecture Analysis"
                )
        
        # Interactive exploration
        with gr.Tab("🔍 Interactive Analysis"):
            gr.Markdown("""
            ### Explore Architecture Concepts
            
            Use the tools below to dive deeper into specific architectural concepts.
            """)
            
            with gr.Row():
                concept_input = gr.Textbox(
                    placeholder="Enter architecture concept (e.g., 'BrowserContext', 'WebSocket', 'Actionability')",
                    label="Architecture Concept",
                    scale=3
                )
                explore_btn = gr.Button("🔍 Explore", variant="secondary", scale=1)
            
            concept_output = gr.Markdown(label="Concept Analysis")
            
            def explore_concept(concept: str) -> str:
                """Explore specific architecture concepts"""
                concept_lower = concept.lower()
                
                if "browsercontext" in concept_lower or "context" in concept_lower:
                    return """
## BrowserContext Deep Dive

**What it is:** An isolated browser session within a single browser process.

**Key Features:**
- Lightweight creation (milliseconds)
- Complete isolation (cookies, storage, permissions)
- Perfect for parallel testing
- Enables multi-user scenarios

**Performance Impact:**
- Memory: ~2-5MB per context vs ~50-100MB per browser process
- CPU: Negligible overhead vs significant process startup cost
- Disk: Shared browser binary, isolated profile data

**Implementation:**
```javascript
// Create isolated contexts
const context1 = await browser.newContext();
const context2 = await browser.newContext();

// Each context is completely isolated
await context1.addCookies([{name: 'user', value: 'alice'}]);
await context2.addCookies([{name: 'user', value: 'bob'}]);
```
                    """
                elif "websocket" in concept_lower or "communication" in concept_lower:
                    return """
## WebSocket Communication Architecture

**Why WebSocket over HTTP:**
- Persistent connection eliminates handshake overhead
- Full-duplex communication for real-time events
- Lower latency for rapid command sequences
- Stateful session management

**Message Flow:**
1. Client sends command as JSON-RPC message
2. Server receives and validates command
3. Server translates to browser protocol
4. Browser executes and sends events back
5. Server forwards events to client

**Performance Benefits:**
- Selenium: ~10-50ms per command (HTTP overhead)
- Playwright: ~1-5ms per command (persistent connection)
                    """
                elif "actionability" in concept_lower or "waiting" in concept_lower:
                    return """
## Auto-Waiting and Actionability System

**The Problem:** Traditional automation fails when elements are present but not ready.

**The Solution:** Multi-dimensional readiness checks before every action.

**Actionability Algorithm:**
```
For each action:
1. Find element(s) matching locator
2. For each required check:
   - Evaluate condition
   - If failed, wait 100ms and retry
   - Continue until pass or timeout
3. Execute action only when all checks pass
```

**Real-World Impact:**
- Eliminates 80%+ of timing-related test failures
- No need for manual wait strategies
- Tests become more reliable and maintainable
                    """
                elif "selector" in concept_lower or "locator" in concept_lower:
                    return """
## Selector Engine Architecture

**Philosophy:** Tests should describe what users see, not implementation details.

**Locator Hierarchy (Recommended Order):**
1. **Semantic**: `getByRole('button', {name: 'Submit'})`
2. **Text-based**: `getByText('Click here')`
3. **Accessibility**: `getByLabel('Username')`
4. **Test IDs**: `getByTestId('submit-btn')`
5. **CSS/XPath**: `locator('.submit-button')` (last resort)

**Engine Extensions:**
- Layout-based: `:right-of()`, `:below()`
- Text matching: `:has-text()`, `:text-is()`
- Visibility: `:visible`
- Shadow DOM: Automatic piercing

**Performance Optimization:**
- Lazy evaluation (queries executed on action)
- Intelligent retry logic
- Cached element references where safe
                    """
                else:
                    return f"""
## Architecture Concept: {concept}

Try exploring these key concepts:
- **BrowserContext**: Isolation and performance model
- **WebSocket**: Communication architecture  
- **Actionability**: Auto-waiting system
- **Selector**: Element identification engine
- **Native Protocols**: Browser communication layer

Or ask specific questions about Playwright's internal design!
                    """
            
            explore_btn.click(
                fn=explore_concept,
                inputs=[concept_input],
                outputs=[concept_output]
            )
        
        # Event handlers for section selection
        analyze_btn.click(
            fn=display_architecture_section,
            inputs=[section_selector],
            outputs=[content_display]
        )
        
        section_selector.change(
            fn=display_architecture_section,
            inputs=[section_selector], 
            outputs=[content_display]
        )
    
    return interface
