"""
OOP Principles in Test Automation
=================================

Comprehensive guide on applying Object-Oriented Programming principles in test automation.
"""

# Encapsulation in Test Design
ENCAPSULATION = {
    "principle": "Encapsulation hides internal details and exposes only necessary interfaces",
    "example": """
class LoginForm {
    constructor(page) {
        this.page = page;
        // Private selectors (encapsulated)
        this._usernameField = page.getByTestId('username');
        this._passwordField = page.getByTestId('password');
        this._submitButton = page.getByTestId('login-submit');
        this._errorMessage = page.locator('.error-message');
    }

    // Public interface methods
    async login(username, password) {
        await this._fillUsername(username);
        await this._fillPassword(password);
        await this._submit();
    }

    async getErrorMessage() {
        return await this._errorMessage.textContent();
    }

    // Private helper methods (encapsulated)
    async _fillUsername(username) {
        await this._usernameField.fill(username);
    }

    async _fillPassword(password) {
        await this._passwordField.fill(password);
    }

    async _submit() {
        await this._submitButton.click();
    }
}
""",
    "benefits": [
        "Hides implementation details",
        "Provides clean public interface",
        "Reduces coupling between components",
        "Makes code easier to maintain",
        "Prevents direct manipulation of internal state"
    ]
}

# Inheritance for Test Base Classes
INHERITANCE = {
    "principle": "Inheritance allows sharing common functionality across related classes",
    "example": """
// Base test class with common functionality
class BaseTest {
    constructor(page) {
        this.page = page;
    }

    async setup() {
        await this.page.goto('/');
        await this.page.waitForLoadState('networkidle');
    }

    async takeScreenshot(name) {
        await this.page.screenshot({ 
            path: `screenshots/${name}-${Date.now()}.png` 
        });
    }

    async handleErrors() {
        this.page.on('pageerror', (error) => {
            console.error('Page error:', error.message);
        });
    }

    async cleanup() {
        await this.page.close();
    }
}

// Specific test class inheriting from base
class AuthenticationTest extends BaseTest {
    constructor(page) {
        super(page);
        this.loginPage = new LoginPage(page);
        this.dashboardPage = new DashboardPage(page);
    }

    async testValidLogin() {
        await this.setup();
        await this.loginPage.login('valid@email.com', 'password');
        await expect(this.dashboardPage.welcomeMessage).toBeVisible();
        await this.takeScreenshot('valid-login');
    }

    async testInvalidLogin() {
        await this.setup();
        await this.loginPage.login('invalid@email.com', 'wrong');
        await expect(this.loginPage.errorMessage).toBeVisible();
        await this.takeScreenshot('invalid-login');
    }
}

// E-commerce specific test class
class EcommerceTest extends BaseTest {
    constructor(page) {
        super(page);
        this.productPage = new ProductPage(page);
        this.cartPage = new CartPage(page);
    }

    async testAddToCart() {
        await this.setup();
        await this.productPage.addToCart();
        await expect(this.cartPage.itemCount).toHaveText('1');
    }
}
""",
    "benefits": [
        "Code reusability across test classes",
        "Consistent setup and teardown",
        "Shared utility methods",
        "Easier maintenance of common functionality",
        "Hierarchical organization of test types"
    ]
}

# Polymorphism in Test Frameworks
POLYMORPHISM = {
    "principle": "Polymorphism allows objects of different types to be treated uniformly",
    "example": """
// Interface for different page types
class PageInterface {
    async navigate() {
        throw new Error('navigate() must be implemented');
    }

    async isLoaded() {
        throw new Error('isLoaded() must be implemented');
    }

    async getTitle() {
        throw new Error('getTitle() must be implemented');
    }
}

// Different page implementations
class HomePage extends PageInterface {
    constructor(page) {
        super();
        this.page = page;
        this.heroSection = page.locator('.hero');
    }

    async navigate() {
        await this.page.goto('/');
    }

    async isLoaded() {
        return await this.heroSection.isVisible();
    }

    async getTitle() {
        return await this.page.title();
    }
}

class ProductListPage extends PageInterface {
    constructor(page) {
        super();
        this.page = page;
        this.productGrid = page.locator('.product-grid');
    }

    async navigate() {
        await this.page.goto('/products');
    }

    async isLoaded() {
        return await this.productGrid.isVisible();
    }

    async getTitle() {
        return await this.page.locator('h1').textContent();
    }
}

// Polymorphic usage
class PageNavigator {
    async testPageLoad(pageObject) {
        await pageObject.navigate();
        const isLoaded = await pageObject.isLoaded();
        const title = await pageObject.getTitle();
        
        expect(isLoaded).toBe(true);
        expect(title).toBeTruthy();
    }
}

// Usage with different page types
const navigator = new PageNavigator();
await navigator.testPageLoad(new HomePage(page));
await navigator.testPageLoad(new ProductListPage(page));
""",
    "benefits": [
        "Uniform interface for different implementations",
        "Flexible and extensible code",
        "Easier to add new page types",
        "Consistent behavior across different objects",
        "Simplified test logic"
    ]
}

