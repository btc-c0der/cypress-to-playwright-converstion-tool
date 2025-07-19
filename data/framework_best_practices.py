"""
Test Automation Framework Best Practices
========================================

Comprehensive guide covering best practices for building robust test automation frameworks.
"""

# Framework Architecture Patterns
ARCHITECTURE_PATTERNS = {
    "layered_architecture": """
// Layered Architecture Pattern
// Layer 1: Test Layer (High-level business scenarios)
class UserJourneyTests {
    constructor() {
        this.userService = new UserService();
        this.orderService = new OrderService();
    }

    async testCompleteUserJourney() {
        const user = await this.userService.createAndLoginUser();
        const product = await this.orderService.addProductToCart();
        const order = await this.orderService.completeCheckout();
        
        expect(order.status).toBe('confirmed');
    }
}

// Layer 2: Service Layer (Business logic abstraction)
class UserService {
    constructor() {
        this.loginPage = new LoginPage();
        this.registrationPage = new RegistrationPage();
    }

    async createAndLoginUser(userData = {}) {
        const user = TestDataBuilder.createUser(userData);
        await this.registrationPage.register(user);
        await this.loginPage.login(user.email, user.password);
        return user;
    }
}

// Layer 3: Page Object Layer (UI abstraction)
class LoginPage {
    constructor(page) {
        this.page = page;
        this.emailField = page.getByTestId('email');
        this.passwordField = page.getByTestId('password');
        this.loginButton = page.getByTestId('login-button');
    }

    async login(email, password) {
        await this.emailField.fill(email);
        await this.passwordField.fill(password);
        await this.loginButton.click();
    }
}

// Layer 4: Driver Layer (Browser/API interactions)
class WebDriverManager {
    static async createBrowser(browserType = 'chromium') {
        const browser = await playwright[browserType].launch();
        return browser;
    }
}
""",
    "benefits": [
        "Clear separation of concerns",
        "Easy to maintain and update",
        "Reusable components across layers",
        "Testable in isolation",
        "Scalable architecture"
    ]
}

# Configuration Management
CONFIGURATION_MANAGEMENT = {
    "environment_configs": """
// Environment-specific configurations
class EnvironmentConfig {
    constructor(environment = 'dev') {
        this.environment = environment;
        this.config = this.loadConfig();
    }

    loadConfig() {
        const configs = {
            dev: {
                baseUrl: 'https://dev.example.com',
                apiUrl: 'https://api-dev.example.com',
                timeout: 30000,
                retries: 1,
                browsers: ['chromium'],
                parallel: false
            },
            staging: {
                baseUrl: 'https://staging.example.com',
                apiUrl: 'https://api-staging.example.com',
                timeout: 60000,
                retries: 2,
                browsers: ['chromium', 'firefox'],
                parallel: true
            },
            production: {
                baseUrl: 'https://example.com',
                apiUrl: 'https://api.example.com',
                timeout: 90000,
                retries: 3,
                browsers: ['chromium', 'firefox', 'webkit'],
                parallel: true
            }
        };

        return configs[this.environment] || configs.dev;
    }

    get baseUrl() { return this.config.baseUrl; }
    get apiUrl() { return this.config.apiUrl; }
    get timeout() { return this.config.timeout; }
    get retries() { return this.config.retries; }
    get browsers() { return this.config.browsers; }
    get parallel() { return this.config.parallel; }
}

// Usage
const config = new EnvironmentConfig(process.env.TEST_ENV || 'dev');
""",
    "test_data_management": """
// Test Data Factory Pattern
class TestDataFactory {
    static createUser(overrides = {}) {
        const baseUser = {
            firstName: faker.person.firstName(),
            lastName: faker.person.lastName(),
            email: faker.internet.email(),
            password: 'Test123!',
            role: 'user',
            active: true,
            ...overrides
        };
        
        return baseUser;
    }

    static createProduct(overrides = {}) {
        return {
            name: faker.commerce.productName(),
            price: faker.commerce.price(),
            description: faker.commerce.productDescription(),
            category: faker.commerce.department(),
            inStock: true,
            ...overrides
        };
    }

    static createOrder(userOverrides = {}, productOverrides = {}) {
        const user = this.createUser(userOverrides);
        const product = this.createProduct(productOverrides);
        
        return {
            user,
            items: [{ product, quantity: 1 }],
            total: product.price,
            status: 'pending'
        };
    }
}
"""
}

