# Cypress to Playwright Conversion Methodology

## 📋 Table of Contents
- [Overview](#overview)
- [Conversion Strategy](#conversion-strategy)
- [Syntax Mapping](#syntax-mapping)
- [Configuration Migration](#configuration-migration)
- [Advanced Patterns](#advanced-patterns)
- [Architecture Analysis](#architecture-analysis)
- [Best Practices](#best-practices)
- [Common Pitfalls](#common-pitfalls)
- [Automation Tools](#automation-tools)

## 🎯 Overview

This document outlines the systematic approach used in the Playwright Studies Portal for converting Cypress test automation code to Playwright. The conversion methodology is based on practical experience, industry best practices, and maintaining test quality during migration.

### Why Migrate from Cypress to Playwright?

| Aspect | Cypress | Playwright |
|--------|---------|------------|
| **Browser Support** | Chrome, Firefox, Edge | Chrome, Firefox, Safari, Edge |
| **Parallel Execution** | Limited | Native support |
| **Multiple Tabs/Windows** | Not supported | Full support |
| **Language Support** | JavaScript/TypeScript | JavaScript, TypeScript, Python, Java, C# |
| **Mobile Testing** | Limited | Device emulation + real devices |
| **Auto-wait** | Built-in | More robust auto-wait |
| **Network Interception** | Good | Excellent |
| **CI/CD Performance** | Good | Superior |

## 🔄 Conversion Strategy

### Phase 1: Analysis and Planning
1. **Audit existing Cypress tests**
   - Count test files and test cases
   - Identify custom commands
   - Document test patterns used
   - Note dependencies and plugins

2. **Plan migration approach**
   - Decide on gradual vs. complete migration
   - Choose Playwright language (JS/TS/Python)
   - Design new test structure
   - Plan for parallel execution

### Phase 2: Environment Setup
```bash
# Remove Cypress dependencies
npm uninstall cypress

# Install Playwright
npm init playwright@latest
# or
pip install playwright
playwright install
```

### Phase 3: Systematic Conversion
1. Start with simplest test files
2. Convert configuration first
3. Migrate utility functions
4. Convert test files one by one
5. Update CI/CD pipelines

## 🔧 Syntax Mapping

### Basic Test Structure

#### Cypress → Playwright
```javascript
// BEFORE (Cypress)
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
});
```

```javascript
// AFTER (Playwright)
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
});
```

### Element Selection and Interaction

| Cypress | Playwright | Notes |
|---------|------------|-------|
| `cy.get('#id')` | `page.locator('#id')` | Basic CSS selector |
| `cy.get('[data-testid="btn"]')` | `page.getByTestId('btn')` | Recommended approach |
| `cy.contains('text')` | `page.getByText('text')` | Text-based selection |
| `cy.get('input').type('text')` | `page.locator('input').fill('text')` | Text input |
| `cy.get('select').select('option')` | `page.locator('select').selectOption('option')` | Dropdown selection |
| `cy.get('checkbox').check()` | `page.locator('checkbox').check()` | Checkbox interaction |

### Assertions

| Cypress | Playwright | Notes |
|---------|------------|-------|
| `cy.get('el').should('be.visible')` | `await expect(page.locator('el')).toBeVisible()` | Visibility check |
| `cy.get('el').should('contain', 'text')` | `await expect(page.locator('el')).toContainText('text')` | Text content |
| `cy.get('el').should('have.text', 'exact')` | `await expect(page.locator('el')).toHaveText('exact')` | Exact text match |
| `cy.url().should('include', '/path')` | `await expect(page).toHaveURL(/.*path/)` | URL verification |
| `cy.get('el').should('have.attr', 'class')` | `await expect(page.locator('el')).toHaveAttribute('class', 'value')` | Attribute check |

### Waiting Strategies

| Cypress | Playwright | Notes |
|---------|------------|-------|
| `cy.wait(5000)` | `await page.waitForTimeout(5000)` | Fixed wait (discouraged) |
| `cy.get('el').should('be.visible')` | `await expect(page.locator('el')).toBeVisible()` | Wait for element |
| `cy.wait('@apiCall')` | `await page.waitForResponse('**/api/**')` | Wait for network |
| `cy.get('el', {timeout: 10000})` | `await page.locator('el').waitFor({timeout: 10000})` | Custom timeout |

## ⚙️ Configuration Migration

### Test Configuration

#### Cypress Config → Playwright Config
```javascript
// cypress.config.js
module.exports = defineConfig({
    e2e: {
        baseUrl: 'http://localhost:3000',
        viewportWidth: 1280,
        viewportHeight: 720,
        defaultCommandTimeout: 10000,
        supportFile: 'cypress/support/e2e.js',
        specPattern: 'cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',
    },
});
```

```javascript
// playwright.config.js
export default defineConfig({
    testDir: './tests',
    timeout: 30 * 1000,
    expect: { timeout: 5000 },
    fullyParallel: true,
    retries: process.env.CI ? 2 : 0,
    use: {
        baseURL: 'http://localhost:3000',
        viewport: { width: 1280, height: 720 },
        actionTimeout: 10000,
        trace: 'on-first-retry',
    },
    projects: [
        { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
        { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
        { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    ],
});
```

### Key Configuration Differences
- **Multi-browser**: Playwright projects vs Cypress single browser
- **Parallelization**: Built-in vs plugin-dependent
- **Timeouts**: More granular control in Playwright
- **Traces**: Built-in debugging capabilities

## 🏗️ Advanced Patterns

### Custom Commands → Page Object Model

#### Cypress Custom Commands
```javascript
// cypress/support/commands.js
Cypress.Commands.add('loginAs', (username, password) => {
    cy.get('[data-testid="username"]').type(username);
    cy.get('[data-testid="password"]').type(password);
    cy.get('[data-testid="login-button"]').click();
    cy.get('[data-testid="dashboard"]').should('be.visible');
});

// Usage in tests
cy.loginAs('user@example.com', 'password123');
```

#### Playwright Page Object Model
```javascript
// pages/LoginPage.js
export class LoginPage {
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

// Usage in tests
import { LoginPage } from '../pages/LoginPage.js';

test('login test', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.loginAs('user@example.com', 'password123');
});
```

### Network Interception

#### Cypress
```javascript
cy.intercept('GET', '/api/users', { fixture: 'users.json' }).as('getUsers');
cy.visit('/users');
cy.wait('@getUsers');
```

#### Playwright
```javascript
await page.route('/api/users', route => {
    route.fulfill({ path: 'fixtures/users.json' });
});
await page.goto('/users');
await page.waitForResponse('/api/users');
```

### File Uploads

#### Cypress
```javascript
cy.get('input[type="file"]').selectFile('cypress/fixtures/file.pdf');
```

#### Playwright
```javascript
await page.setInputFiles('input[type="file"]', 'tests/fixtures/file.pdf');
```

## 🎯 Best Practices

### 1. Locator Strategy Priority
1. **User-facing attributes**: `getByRole()`, `getByText()`, `getByLabel()`
2. **Test IDs**: `getByTestId()` for elements without semantic meaning
3. **CSS selectors**: Last resort, prefer stable attributes

### 2. Page Object Design
```javascript
class BasePage {
    constructor(page) {
        this.page = page;
    }

    async waitForPageLoad() {
        await this.page.waitForLoadState('networkidle');
    }
}

class LoginPage extends BasePage {
    constructor(page) {
        super(page);
        this.usernameInput = page.getByLabel('Username');
        this.passwordInput = page.getByLabel('Password');
        this.loginButton = page.getByRole('button', { name: 'Login' });
    }

    async login(username, password) {
        await this.usernameInput.fill(username);
        await this.passwordInput.fill(password);
        await this.loginButton.click();
        await this.waitForPageLoad();
    }
}
```

### 3. Parallel Execution Setup
```javascript
// playwright.config.js
export default defineConfig({
    fullyParallel: true,
    workers: process.env.CI ? 2 : undefined,
    projects: [
        {
            name: 'setup',
            testMatch: /.*\.setup\.js/,
        },
        {
            name: 'chromium',
            use: { ...devices['Desktop Chrome'] },
            dependencies: ['setup'],
        },
    ],
});
```

### 4. Error Handling
```javascript
test('handle network errors gracefully', async ({ page }) => {
    // Set up network failure simulation
    await page.route('**/api/**', route => route.abort());
    
    await page.goto('/dashboard');
    
    // Check error state
    await expect(page.getByText('Network error')).toBeVisible();
});
```

## ⚠️ Common Pitfalls

### 1. Async/Await Confusion
```javascript
// ❌ Wrong - Missing await
test('wrong', async ({ page }) => {
    page.goto('/login'); // This returns a promise!
    page.fill('input', 'text'); // This will fail
});

// ✅ Correct - Proper async/await
test('correct', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input', 'text');
});
```

### 2. Selector Specificity
```javascript
// ❌ Fragile - Too specific
await page.locator('div.container > ul.list > li:nth-child(3) > span.text');

// ✅ Resilient - Semantic locators
await page.getByRole('listitem').filter({ hasText: 'Item 3' });
```

### 3. Race Conditions
```javascript
// ❌ Potential race condition
await page.click('button');
await page.fill('input', 'text'); // Might fail if button action is slow

// ✅ Proper waiting
await page.click('button');
await page.waitForSelector('input'); // Wait for input to appear
await page.fill('input', 'text');
```

## 🔬 Architecture Analysis

Understanding Playwright's internal architecture is crucial for effective migration and optimal usage. This section provides insights into the design decisions that make Playwright powerful and reliable.

### Why Architecture Matters for Migration

When migrating from Cypress to Playwright, understanding the architectural differences helps you:

1. **Make informed design decisions** for your test suite structure
2. **Leverage Playwright's strengths** effectively
3. **Avoid anti-patterns** that fight against the framework's design
4. **Optimize performance** by aligning with the architecture

### Core Architectural Principles

#### 1. Decoupled Client-Server Model
Playwright uses a language-agnostic Node.js server that communicates with client libraries via WebSocket. This enables:
- **Multi-language support** without reimplementing core logic
- **Consistent behavior** across all language bindings
- **Centralized updates** and bug fixes

#### 2. Native Browser Protocols
Direct communication with browsers using their debugging protocols (CDP, Firefox Remote, WebKit Debug) provides:
- **Lower latency** than WebDriver's HTTP-based approach
- **Richer functionality** through protocol extensions
- **Real-time event streaming** for robust auto-waiting

#### 3. BrowserContext Isolation
Lightweight isolation within browser processes offers:
- **Efficient parallelization** (contexts vs. processes)
- **Complete test isolation** without performance overhead
- **Multi-user testing scenarios** within single tests

#### 4. Auto-Waiting Engine
Sophisticated actionability checks before every interaction ensure:
- **Reliable test execution** without manual waits
- **Reduced flakiness** through multi-dimensional readiness validation
- **Human-like interaction patterns** that mirror real user behavior

### Migration Strategy Based on Architecture

#### From Selenium: Leverage Direct Control
- **Replace explicit waits** with Playwright's auto-waiting
- **Utilize multiple browsers** through projects configuration
- **Implement efficient parallelization** using BrowserContexts

#### From Cypress: Embrace Multi-Process Design
- **Restructure for multi-tab/window scenarios** that Cypress cannot handle
- **Implement cross-origin testing** without restrictions
- **Design for true parallel execution** across test files

### Performance Implications

Understanding the architecture helps optimize performance:

```javascript
// ❌ Inefficient - Creates new browser for each test
test.describe('Login Tests', () => {
    test('user login', async () => {
        const browser = await chromium.launch();
        const page = await browser.newPage();
        // ... test logic
        await browser.close();
    });
});

// ✅ Efficient - Uses shared browser with isolated contexts
test.describe('Login Tests', () => {
    test('user login', async ({ page }) => {
        // Playwright automatically provides isolated context
        // ... test logic
    });
});
```

### Debugging with Architecture Knowledge

Understanding the internal flow helps with debugging:

1. **Client command** → WebSocket → **Server translation** → Native protocol → **Browser execution**
2. **Event stream** ← WebSocket ← **Server aggregation** ← Native protocol ← **Browser events**

When tests fail, trace the flow:
- Is the client command correct?
- Is the WebSocket connection stable?
- Are browser events being received?
- Are actionability checks failing?

### Configuration Alignment

Align your configuration with the architecture:

```javascript
// playwright.config.js - Optimized for architecture
export default defineConfig({
    // Leverage parallel workers efficiently
    fullyParallel: true,
    workers: process.env.CI ? 2 : undefined,
    
    // Configure all browsers through projects
    projects: [
        { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
        { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
        { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    ],
    
    // Utilize built-in capabilities
    use: {
        trace: 'on-first-retry', // Leverage event stream recording
        video: 'retain-on-failure', // Use browser recording features
    },
});
```

For a comprehensive architectural deep dive, explore the **🔬 Architecture** tab in the Playwright Studies Portal, which includes:
- Interactive diagrams of the client-server model
- Communication protocol analysis
- BrowserContext performance comparisons
- Actionability check implementations
- Framework comparison matrices

## 🤖 Automation Tools

### Conversion Script Example
```javascript
// convert-cypress-to-playwright.js
const fs = require('fs');
const path = require('path');

const conversionMap = {
    'cy.get(': 'page.locator(',
    'cy.visit(': 'page.goto(',
    '.type(': '.fill(',
    '.should(\'be.visible\')': 'toBeVisible()',
    '.should(\'contain\',': '.toContainText(',
};

function convertFile(filePath) {
    let content = fs.readFileSync(filePath, 'utf8');
    
    // Apply basic conversions
    for (const [cypress, playwright] of Object.entries(conversionMap)) {
        content = content.replaceAll(cypress, playwright);
    }
    
    // Add async/await
    content = content.replace(/it\('([^']+)',\s*\(\)\s*=>\s*{/g, 
        "test('$1', async ({ page }) => {");
    
    // Add expect imports
    if (content.includes('toBeVisible') || content.includes('toContainText')) {
        content = "import { test, expect } from '@playwright/test';\n\n" + content;
    }
    
    return content;
}
```

### Migration Checklist
- [ ] **Environment Setup**
  - [ ] Install Playwright
  - [ ] Configure browsers
  - [ ] Set up CI/CD
- [ ] **Code Conversion**
  - [ ] Convert test structure
  - [ ] Update selectors
  - [ ] Fix assertions
  - [ ] Add async/await
- [ ] **Advanced Features**
  - [ ] Implement Page Objects
  - [ ] Set up fixtures
  - [ ] Configure parallel execution
  - [ ] Add reporting
- [ ] **Quality Assurance**
  - [ ] Run all tests
  - [ ] Check coverage
  - [ ] Performance testing
  - [ ] Documentation update

## 📚 Resources

### Official Documentation
- [Playwright Documentation](https://playwright.dev/)
- [Migration Guide](https://playwright.dev/docs/migration)
- [Best Practices](https://playwright.dev/docs/best-practices)

### Community Resources
- [Playwright GitHub](https://github.com/microsoft/playwright)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/playwright)
- [Discord Community](https://discord.com/invite/playwright)

### Tools and Extensions
- [Playwright VSCode Extension](https://marketplace.visualstudio.com/items?itemName=ms-playwright.playwright)
- [Playwright Test Generator](https://playwright.dev/docs/codegen)
- [Playwright Inspector](https://playwright.dev/docs/inspector)

---

This methodology has been implemented in the **Playwright Studies Portal** to provide a comprehensive learning experience for teams migrating from Cypress to Playwright. The portal includes interactive examples, hands-on exercises, and AI-powered assistance to ensure successful migration.
