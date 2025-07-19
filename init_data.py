"""
Data initialization script for the Playwright Studies Portal.
This script populates the database with initial study modules and code examples.
"""

import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import StudyModule, CodeExample, SessionLocal, create_tables
from data import (
    get_migration_guide,
    get_best_practices_guide,
    get_oop_guide,
    get_solid_guide,
    get_framework_best_practices
)

def initialize_study_modules():
    """Initialize study modules in the database"""
    
    db = SessionLocal()
    
    try:
        # Check if modules already exist
        existing_modules = db.query(StudyModule).count()
        if existing_modules > 0:
            print(f"Database already contains {existing_modules} modules. Skipping initialization.")
            return
        
        modules = [
            # Cypress Migration Modules
            StudyModule(
                name="Basic Syntax Conversion",
                description="Learn how to convert basic Cypress syntax to Playwright",
                category="cypress_migration",
                content="Convert cy.get() to page.locator(), cy.visit() to page.goto(), and more",
                difficulty_level="beginner",
                estimated_time=30
            ),
            StudyModule(
                name="Assertion Migration",
                description="Convert Cypress assertions to Playwright expect syntax",
                category="cypress_migration", 
                content="Learn .should() to expect() conversions and async assertion patterns",
                difficulty_level="beginner",
                estimated_time=25
            ),
            StudyModule(
                name="Configuration Migration",
                description="Migrate Cypress configuration to Playwright config",
                category="cypress_migration",
                content="Convert cypress.config.js to playwright.config.js with projects setup",
                difficulty_level="intermediate",
                estimated_time=45
            ),
            
            # Best Practices Modules
            StudyModule(
                name="Page Object Model",
                description="Implement Page Object Model pattern in Playwright",
                category="best_practices",
                content="Create maintainable page objects with proper encapsulation",
                difficulty_level="intermediate",
                estimated_time=60
            ),
            StudyModule(
                name="Selector Strategies",
                description="Master Playwright selector best practices",
                category="best_practices",
                content="Learn getByRole, getByTestId, and other resilient selector methods",
                difficulty_level="beginner",
                estimated_time=40
            ),
            StudyModule(
                name="Parallel Testing",
                description="Configure and optimize parallel test execution",
                category="best_practices",
                content="Setup parallel execution, test isolation, and CI/CD integration",
                difficulty_level="advanced",
                estimated_time=90
            ),
            
            # OOP Modules
            StudyModule(
                name="Encapsulation in Testing",
                description="Apply encapsulation principles to test automation",
                category="oop",
                content="Hide implementation details and create clean interfaces",
                difficulty_level="intermediate",
                estimated_time=50
            ),
            StudyModule(
                name="Inheritance for Test Classes",
                description="Use inheritance to share common test functionality",
                category="oop",
                content="Create base test classes and extend for specific test types",
                difficulty_level="intermediate",
                estimated_time=55
            ),
            StudyModule(
                name="Polymorphism in Frameworks",
                description="Implement polymorphic behavior in test frameworks",
                category="oop",
                content="Create flexible test frameworks using polymorphic patterns",
                difficulty_level="advanced",
                estimated_time=70
            ),
            
            # SOLID Modules
            StudyModule(
                name="Single Responsibility Principle",
                description="Apply SRP to test automation code",
                category="solid",
                content="Create classes with single, well-defined responsibilities",
                difficulty_level="intermediate",
                estimated_time=45
            ),
            StudyModule(
                name="Open/Closed Principle",
                description="Design extensible test frameworks",
                category="solid",
                content="Create frameworks open for extension, closed for modification",
                difficulty_level="advanced",
                estimated_time=60
            ),
            StudyModule(
                name="Dependency Inversion",
                description="Apply dependency inversion in test automation",
                category="solid",
                content="Depend on abstractions, not concretions in test design",
                difficulty_level="advanced",
                estimated_time=65
            ),
            
            # Framework Modules
            StudyModule(
                name="Framework Architecture",
                description="Design scalable test automation frameworks",
                category="frameworks",
                content="Learn layered architecture and modular design patterns",
                difficulty_level="advanced",
                estimated_time=120
            ),
            StudyModule(
                name="Configuration Management",
                description="Manage configurations across environments",
                category="frameworks",
                content="Environment-specific configs and test data management",
                difficulty_level="intermediate",
                estimated_time=75
            ),
            StudyModule(
                name="Error Handling & Recovery",
                description="Implement robust error handling in tests",
                category="frameworks",
                content="Retry mechanisms, graceful degradation, and failure recovery",
                difficulty_level="advanced",
                estimated_time=85
            )
        ]
        
        db.add_all(modules)
        db.commit()
        
        print(f"✅ Initialized {len(modules)} study modules")
        
    except Exception as e:
        print(f"❌ Error initializing study modules: {e}")
        db.rollback()
    finally:
        db.close()