# Error Handling and Recovery
ERROR_HANDLING = {
    "retry_mechanisms": """
// Comprehensive retry and recovery strategies
class RetryHandler {
    static async withRetry(operation, options = {}) {
        const {
            maxRetries = 3,
            delay = 1000,
            backoff = 2,
            condition = () => true
        } = options;

        let lastError;
        
        for (let attempt = 0; attempt <= maxRetries; attempt++) {
            try {
                return await operation();
            } catch (error) {
                lastError = error;
                
                if (attempt === maxRetries || !condition(error)) {
                    throw error;
                }
                
                const waitTime = delay * Math.pow(backoff, attempt);
                await this.sleep(waitTime);
                
                console.log(`Retry ${attempt + 1}/${maxRetries} after ${waitTime}ms`);
            }
        }
        
        throw lastError;
    }

    static async sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Usage examples
class RobustPageObject {
    async clickWithRetry(selector, options = {}) {
        return RetryHandler.withRetry(
            async () => {
                await this.page.click(selector);
            },
            {
                maxRetries: 3,
                condition: (error) => error.message.includes('Element not found')
            }
        );
    }

    async waitForElementWithRetry(selector, options = {}) {
        return RetryHandler.withRetry(
            async () => {
                return await this.page.waitForSelector(selector, { timeout: 5000 });
            },
            {
                maxRetries: 3,
                delay: 2000
            }
        );
    }
}
""",
    "graceful_degradation": """
// Graceful degradation strategies
class GracefulTestExecution {
    async executeTestWithFallback(primaryTest, fallbackTest) {
        try {
            return await primaryTest();
        } catch (error) {
            console.warn('Primary test failed, attempting fallback:', error.message);
            return await fallbackTest();
        }
    }

    async verifyElementWithFallback(primarySelector, fallbackSelector) {
        try {
            return await this.page.waitForSelector(primarySelector, { timeout: 5000 });
        } catch (error) {
            console.warn(`Primary selector failed: ${primarySelector}, trying fallback: ${fallbackSelector}`);
            return await this.page.waitForSelector(fallbackSelector, { timeout: 10000 });
        }
    }
}
"""
}

