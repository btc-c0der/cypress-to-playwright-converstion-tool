#!/usr/bin/env python3
"""
Playwright Studies Portal
=========================

A comprehensive educational portal for learning Playwright test automation,
built with Gradio and SQLAlchemy, powered by the Kimi-K2-Instruct AI model.

Features:
- Cypress to Playwright migration assistance
- Best practices guidance
- OOP and SOLID principles in test automation
- Interactive AI assistant
- Progress tracking with SQLAlchemy
"""

import os
import sys
import gradio as gr
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Initialize database
try:
    from models import create_tables
    create_tables()
    print("✅ Database initialized successfully")
except Exception as e:
    print(f"⚠️ Database initialization warning: {e}")

# Import components
from components import (
    create_migration_interface,
    create_best_practices_interface,
    create_principles_interface,
    create_ai_chat_interface,
    create_architecture_interface
)

def create_main_app():
    """Create the main Gradio application with multiple tabs"""
    
    # Custom CSS for better styling
    custom_css = """
    .gradio-container {
        max-width: 1200px !important;
        margin: auto !important;
    }
    
    .tab-nav {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
    }
    
    .code-block {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 0.375rem;
        padding: 1rem;
        font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
    }
    
    .highlight-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    """
    
    with gr.Blocks(
        title="Cypress to Playwright Conversion Tool & Playwright Studies Portal",
        theme=gr.themes.Soft(),
        css=custom_css
    ) as app:
        
        # Header
        gr.Markdown("""
        # 🎭 Playwright Studies Portal
        
        **Master Playwright Test Automation with AI-Powered Learning**
        
        Learn Playwright through comprehensive guides, hands-on examples, and AI assistance.
        Built with Gradio, SQLAlchemy, and powered by Kimi-K2-Instruct.
        """, elem_classes="highlight-box")
        
        # Create tabbed interface
        with gr.Tabs():
            
            # Migration Tab
            with gr.Tab("🔄 Cypress → Playwright", id="migration"):
                gr.Markdown("""
                ### Convert your Cypress tests to Playwright
                
                Get step-by-step guidance, code conversion tools, and migration best practices.
                """)
                
                migration_interface = create_migration_interface()
            
            # Best Practices Tab
            with gr.Tab("🎯 Best Practices", id="best_practices"):
                gr.Markdown("""
                ### Learn Playwright testing best practices
                
                Explore Page Object Model, selector strategies, test organization, and more.
                """)
                
                best_practices_interface = create_best_practices_interface()
            
            # Principles Tab
            with gr.Tab("🏗️ OOP & SOLID", id="principles"):
                gr.Markdown("""
                ### Apply OOP and SOLID principles to test automation
                
                Learn how to create maintainable, scalable test frameworks using proven design principles.
                """)
                
                principles_interface = create_principles_interface()
            
            # Architecture Analysis Tab
            with gr.Tab("🔬 Architecture", id="architecture"):
                gr.Markdown("""
                ### Deep dive into Playwright's internal architecture
                
                Understand the client-server model, communication protocols, and design decisions that make Playwright powerful.
                """)
                
                architecture_interface = create_architecture_interface()
            
            # AI Assistant Tab
            with gr.Tab("🤖 AI Assistant", id="ai_chat"):
                gr.Markdown("""
                ### Get personalized help from our AI assistant
                
                Ask questions about Playwright, get code examples, and receive expert guidance.
                """)
                
                ai_interface = create_ai_chat_interface()
            
            # Resources Tab
            with gr.Tab("📚 Resources", id="resources"):
                gr.Markdown("""
                ## 📖 Additional Learning Resources
                
                ### Official Documentation
                - [Playwright Official Docs](https://playwright.dev/)
                - [Playwright API Reference](https://playwright.dev/docs/api/class-playwright)
                - [Playwright Best Practices](https://playwright.dev/docs/best-practices)
                
                ### Migration Resources
                - [Cypress vs Playwright Comparison](https://playwright.dev/docs/why-playwright)
                - [Migration Guide Examples](https://github.com/microsoft/playwright/tree/main/docs/src/migration-guides)
                
                ### Design Patterns
                - [Page Object Model](https://playwright.dev/docs/pom)
                - [Test Organization](https://playwright.dev/docs/test-runners)
                - [Fixtures and Hooks](https://playwright.dev/docs/test-fixtures)
                
                ### Community
                - [Playwright Discord](https://discord.gg/playwright-807756831384403968)
                - [GitHub Discussions](https://github.com/microsoft/playwright/discussions)
                - [Stack Overflow](https://stackoverflow.com/questions/tagged/playwright)
                
                ### Video Tutorials
                - [Playwright Official YouTube](https://www.youtube.com/@Playwrightdev)
                - [Testing with Playwright](https://testingwithplaywright.com/)
                
                ---
                
                ## 🛠️ Development Setup
                
                ### Quick Start
                ```bash
                # Install Playwright
                npm init playwright@latest
                
                # Install browsers
                npx playwright install
                
                # Run tests
                npx playwright test
                ```
                
                ### Configuration Example
                ```javascript
                // playwright.config.js
                import { defineConfig, devices } from '@playwright/test';
                
                export default defineConfig({
                    testDir: './tests',
                    fullyParallel: true,
                    retries: process.env.CI ? 2 : 0,
                    workers: process.env.CI ? 1 : undefined,
                    
                    use: {
                        baseURL: 'http://localhost:3000',
                        trace: 'on-first-retry',
                    },
                    
                    projects: [
                        { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
                        { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
                        { name: 'webkit', use: { ...devices['Desktop Safari'] } },
                    ],
                });
                ```
                
                ---
                
                ## 📊 Progress Tracking
                
                This portal tracks your learning progress through:
                - ✅ Completed tutorials and guides
                - 📝 AI chat interactions  
                - 🔄 Migration exercises completed
                - 🎯 Best practices mastered
                
                Your progress is automatically saved and can be resumed anytime.
                """)
        
        # Footer
        gr.Markdown("""
        ---
        
        **Playwright Studies Portal** | Built with ❤️ using Gradio & SQLAlchemy | Powered by Kimi-K2-Instruct
        
        *Master test automation with modern tools and AI assistance*
        """, elem_classes="highlight-box")
    
    return app

def main():
    """Main function to run the application"""
    
    print("🎭 Starting Playwright Studies Portal...")
    
    # Check for Hugging Face token
    if not os.getenv("HUGGINGFACE_TOKEN"):
        print("⚠️ HUGGINGFACE_TOKEN not found. AI features may be limited.")
        print("💡 Set your token in .env file for full AI functionality.")
    
    # Create and launch the app
    app = create_main_app()
    
    # Launch configuration
    launch_config = {
        "server_name": "0.0.0.0",
        "server_port": 7860,
        "share": False,  # Set to True to create public link
        "show_error": True,
    }
    
    print("🚀 Launching application...")
    print(f"📍 Access the portal at: http://localhost:{launch_config['server_port']}")
    print("🎯 Features available:")
    print("   • Cypress to Playwright migration tools")
    print("   • Fixtures and custom commands conversion")
    print("   • cy.contains() and custom command detection")
    print("   • Best practices guidance") 
    print("   • OOP & SOLID principles tutorials")
    print("   • Architecture deep dive and analysis")
    print("   • AI-powered assistance")
    print("   • Progress tracking")
    
    app.launch(**launch_config)

if __name__ == "__main__":
    main()
