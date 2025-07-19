"""
SOLID Principles Applied to Test Automation
===========================================

Comprehensive guide on applying SOLID principles to create maintainable test automation frameworks.
"""

# Single Responsibility Principle (SRP)
SINGLE_RESPONSIBILITY = {
    "principle": "A class should have one, and only one, reason to change",
    "bad_example": """
// BAD: Class with multiple responsibilities
class UserTestPage {
    constructor(page) {
        this.page = page;
    }

    // User interaction responsibility
    async login(username, password) {
        await this.page.fill('#username', username);
        await this.page.fill('#password', password);
        await this.page.click('#login-button');
    }

    // Database responsibility
    async createUserInDB(userData) {
        // Database logic here
    }

    // API responsibility
    async getUserFromAPI(userId) {
        // API logic here
    }

    // Validation responsibility
    async validateEmail(email) {
        // Email validation logic here
    }

    // Reporting responsibility
    async generateTestReport() {
        // Report generation logic here
    }
}
""",
    "good_example": """
// GOOD: Separate classes with single responsibilities

// Responsible only for user page interactions
class UserPage {
    constructor(page) {
        this.page = page;
        this.usernameField = page.locator('#username');
        this.passwordField = page.locator('#password');
        this.loginButton = page.locator('#login-button');
    }

    async login(username, password) {
        await this.usernameField.fill(username);
        await this.passwordField.fill(password);
        await this.loginButton.click();
    }
}

// Responsible only for database operations
class UserRepository {
    constructor(dbConnection) {
        this.db = dbConnection;
    }

    async createUser(userData) {
        return await this.db.users.create(userData);
    }

    async getUserById(userId) {
        return await this.db.users.findById(userId);
    }
}

// Responsible only for API operations
class UserAPIClient {
    constructor(baseURL) {
        this.baseURL = baseURL;
    }

    async getUser(userId) {
        const response = await fetch(`${this.baseURL}/users/${userId}`);
        return response.json();
    }
}

// Responsible only for validation
class UserValidator {
    static validateEmail(email) {
        const emailRegex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;
        return emailRegex.test(email);
    }

    static validatePassword(password) {
        return password.length >= 8;
    }
}
""",
    "benefits": [
        "Easier to understand and maintain",
        "Changes to one responsibility don't affect others",
        "Better testability",
        "Improved reusability",
        "Clearer code organization"
    ]
}

# Open/Closed Principle (OCP)
OPEN_CLOSED = {
    "principle": "Software entities should be open for extension but closed for modification",
    "bad_example": """
// BAD: Modifying existing class for new functionality
class TestReporter {
    constructor(type) {
        this.type = type;
    }

    generateReport(testResults) {
        if (this.type === 'html') {
            return this.generateHTMLReport(testResults);
        } else if (this.type === 'json') {
            return this.generateJSONReport(testResults);
        } else if (this.type === 'xml') {  // New requirement - modifying existing code
            return this.generateXMLReport(testResults);
        }
    }

    generateHTMLReport(results) {
        // HTML report logic
    }

    generateJSONReport(results) {
        // JSON report logic
    }

    generateXMLReport(results) {  // Adding new method to existing class
        // XML report logic
    }
}
""",
    "good_example": """
// GOOD: Using abstraction and extension

// Abstract base class (closed for modification)
class ReportGenerator {
    async generateReport(testResults) {
        throw new Error('generateReport must be implemented');
    }
}

// Concrete implementations (extensions)
class HTMLReportGenerator extends ReportGenerator {
    async generateReport(testResults) {
        return this.createHTMLReport(testResults);
    }

    createHTMLReport(results) {
        // HTML-specific logic
        return `<html><body>${JSON.stringify(results)}</body></html>`;
    }
}

class JSONReportGenerator extends ReportGenerator {
    async generateReport(testResults) {
        return JSON.stringify(testResults, null, 2);
    }
}

// New requirement - extend without modifying existing code
class XMLReportGenerator extends ReportGenerator {
    async generateReport(testResults) {
        return this.createXMLReport(testResults);
    }

    createXMLReport(results) {
        // XML-specific logic
        return `<report>${JSON.stringify(results)}</report>`;
    }
}

// Factory to manage different generators
class ReportFactory {
    static createGenerator(type) {
        switch (type) {
            case 'html':
                return new HTMLReportGenerator();
            case 'json':
                return new JSONReportGenerator();
            case 'xml':
                return new XMLReportGenerator();
            default:
                throw new Error(`Unknown report type: ${type}`);
        }
    }
}
""",
    "benefits": [
        "New functionality added without breaking existing code",
        "Easier to add new features",
        "Reduced risk of introducing bugs",
        "Better code stability",
        "Supports polymorphism"
    ]
}

