"""
Cypress to Playwright Migration Guide
=====================================

This module contains comprehensive examples and guidance for migrating from Cypress to Playwright.
"""

# Basic syntax comparison examples
SYNTAX_COMPARISONS = [
    {
        "title": "Basic Test Structure",
        "cypress_code": """// Cypress
describe('Login Tests', () => {
    beforeEach(() => {
        cy.visit('/login');
    });

    it('should login successfully', () => {
        cy.get('[data-testid="username"]').type('user@example.com');
        cy.get('[data-testid="password"]').type('password123');
        cy.get('[data-testid="login-button"]').click();
        cy.url().should('include', '/dashboard');
    });
});""",
        "playwright_code": """// Playwright
import { test, expect } from '@playwright/test';

test.describe('Login Tests', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto('/login');
    });

    test('should login successfully', async ({ page }) => {
        await page.getByTestId('username').fill('user@example.com');
        await page.getByTestId('password').fill('password123');
        await page.getByTestId('login-button').click();
        await expect(page).toHaveURL(/.*dashboard/);
    });
});""",
        "explanation": """
Key differences:
1. Playwright uses async/await syntax
2. Page object is passed as parameter
3. Different selector methods (getByTestId vs get)
4. Different assertion syntax (expect vs should)
"""
    },
    {
        "title": "Element Interactions",
        "cypress_code": """// Cypress
cy.get('#dropdown').select('Option 1');
cy.get('[type="checkbox"]').check();
cy.get('[type="radio"]').check();
cy.get('input').clear().type('new text');
cy.get('button').should('be.visible').click();""",
        "playwright_code": """// Playwright
await page.locator('#dropdown').selectOption('Option 1');
await page.locator('[type="checkbox"]').check();
await page.locator('[type="radio"]').check();
await page.locator('input').clear();
await page.locator('input').fill('new text');
await expect(page.locator('button')).toBeVisible();
await page.locator('button').click();""",
        "explanation": """
Key differences:
1. selectOption() instead of select()
2. fill() instead of type()
3. Separate clear() and fill() operations
4. toBeVisible() assertion before interaction
"""
    },
    {
        "title": "URL Navigation and Assertions",
        "cypress_code": """// Cypress
cy.visit('/login');
cy.url().should('include', '/dashboard');
cy.url().should('eq', 'https://example.com/profile');
cy.url().should('contain', 'success');
cy.go('back');
cy.reload();""",
        "playwright_code": """// Playwright
await page.goto('/login');
await expect(page).toHaveURL(/.*dashboard/);
await expect(page).toHaveURL('https://example.com/profile');
await expect(page).toHaveURL(/.*success/);
await page.goBack();
await page.reload();""",
        "explanation": """
Key differences:
1. goto() instead of visit()
2. toHaveURL() with regex for partial matches
3. toHaveURL() with string for exact matches
4. goBack() instead of go('back')
5. All operations are async and require await
"""
    },
    {
        "title": "Waiting Strategies and Network Interception",
        "cypress_code": """// Cypress Waiting Patterns
// Network waiting with alias
cy.intercept('GET', '/api/data', { fixture: 'data.json' }).as('getData');
cy.visit('/dashboard');
cy.wait('@getData').its('response.statusCode').should('eq', 200);

// Fixed timeout waiting (discouraged)
cy.wait(3000);

// Element state waiting
cy.get('.loading').should('not.exist');
cy.get('.content').should('be.visible');

// Custom condition waiting
cy.waitUntil(() => window.appReady === true);""",
        "playwright_code": """// Playwright Waiting Patterns
// Network waiting and mocking
await page.route('/api/data', route => {
    route.fulfill({ path: 'fixtures/data.json' });
});
await page.goto('/dashboard');
const response = await page.waitForResponse('/api/data');
expect(response.status()).toBe(200);

// Fixed timeout (still discouraged, but available)
await page.waitForTimeout(3000);

// Element state waiting (auto-wait built-in)
await expect(page.locator('.loading')).not.toBeVisible();
await expect(page.locator('.content')).toBeVisible();

// Custom condition waiting
await page.waitForFunction(() => window.appReady === true);""",
        "explanation": """
Key differences:
1. page.route() + waitForResponse() instead of intercept + wait(@alias)
2. Direct response.status() access instead of .its() chaining
3. Auto-waiting in expect() assertions eliminates most manual waits
4. waitForFunction() for custom JavaScript conditions
5. All operations require await keyword
"""
    },
    {
        "title": "Waiting and Assertions",
        "cypress_code": """// Cypress
cy.get('.loading').should('not.exist');
cy.get('.content').should('be.visible');
cy.get('.text').should('contain', 'Success');
cy.get('.counter').should('have.text', '5');
cy.url().should('eq', 'https://example.com/page');""",
        "playwright_code": """// Playwright
await expect(page.locator('.loading')).not.toBeVisible();
await expect(page.locator('.content')).toBeVisible();
await expect(page.locator('.text')).toContainText('Success');
await expect(page.locator('.counter')).toHaveText('5');
await expect(page).toHaveURL('https://example.com/page');""",
        "explanation": """
Key differences:
1. All assertions use expect() function
2. Different assertion methods (toBeVisible vs be.visible)
3. toContainText instead of contain
4. Page-level assertions for URL
"""
    }
]

