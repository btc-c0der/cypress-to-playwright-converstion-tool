"""
Playwright Best Practices Guide
===============================

Comprehensive guide covering Playwright testing best practices.
"""

# Page Object Model best practices
PAGE_OBJECT_MODEL = {
    "basic_example": """
// Base Page Class
class BasePage {
    constructor(page) {
        this.page = page;
    }

    async goto(url) {
        await this.page.goto(url);
    }

    async waitForLoadState() {
        await this.page.waitForLoadState('networkidle');
    }

    async screenshot(name) {
        await this.page.screenshot({ path: `screenshots/${name}.png` });
    }
}

// Specific Page Class
class ProductPage extends BasePage {
    constructor(page) {
        super(page);
        this.addToCartButton = page.getByRole('button', { name: 'Add to Cart' });
        this.productTitle = page.locator('.product-title');
        this.productPrice = page.locator('.product-price');
        this.quantityInput = page.locator('[data-testid="quantity"]');
    }

    async addToCart(quantity = 1) {
        await this.quantityInput.fill(quantity.toString());
        await this.addToCartButton.click();
        await expect(this.page.locator('.cart-notification')).toBeVisible();
    }

    async getProductInfo() {
        return {
            title: await this.productTitle.textContent(),
            price: await this.productPrice.textContent()
        };
    }
}
""",
    "benefits": [
        "Improved code reusability",
        "Better maintenance and updates",
        "Clear separation of concerns",
        "Enhanced readability",
        "Easier debugging"
    ]
}

# Selector best practices
SELECTOR_STRATEGIES = {
    "priority_order": [
        "getByRole() - Most accessible and resilient",
        "getByTestId() - Explicit test identifiers",
        "getByLabel() - Form elements with labels",
        "getByPlaceholder() - Input placeholders",
        "getByText() - Unique text content",
        "CSS selectors - Last resort"
    ],
    "examples": """
// Good selector strategies
await page.getByRole('button', { name: 'Submit' });
await page.getByTestId('user-profile');
await page.getByLabel('Email address');
await page.getByPlaceholder('Enter your name');

// Avoid fragile selectors
await page.locator('div > div > span:nth-child(3)'); // Bad
await page.locator('#app > main > section.content'); // Bad
"""
}

# Test organization patterns
TEST_ORGANIZATION = {
    "structure": """
tests/
├── auth/
│   ├── login.spec.ts
│   ├── registration.spec.ts
│   └── password-reset.spec.ts
├── e2e/
│   ├── user-journey.spec.ts
│   └── checkout-flow.spec.ts
├── pages/
│   ├── base-page.ts
│   ├── login-page.ts
│   └── product-page.ts
├── fixtures/
│   ├── test-data.json
│   └── mock-responses.json
└── utils/
    ├── api-helpers.ts
    └── test-helpers.ts
""",
    "naming_conventions": [
        "Use descriptive test names",
        "Group related tests in describe blocks",
        "Use consistent file naming (.spec.ts)",
        "Organize by feature or user journey"
    ]
}

# Error handling and debugging
ERROR_HANDLING = {
    "retry_strategies": """
// Automatic retries
test.describe.configure({ retries: 2 });

// Custom retry logic
async function retryAction(action, maxRetries = 3) {
    for (let i = 0; i < maxRetries; i++) {
        try {
            await action();
            return;
        } catch (error) {
            if (i === maxRetries - 1) throw error;
            await page.waitForTimeout(1000);
        }
    }
}
""",
    "debugging_tools": [
        "page.pause() - Interactive debugging",
        "Trace viewer for failed tests",
        "Screenshots on failure",
        "Video recording",
        "Console logs capture"
    ]
}

# Parallel execution best practices
PARALLEL_EXECUTION = {
    "configuration": """
// playwright.config.js
export default defineConfig({
    fullyParallel: true,
    workers: process.env.CI ? 2 : 4,
    
    // Test isolation
    use: {
        trace: 'on-first-retry',
        video: 'retain-on-failure',
    },
    
    // Shard tests across machines
    shard: process.env.SHARD ? {
        current: parseInt(process.env.SHARD_CURRENT),
        total: parseInt(process.env.SHARD_TOTAL)
    } : undefined,
});
""",
    "isolation_techniques": [
        "Use unique test data",
        "Clean up after each test",
        "Avoid shared global state",
        "Use test.serial() for dependent tests"
    ]
}

# CI/CD integration
CICD_INTEGRATION = {
    "github_actions": """
name: Playwright Tests
on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  test:
    timeout-minutes: 60
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with:
        node-version: lts/*
    - name: Install dependencies
      run: npm ci
    - name: Install Playwright Browsers
      run: npx playwright install --with-deps
    - name: Run Playwright tests
      run: npx playwright test
    - uses: actions/upload-artifact@v4
      if: always()
      with:
        name: playwright-report
        path: playwright-report/
        retention-days: 30
""",
    "best_practices": [
        "Run tests in CI/CD pipeline",
        "Parallel execution across environments",
        "Store test reports as artifacts",
        "Fail fast for critical issues",
        "Run different test suites for different environments"
    ]
}

def get_best_practices_guide():
    """Get the complete best practices guide"""
    return {
        "page_object_model": PAGE_OBJECT_MODEL,
        "selector_strategies": SELECTOR_STRATEGIES,
        "test_organization": TEST_ORGANIZATION,
        "error_handling": ERROR_HANDLING,
        "parallel_execution": PARALLEL_EXECUTION,
        "cicd_integration": CICD_INTEGRATION
    }