# Abstraction for Page Objects
ABSTRACTION = {
    "principle": "Abstraction focuses on essential features while hiding complex implementation",
    "example": """
// Abstract base for form interactions
class AbstractForm {
    constructor(page) {
        this.page = page;
        this.fields = new Map();
        this.buttons = new Map();
    }

    // Abstract methods to be implemented by subclasses
    defineFields() {
        throw new Error('defineFields() must be implemented');
    }

    defineButtons() {
        throw new Error('defineButtons() must be implemented');
    }

    // Concrete methods using abstraction
    async fillField(fieldName, value) {
        if (!this.fields.has(fieldName)) {
            throw new Error(`Field '${fieldName}' not defined`);
        }
        const field = this.fields.get(fieldName);
        await field.fill(value);
    }

    async clickButton(buttonName) {
        if (!this.buttons.has(buttonName)) {
            throw new Error(`Button '${buttonName}' not defined`);
        }
        const button = this.buttons.get(buttonName);
        await button.click();
    }

    async submitForm(formData) {
        for (const [fieldName, value] of Object.entries(formData)) {
            await this.fillField(fieldName, value);
        }
        await this.clickButton('submit');
    }
}

// Concrete implementation
class ContactForm extends AbstractForm {
    constructor(page) {
        super(page);
        this.defineFields();
        this.defineButtons();
    }

    defineFields() {
        this.fields.set('name', this.page.getByTestId('contact-name'));
        this.fields.set('email', this.page.getByTestId('contact-email'));
        this.fields.set('message', this.page.getByTestId('contact-message'));
    }

    defineButtons() {
        this.buttons.set('submit', this.page.getByTestId('contact-submit'));
        this.buttons.set('reset', this.page.getByTestId('contact-reset'));
    }
}

// Usage
const contactForm = new ContactForm(page);
await contactForm.submitForm({
    name: 'John Doe',
    email: 'john@example.com',
    message: 'Hello there!'
});
""",
    "benefits": [
        "Simplified interface for complex operations",
        "Focuses on what rather than how",
        "Reduces cognitive load",
        "Promotes code reusability",
        "Easier to understand and maintain"
    ]
}

# Design Patterns in Test Automation
DESIGN_PATTERNS = {
    "builder_pattern": """
// Builder pattern for test data creation
class UserBuilder {
    constructor() {
        this.user = {
            name: 'Default User',
            email: 'default@example.com',
            role: 'user',
            active: true
        };
    }

    withName(name) {
        this.user.name = name;
        return this;
    }

    withEmail(email) {
        this.user.email = email;
        return this;
    }

    withRole(role) {
        this.user.role = role;
        return this;
    }

    inactive() {
        this.user.active = false;
        return this;
    }

    build() {
        return { ...this.user };
    }
}

// Usage
const adminUser = new UserBuilder()
    .withName('Admin User')
    .withEmail('admin@example.com')
    .withRole('admin')
    .build();
""",
    "factory_pattern": """
// Factory pattern for creating different page objects
class PageFactory {
    static createPage(pageType, page) {
        switch (pageType) {
            case 'login':
                return new LoginPage(page);
            case 'dashboard':
                return new DashboardPage(page);
            case 'product':
                return new ProductPage(page);
            default:
                throw new Error(`Unknown page type: ${pageType}`);
        }
    }
}

// Usage
const loginPage = PageFactory.createPage('login', page);
const dashboardPage = PageFactory.createPage('dashboard', page);
"""
}

def get_oop_guide():
    """Get the complete OOP principles guide"""
    return {
        "encapsulation": ENCAPSULATION,
        "inheritance": INHERITANCE,
        "polymorphism": POLYMORPHISM,
        "abstraction": ABSTRACTION,
        "design_patterns": DESIGN_PATTERNS
    }