# Liskov Substitution Principle (LSP)
LISKOV_SUBSTITUTION = {
    "principle": "Objects of a superclass should be replaceable with objects of a subclass without breaking functionality",
    "bad_example": """
// BAD: Subclass changes expected behavior
class BasePage {
    constructor(page) {
        this.page = page;
    }

    async navigate(url) {
        await this.page.goto(url);
        await this.waitForLoad();
    }

    async waitForLoad() {
        await this.page.waitForLoadState('networkidle');
    }
}

class LoginPage extends BasePage {
    async navigate(url) {
        // Breaking LSP: Changes expected behavior
        if (!url.includes('/login')) {
            throw new Error('LoginPage can only navigate to login URLs');
        }
        await super.navigate(url);
    }

    async waitForLoad() {
        // Breaking LSP: Different waiting strategy that might fail
        await this.page.waitForTimeout(5000); // Fixed timeout instead of network idle
    }
}
""",
    "good_example": """
// GOOD: Subclasses maintain expected behavior
class BasePage {
    constructor(page) {
        this.page = page;
    }

    async navigate(url) {
        await this.page.goto(url);
        await this.waitForLoad();
    }

    async waitForLoad() {
        await this.page.waitForLoadState('networkidle');
    }

    async isLoaded() {
        return true; // Default implementation
    }
}

class LoginPage extends BasePage {
    constructor(page) {
        super(page);
        this.loginForm = page.locator('.login-form');
    }

    async waitForLoad() {
        // Extends behavior while maintaining contract
        await super.waitForLoad();
        await expect(this.loginForm).toBeVisible();
    }

    async isLoaded() {
        // Specific implementation that maintains contract
        return await this.loginForm.isVisible();
    }

    async login(username, password) {
        // Additional functionality specific to LoginPage
        await this.page.fill('#username', username);
        await this.page.fill('#password', password);
        await this.page.click('#login-button');
    }
}

class DashboardPage extends BasePage {
    constructor(page) {
        super(page);
        this.dashboardContent = page.locator('.dashboard');
    }

    async waitForLoad() {
        await super.waitForLoad();
        await expect(this.dashboardContent).toBeVisible();
    }

    async isLoaded() {
        return await this.dashboardContent.isVisible();
    }
}

// Both subclasses can be used interchangeably
async function testPageNavigation(pageObject, url) {
    await pageObject.navigate(url);
    const loaded = await pageObject.isLoaded();
    expect(loaded).toBe(true);
}

// Works with any BasePage subclass
await testPageNavigation(new LoginPage(page), '/login');
await testPageNavigation(new DashboardPage(page), '/dashboard');
""",
    "benefits": [
        "Predictable behavior across inheritance hierarchy",
        "Interchangeable objects",
        "Reliable polymorphism",
        "Easier testing and debugging",
        "Consistent API contracts"
    ]
}

# Interface Segregation Principle (ISP)
INTERFACE_SEGREGATION = {
    "principle": "No client should be forced to depend on methods it does not use",
    "bad_example": """
// BAD: Fat interface with methods not needed by all implementations
class PageInterface {
    async navigate(url) {}
    async login(username, password) {}
    async logout() {}
    async search(query) {}
    async addToCart(productId) {}
    async checkout() {}
    async submitForm(data) {}
    async uploadFile(filePath) {}
    async downloadFile(fileName) {}
}

// HomePage doesn't need login, cart, or file operations
class HomePage extends PageInterface {
    async navigate(url) {
        await this.page.goto(url);
    }

    // Forced to implement methods it doesn't need
    async login(username, password) {
        throw new Error('HomePage does not support login');
    }

    async addToCart(productId) {
        throw new Error('HomePage does not support cart operations');
    }

    async uploadFile(filePath) {
        throw new Error('HomePage does not support file upload');
    }
    // ... other unnecessary methods
}
""",
    "good_example": """
// GOOD: Segregated interfaces for specific capabilities

// Basic navigation interface
class Navigatable {
    async navigate(url) {
        throw new Error('navigate must be implemented');
    }

    async isLoaded() {
        throw new Error('isLoaded must be implemented');
    }
}

// Authentication interface
class Authenticatable {
    async login(username, password) {
        throw new Error('login must be implemented');
    }

    async logout() {
        throw new Error('logout must be implemented');
    }
}

// Search interface
class Searchable {
    async search(query) {
        throw new Error('search must be implemented');
    }

    async getSearchResults() {
        throw new Error('getSearchResults must be implemented');
    }
}

// Shopping interface
class Shoppable {
    async addToCart(productId) {
        throw new Error('addToCart must be implemented');
    }

    async removeFromCart(productId) {
        throw new Error('removeFromCart must be implemented');
    }
}

// File operations interface
class FileOperatable {
    async uploadFile(filePath) {
        throw new Error('uploadFile must be implemented');
    }

    async downloadFile(fileName) {
        throw new Error('downloadFile must be implemented');
    }
}

// Implementations only implement needed interfaces
class HomePage extends Navigatable {
    constructor(page) {
        super();
        this.page = page;
    }

    async navigate(url) {
        await this.page.goto(url);
    }

    async isLoaded() {
        return await this.page.locator('.hero-section').isVisible();
    }
}

class LoginPage extends Navigatable {
    constructor(page) {
        super();
        this.page = page;
    }

    async navigate(url) {
        await this.page.goto(url);
    }

    async isLoaded() {
        return await this.page.locator('.login-form').isVisible();
    }

    async login(username, password) {
        await this.page.fill('#username', username);
        await this.page.fill('#password', password);
        await this.page.click('#login-button');
    }
}

class ProductPage extends Navigatable {
    constructor(page) {
        super();
        this.page = page;
    }

    async navigate(url) {
        await this.page.goto(url);
    }

    async isLoaded() {
        return await this.page.locator('.product-details').isVisible();
    }

    async addToCart(productId) {
        await this.page.click(`[data-product-id="${productId}"] .add-to-cart`);
    }
}
""",
    "benefits": [
        "Classes implement only needed functionality",
        "Reduces coupling between components",
        "Easier to understand and maintain",
        "Better testability",
        "More flexible design"
    ]
}