# Reporting and Analytics
REPORTING_ANALYTICS = {
    "custom_reporter": """
// Custom test reporter with analytics
class AdvancedTestReporter {
    constructor() {
        this.testResults = [];
        this.startTime = Date.now();
    }

    onTestBegin(test) {
        test.startTime = Date.now();
        console.log(`Starting test: ${test.title}`);
    }

    onTestEnd(test, result) {
        const endTime = Date.now();
        const duration = endTime - test.startTime;
        
        const testResult = {
            title: test.title,
            status: result.status,
            duration,
            error: result.error?.message,
            retries: result.retry,
            tags: test.tags,
            timestamp: new Date().toISOString()
        };
        
        this.testResults.push(testResult);
        
        if (result.status === 'failed') {
            this.captureFailureContext(test, result);
        }
    }

    async captureFailureContext(test, result) {
        try {
            // Capture screenshot
            await test.page?.screenshot({
                path: `screenshots/failure-${test.title}-${Date.now()}.png`
            });
            
            // Capture page HTML
            const html = await test.page?.content();
            if (html) {
                fs.writeFileSync(`logs/failure-${test.title}-${Date.now()}.html`, html);
            }
            
            // Capture console logs
            const logs = test.page?.context()?.pages()[0]?.consoleLogs || [];
            console.log('Console logs at failure:', logs);
            
        } catch (error) {
            console.error('Failed to capture failure context:', error);
        }
    }

    onEnd() {
        const endTime = Date.now();
        const totalDuration = endTime - this.startTime;
        
        const summary = this.generateSummary(totalDuration);
        this.saveReport(summary);
        this.sendAnalytics(summary);
    }

    generateSummary(totalDuration) {
        const passed = this.testResults.filter(t => t.status === 'passed').length;
        const failed = this.testResults.filter(t => t.status === 'failed').length;
        const skipped = this.testResults.filter(t => t.status === 'skipped').length;
        
        return {
            total: this.testResults.length,
            passed,
            failed,
            skipped,
            passRate: ((passed / this.testResults.length) * 100).toFixed(2),
            totalDuration,
            averageDuration: (totalDuration / this.testResults.length).toFixed(2),
            results: this.testResults
        };
    }
}
""",
    "performance_monitoring": """
// Performance monitoring integration
class PerformanceMonitor {
    static async measurePageLoad(page, url) {
        const startTime = Date.now();
        
        await page.goto(url);
        await page.waitForLoadState('networkidle');
        
        const endTime = Date.now();
        const loadTime = endTime - startTime;
        
        // Get performance metrics
        const metrics = await page.evaluate(() => {
            const navigation = performance.getEntriesByType('navigation')[0];
            return {
                domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
                loadComplete: navigation.loadEventEnd - navigation.loadEventStart,
                firstPaint: performance.getEntriesByName('first-paint')[0]?.startTime,
                firstContentfulPaint: performance.getEntriesByName('first-contentful-paint')[0]?.startTime
            };
        });
        
        return {
            totalLoadTime: loadTime,
            ...metrics
        };
    }

    static async monitorResourceLoading(page) {
        const resources = [];
        
        page.on('response', (response) => {
            resources.push({
                url: response.url(),
                status: response.status(),
                contentType: response.headers()['content-type'],
                size: response.headers()['content-length']
            });
        });
        
        return resources;
    }
}
"""
}

# Maintenance and Scalability
MAINTENANCE_SCALABILITY = {
    "code_organization": """
// Modular framework organization
src/
├── pages/
│   ├── base/
│   │   ├── BasePage.js
│   │   └── BaseComponent.js
│   ├── auth/
│   │   ├── LoginPage.js
│   │   └── RegistrationPage.js
│   └── shop/
│       ├── ProductPage.js
│       └── CartPage.js
├── services/
│   ├── ApiService.js
│   ├── DatabaseService.js
│   └── EmailService.js
├── utils/
│   ├── TestDataFactory.js
│   ├── RetryHandler.js
│   └── PerformanceMonitor.js
├── config/
│   ├── EnvironmentConfig.js
│   └── BrowserConfig.js
└── tests/
    ├── api/
    ├── e2e/
    └── integration/
""",
    "version_control": """
// Framework versioning and changelog management
class FrameworkVersion {
    static getCurrentVersion() {
        return require('../package.json').version;
    }

    static logFrameworkInfo() {
        const version = this.getCurrentVersion();
        const nodeVersion = process.version;
        const playwrightVersion = require('@playwright/test/package.json').version;
        
        console.log(`
Framework Version: ${version}
Node.js Version: ${nodeVersion}
Playwright Version: ${playwrightVersion}
Environment: ${process.env.NODE_ENV || 'development'}
        `);
    }
}
"""
}

def get_framework_best_practices():
    """Get the complete framework best practices guide"""
    return {
        "architecture_patterns": ARCHITECTURE_PATTERNS,
        "configuration_management": CONFIGURATION_MANAGEMENT,
        "error_handling": ERROR_HANDLING,
        "reporting_analytics": REPORTING_ANALYTICS,
        "maintenance_scalability": MAINTENANCE_SCALABILITY
    }