# Configuration migration examples
CONFIG_MIGRATION = {
    "cypress_config": """// cypress.config.js
const { defineConfig } = require('cypress');

module.exports = defineConfig({
    e2e: {
        baseUrl: 'http://localhost:3000',
        viewportWidth: 1280,
        viewportHeight: 720,
        defaultCommandTimeout: 10000,
        requestTimeout: 10000,
        supportFile: 'cypress/support/e2e.js',
        specPattern: 'cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',
        setupNodeEvents(on, config) {
            // implement node event listeners here
        },
    },
});""",
    "playwright_config": """// playwright.config.js
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
    testDir: './tests',
    timeout: 30 * 1000,
    expect: {
        timeout: 5000
    },
    fullyParallel: true,
    retries: process.env.CI ? 2 : 0,
    workers: process.env.CI ? 1 : undefined,
    reporter: 'html',
    use: {
        baseURL: 'http://localhost:3000',
        actionTimeout: 10000,
        navigationTimeout: 10000,
        trace: 'on-first-retry',
    },
    projects: [
        {
            name: 'chromium',
            use: { ...devices['Desktop Chrome'] },
        },
        {
            name: 'firefox',
            use: { ...devices['Desktop Firefox'] },
        },
        {
            name: 'webkit',
            use: { ...devices['Desktop Safari'] },
        },
    ],
});""",
    "explanation": """
Key differences:
1. Playwright uses projects for multi-browser testing
2. Built-in parallel execution support
3. Different timeout configurations
4. Built-in trace and reporting features
"""
}