def initialize_code_examples():
    """Initialize code examples in the database"""
    
    db = SessionLocal()
    
    try:
        # Check if examples already exist
        existing_examples = db.query(CodeExample).count()
        if existing_examples > 0:
            print(f"Database already contains {existing_examples} examples. Skipping initialization.")
            return
        
        # Get migration guide data
        migration_data = get_migration_guide()
        
        examples = []
        
        # Add syntax comparison examples
        for i, comparison in enumerate(migration_data['syntax_comparisons']):
            examples.append(CodeExample(
                title=comparison['title'],
                description=f"Migration example: {comparison['title']}",
                category="cypress_migration",
                language="javascript",
                framework="both",
                code_before=comparison['cypress_code'],
                code_after=comparison['playwright_code'],
                explanation=comparison['explanation'],
                difficulty_level="beginner"
            ))
        
        # Add Page Object Model examples
        examples.append(CodeExample(
            title="Basic Page Object Model",
            description="Simple page object implementation in Playwright",
            category="best_practices",
            language="javascript", 
            framework="playwright",
            code_before="// Without Page Object Model\ntest('login test', async ({ page }) => {\n  await page.goto('/login');\n  await page.fill('#username', 'user');\n  await page.fill('#password', 'pass');\n  await page.click('#login-btn');\n});",
            code_after="// With Page Object Model\nclass LoginPage {\n  constructor(page) {\n    this.page = page;\n    this.usernameInput = page.locator('#username');\n    this.passwordInput = page.locator('#password');\n    this.loginButton = page.locator('#login-btn');\n  }\n\n  async login(username, password) {\n    await this.usernameInput.fill(username);\n    await this.passwordInput.fill(password);\n    await this.loginButton.click();\n  }\n}\n\ntest('login test', async ({ page }) => {\n  const loginPage = new LoginPage(page);\n  await page.goto('/login');\n  await loginPage.login('user', 'pass');\n});",
            explanation="Page Object Model encapsulates page elements and interactions",
            difficulty_level="intermediate"
        ))
        
        # Add OOP example
        examples.append(CodeExample(
            title="Encapsulation Example",
            description="Demonstrating encapsulation in test automation",
            category="oop",
            language="javascript",
            framework="playwright",
            code_before="// Poor encapsulation\nclass TestPage {\n  constructor(page) {\n    this.page = page;\n    this.username = page.locator('#username');\n    this.password = page.locator('#password');\n  }\n\n  async doLogin(user, pass) {\n    await this.username.fill(user);\n    await this.password.fill(pass);\n    await this.page.click('#login');\n  }\n}",
            code_after="// Good encapsulation\nclass LoginForm {\n  constructor(page) {\n    this.page = page;\n    this._usernameField = page.locator('#username');\n    this._passwordField = page.locator('#password');\n    this._submitButton = page.locator('#login');\n  }\n\n  async login(credentials) {\n    await this._fillCredentials(credentials);\n    await this._submit();\n  }\n\n  // Private methods\n  async _fillCredentials({ username, password }) {\n    await this._usernameField.fill(username);\n    await this._passwordField.fill(password);\n  }\n\n  async _submit() {\n    await this._submitButton.click();\n  }\n}",
            explanation="Encapsulation hides internal implementation and provides clean interface",
            difficulty_level="intermediate"
        ))
        
        # Add SOLID example
        examples.append(CodeExample(
            title="Single Responsibility Principle",
            description="Applying SRP to test automation",
            category="solid",
            language="javascript",
            framework="playwright", 
            code_before="// Violates SRP - multiple responsibilities\nclass UserTestManager {\n  constructor(page) {\n    this.page = page;\n  }\n\n  async createUser(userData) {\n    // Database logic\n    await this.saveToDatabase(userData);\n  }\n\n  async loginUser(email, password) {\n    // UI interaction logic\n    await this.page.fill('#email', email);\n    await this.page.fill('#password', password);\n    await this.page.click('#login');\n  }\n\n  async validateEmail(email) {\n    // Validation logic\n    return email.includes('@');\n  }\n\n  async generateReport() {\n    // Reporting logic\n    return 'Test Report';\n  }\n}",
            code_after="// Follows SRP - single responsibility per class\nclass UserPage {\n  constructor(page) {\n    this.page = page;\n  }\n\n  async login(email, password) {\n    await this.page.fill('#email', email);\n    await this.page.fill('#password', password);\n    await this.page.click('#login');\n  }\n}\n\nclass UserRepository {\n  async createUser(userData) {\n    // Database operations only\n    return await this.database.users.create(userData);\n  }\n}\n\nclass EmailValidator {\n  static validate(email) {\n    // Validation logic only\n    return email.includes('@') && email.includes('.');\n  }\n}\n\nclass TestReporter {\n  generateReport(results) {\n    // Reporting logic only\n    return { summary: results.length, passed: results.filter(r => r.passed).length };\n  }\n}",
            explanation="Each class has a single, well-defined responsibility",
            difficulty_level="intermediate"
        ))
        
        db.add_all(examples)
        db.commit()
        
        print(f"✅ Initialized {len(examples)} code examples")
        
    except Exception as e:
        print(f"❌ Error initializing code examples: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Main initialization function"""
    print("🎭 Initializing Playwright Studies Portal database...")
    
    # Create tables
    create_tables()
    print("✅ Database tables created")
    
    # Initialize data
    initialize_study_modules()
    initialize_code_examples()
    
    print("🎉 Database initialization complete!")
    print("💡 You can now run 'python main.py' to start the portal")

if __name__ == "__main__":
    main()