# Dependency Inversion Principle (DIP)
DEPENDENCY_INVERSION = {
    "principle": "High-level modules should not depend on low-level modules. Both should depend on abstractions",
    "bad_example": """
// BAD: High-level class depends on concrete implementations
class TestRunner {
    constructor() {
        // Direct dependencies on concrete classes
        this.database = new MySQLDatabase();
        this.emailService = new GmailService();
        this.reportGenerator = new HTMLReportGenerator();
    }

    async runTests(testSuite) {
        const results = await this.executeTests(testSuite);
        
        // Tightly coupled to specific implementations
        await this.database.saveResults(results);
        await this.emailService.sendReport(results);
        const report = await this.reportGenerator.generate(results);
        
        return report;
    }
}
""",
    "good_example": """
// GOOD: Depends on abstractions, not concrete implementations

// Abstractions (interfaces)
class DatabaseInterface {
    async saveResults(results) {
        throw new Error('saveResults must be implemented');
    }
}

class EmailServiceInterface {
    async sendReport(results) {
        throw new Error('sendReport must be implemented');
    }
}

class ReportGeneratorInterface {
    async generate(results) {
        throw new Error('generate must be implemented');
    }
}

// Concrete implementations
class MySQLDatabase extends DatabaseInterface {
    async saveResults(results) {
        // MySQL-specific implementation
        console.log('Saving to MySQL:', results);
    }
}

class PostgreSQLDatabase extends DatabaseInterface {
    async saveResults(results) {
        // PostgreSQL-specific implementation
        console.log('Saving to PostgreSQL:', results);
    }
}

class GmailService extends EmailServiceInterface {
    async sendReport(results) {
        // Gmail-specific implementation
        console.log('Sending via Gmail:', results);
    }
}

class SlackService extends EmailServiceInterface {
    async sendReport(results) {
        // Slack-specific implementation
        console.log('Sending via Slack:', results);
    }
}

// High-level module depends on abstractions
class TestRunner {
    constructor(database, emailService, reportGenerator) {
        // Dependency injection - depends on abstractions
        this.database = database;
        this.emailService = emailService;
        this.reportGenerator = reportGenerator;
    }

    async runTests(testSuite) {
        const results = await this.executeTests(testSuite);
        
        // Uses abstractions - can work with any implementation
        await this.database.saveResults(results);
        await this.emailService.sendReport(results);
        const report = await this.reportGenerator.generate(results);
        
        return report;
    }

    async executeTests(testSuite) {
        // Test execution logic
        return { passed: 10, failed: 2, total: 12 };
    }
}

// Dependency injection container
class DIContainer {
    static createTestRunner(config) {
        const database = config.database === 'mysql' 
            ? new MySQLDatabase() 
            : new PostgreSQLDatabase();
            
        const emailService = config.notification === 'gmail'
            ? new GmailService()
            : new SlackService();
            
        const reportGenerator = new HTMLReportGenerator();
        
        return new TestRunner(database, emailService, reportGenerator);
    }
}

// Usage - easy to change implementations
const testRunner = DIContainer.createTestRunner({
    database: 'postgresql',
    notification: 'slack'
});
""",
    "benefits": [
        "Loose coupling between components",
        "Easy to swap implementations",
        "Better testability with mocks",
        "More flexible and extensible design",
        "Follows inversion of control pattern"
    ]
}

def get_solid_guide():
    """Get the complete SOLID principles guide"""
    return {
        "single_responsibility": SINGLE_RESPONSIBILITY,
        "open_closed": OPEN_CLOSED,
        "liskov_substitution": LISKOV_SUBSTITUTION,
        "interface_segregation": INTERFACE_SEGREGATION,
        "dependency_inversion": DEPENDENCY_INVERSION
    }