# Advanced migration patterns
ADVANCED_PATTERNS = [
    {
        "title": "Custom Commands to Page Object Model",
        "cypress_code": """// Cypress Custom Command
Cypress.Commands.add('loginAs', (username, password) => {
    cy.get('[data-testid="username"]').type(username);
    cy.get('[data-testid="password"]').type(password);
    cy.get('[data-testid="login-button"]').click();
    cy.get('[data-testid="dashboard"]').should('be.visible');
});

// Usage
cy.loginAs('user@example.com', 'password123');""",
        "playwright_code": """// Playwright Page Object Model
class LoginPage {
    constructor(page) {
        this.page = page;
        this.usernameInput = page.getByTestId('username');
        this.passwordInput = page.getByTestId('password');
        this.loginButton = page.getByTestId('login-button');
        this.dashboard = page.getByTestId('dashboard');
    }

    async loginAs(username, password) {
        await this.usernameInput.fill(username);
        await this.passwordInput.fill(password);
        await this.loginButton.click();
        await expect(this.dashboard).toBeVisible();
    }
}

// Usage
const loginPage = new LoginPage(page);
await loginPage.loginAs('user@example.com', 'password123');""",
        "explanation": """
Migration strategy:
1. Convert custom commands to Page Object methods
2. Use class-based approach for better organization
3. Encapsulate selectors within page objects
4. Maintain the same functionality with improved structure
"""
    },
    {
        "title": "Network Interception and API Mocking",
        "cypress_code": """// Cypress Network Interception
cy.intercept('GET', '/api/dashboard/items', {
    fixture: 'dashboard-items.json'
}).as('getDashboardData');

cy.visit('/dashboard');
cy.wait('@getDashboardData').its('response.statusCode').should('eq', 200);
cy.get('.dashboard-item').should('have.length', 3);""",
        "playwright_code": """// Playwright Network Interception
await page.route('/api/dashboard/items', route => {
    route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([
            { "id": 1, "name": "First Item", "status": "active" },
            { "id": 2, "name": "Second Item", "status": "inactive" },
            { "id": 3, "name": "Third Item", "status": "active" }
        ])
    });
});

await page.goto('/dashboard');
const response = await page.waitForResponse('/api/dashboard/items');
expect(response.status()).toBe(200);
await expect(page.locator('.dashboard-item')).toHaveCount(3);""",
        "explanation": """
Key differences:
1. page.route() instead of cy.intercept()
2. route.fulfill() for mocking responses
3. page.waitForResponse() instead of cy.wait('@alias')
4. Direct response status checking
5. toHaveCount() instead of should('have.length')
"""
    },
    {
        "title": "API Requests and Authentication",
        "cypress_code": """// Cypress API Request and Login
Cypress.Commands.add('loginByApi', () => {
    cy.request({
        method: 'POST',
        url: '/api/login',
        body: {
            username: Cypress.env('username'),
            password: Cypress.env('password'),
        },
    }).then((response) => {
        window.localStorage.setItem('authToken', response.body.token);
    });
});

// Usage in test
cy.loginByApi();
cy.visit('/dashboard');""",
        "playwright_code": """// Playwright API Request and Login
class AuthHelper {
    constructor(page, request) {
        this.page = page;
        this.request = request;
    }

    async loginByApi() {
        const response = await this.request.post('/api/login', {
            data: {
                username: process.env.USERNAME,
                password: process.env.PASSWORD,
            }
        });
        
        const { token } = await response.json();
        await this.page.evaluate((token) => {
            localStorage.setItem('authToken', token);
        }, token);
    }
}

// Usage in test
const authHelper = new AuthHelper(page, request);
await authHelper.loginByApi();
await page.goto('/dashboard');""",
        "explanation": """
Migration approach:
1. Convert custom commands to utility classes
2. Use request fixture for API calls
3. page.evaluate() for browser context code
4. process.env for environment variables
5. Explicit async/await handling
"""
    },
    {
        "title": "Element Iteration and Aliases",
        "cypress_code": """// Cypress Element Iteration with Aliases
cy.get('.dashboard-item').as('dashboardItems');
cy.get('@dashboardItems').should('have.length', 3);

cy.get('@dashboardItems').each(($item, index) => {
    cy.wrap($item).find('h3').should('not.be.empty');
    cy.wrap($item)
        .find('.item-status')
        .should('have.class', index % 2 === 0 ? 'status-active' : 'status-inactive');
});""",
        "playwright_code": """// Playwright Element Iteration with Variables
const dashboardItems = page.locator('.dashboard-item');
await expect(dashboardItems).toHaveCount(3);

const itemCount = await dashboardItems.count();
for (let i = 0; i < itemCount; i++) {
    const item = dashboardItems.nth(i);
    await expect(item.locator('h3')).not.toBeEmpty();
    
    const expectedClass = i % 2 === 0 ? 'status-active' : 'status-inactive';
    await expect(item.locator('.item-status')).toHaveClass(expectedClass);
}""",
        "explanation": """
Key changes:
1. Variables instead of aliases (no .as() needed)
2. Standard for loop instead of .each()
3. locator.nth(index) for specific elements
4. locator.count() to get element count
5. Cleaner scoping with direct variable references
"""
    },
    {
        "title": "Tasks and Environment Configuration",
        "cypress_code": """// Cypress Task and Environment Usage
// In cypress.config.js
setupNodeEvents(on, config) {
    on('task', {
        log(message) {
            console.log(`[TASK LOG] ${message}`);
            return null;
        },
    });
}

// In test
cy.task('log', 'API call was mocked and received successfully.');
const username = Cypress.env('username');""",
        "playwright_code": """// Playwright Environment and Logging
// In test setup or helper
class TestLogger {
    static log(message) {
        console.log(`[TEST LOG] ${message}`);
    }
}

// In test
TestLogger.log('API call was mocked and received successfully.');
const username = process.env.USERNAME;

// Or using built-in test info
test('example test', async ({ page }, testInfo) => {
    testInfo.annotations.push({ type: 'info', description: 'API call mocked' });
});""",
        "explanation": """
Migration approach:
1. Replace cy.task() with direct function calls or classes
2. Use process.env instead of Cypress.env()
3. Leverage Playwright's built-in test.info for annotations
4. Create utility classes for common operations
5. Use standard Node.js patterns for non-browser code
"""
    },
    {
        "title": "Advanced Wait Patterns and Aliases",
        "cypress_code": """// Cypress Advanced Waiting
// Multiple network requests with different aliases
cy.intercept('GET', '/api/users', { fixture: 'users.json' }).as('getUsers');
cy.intercept('POST', '/api/users', { statusCode: 201 }).as('createUser');

cy.visit('/users');
cy.wait('@getUsers');

cy.get('#create-user-btn').click();
cy.get('#username').type('newuser');
cy.get('#submit').click();
cy.wait('@createUser').its('response.statusCode').should('eq', 201);

// Waiting for multiple requests
cy.wait(['@getUsers', '@getProfile']);

// Conditional waiting
cy.get('.notification').should('be.visible');
cy.wait('@getUsers').then((interception) => {
    if (interception.response.statusCode === 200) {
        cy.get('.success-message').should('be.visible');
    }
});""",
        "playwright_code": """// Playwright Advanced Waiting
// Multiple network requests with variables
await page.route('/api/users', route => {
    if (route.request().method() === 'GET') {
        route.fulfill({ path: 'fixtures/users.json' });
    } else if (route.request().method() === 'POST') {
        route.fulfill({ status: 201, body: '{"success": true}' });
    }
});

await page.goto('/users');
await page.waitForResponse('/api/users');

await page.locator('#create-user-btn').click();
await page.locator('#username').fill('newuser');
await page.locator('#submit').click();
const createResponse = await page.waitForResponse(request => 
    request.url().includes('/api/users') && request.method() === 'POST'
);
expect(createResponse.status()).toBe(201);

// Waiting for multiple requests
await Promise.all([
    page.waitForResponse('/api/users'),
    page.waitForResponse('/api/profile')
]);

// Conditional waiting
await expect(page.locator('.notification')).toBeVisible();
const response = await page.waitForResponse('/api/users');
if (response.status() === 200) {
    await expect(page.locator('.success-message')).toBeVisible();
}""",
        "explanation": """
Advanced wait migration:
1. Single route handler for multiple HTTP methods
2. Response filtering with request.method() and url()
3. Promise.all() for multiple concurrent waits
4. Direct response status checking with conditionals
5. No aliases needed - use variables and direct references
"""
    }
]

def get_migration_guide():
    """Get the complete migration guide"""
    return {
        "syntax_comparisons": SYNTAX_COMPARISONS,
        "config_migration": CONFIG_MIGRATION,
        "advanced_patterns": ADVANCED_PATTERNS
    }
