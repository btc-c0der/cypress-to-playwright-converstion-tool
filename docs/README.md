# Playwright Studies Portal

![Playwright Logo](https://playwright.dev/img/playwright-logo.svg)

A comprehensive educational portal for learning Playwright test automation, built with **Gradio** and **SQLAlchemy**, powered by the **Kimi-K2-Instruct** AI model from Hugging Face.

## 🎯 Features

### 🔄 Cypress to Playwright Migration
- **Interactive Code Converter**: Paste Cypress code and get Playwright equivalent
- **Syntax Comparison**: Side-by-side comparison of commands and assertions
- **Migration Strategies**: Step-by-step guidance for different migration scenarios
- **Best Practices**: Recommended approaches for smooth migration

### 🎯 Playwright Best Practices
- **Page Object Model**: Implementation patterns and examples
- **Selector Strategies**: Priority order and resilient selector techniques
- **Test Organization**: Structure and naming conventions
- **Parallel Execution**: Configuration and optimization
- **CI/CD Integration**: Setup for continuous testing

### 🏗️ OOP Principles in Test Automation
- **Encapsulation**: Hide implementation details in page objects
- **Inheritance**: Share common functionality across test classes
- **Polymorphism**: Flexible test framework design
- **Abstraction**: Simplify complex test operations

### 🔧 SOLID Principles Applied
- **Single Responsibility**: One purpose per class
- **Open/Closed**: Extensible without modification
- **Liskov Substitution**: Interchangeable subclasses
- **Interface Segregation**: Focused interfaces
- **Dependency Inversion**: Depend on abstractions

### 🤖 AI-Powered Assistant
- **Interactive Chat**: Ask questions about Playwright
- **Code Examples**: Get personalized code snippets
- **Best Practice Guidance**: Receive expert recommendations
- **Migration Help**: Specific assistance for conversion tasks

### 📊 Progress Tracking
- **Study Modules**: Track completion of learning modules
- **User Progress**: SQLAlchemy-based persistence
- **Learning Analytics**: Monitor your improvement over time

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager
- (Optional) Hugging Face account for AI features

### Installation

1. **Clone or download** this project to your local machine

2. **Run the setup script**:
   ```bash
   ./setup.sh
   ```

3. **Configure environment** (optional but recommended):
   ```bash
   # Edit .env file and add your Hugging Face token
   HUGGINGFACE_TOKEN=your_token_here
   ```

4. **Start the portal**:
   ```bash
   source venv/bin/activate  # Activate virtual environment
   python main.py           # Start the application
   ```

5. **Access the portal** at [http://localhost:7860](http://localhost:7860)

### Manual Installation

If you prefer manual setup:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_data.py

# Start the portal
python main.py
```

## 📚 Learning Paths

### 🔰 Beginner Path
1. **Basic Syntax Conversion** - Learn fundamental Cypress → Playwright mappings
2. **Selector Strategies** - Master resilient element selection
3. **Simple Page Objects** - Create your first page object classes

### 🔥 Intermediate Path
1. **Advanced Migration** - Handle complex Cypress patterns
2. **Test Organization** - Structure large test suites
3. **OOP Principles** - Apply object-oriented design
4. **Configuration Management** - Multi-environment setups

### 🚀 Advanced Path
1. **Framework Architecture** - Design scalable test frameworks
2. **SOLID Principles** - Create maintainable code
3. **Performance Optimization** - Parallel execution and CI/CD
4. **Custom Extensions** - Build framework add-ons

## 🛠️ Project Structure

```
playwright-cypress/
├── main.py                 # Main Gradio application
├── init_data.py            # Database initialization
├── setup.sh               # Automated setup script
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── README.md             # This file
│
├── models/               # SQLAlchemy database models
│   ├── __init__.py
│   └── database.py      # User, StudyModule, Progress models
│
├── services/             # Business logic and AI services
│   ├── __init__.py
│   ├── ai_service.py    # Kimi-K2-Instruct integration
│   └── study_service.py # Progress tracking service
│
├── components/           # Gradio UI components
│   ├── __init__.py
│   └── interfaces.py    # Tab interfaces and interactions
│
├── data/                # Study materials and examples
│   ├── __init__.py
│   ├── migration_guide.py      # Cypress → Playwright examples
│   ├── best_practices.py       # Playwright best practices
│   ├── oop_principles.py       # OOP in test automation
│   ├── solid_principles.py     # SOLID principles guide
│   └── framework_best_practices.py # Framework design
│
└── utils/               # Utility functions
    ├── __init__.py
    └── helpers.py       # Code formatting and validation
```

## 🎨 Technologies Used

- **[Gradio](https://gradio.app/)** - Interactive web UI framework
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - Database ORM for progress tracking
- **[Transformers](https://huggingface.co/transformers/)** - Hugging Face model integration
- **[Kimi-K2-Instruct](https://huggingface.co/moonshotai/Kimi-K2-Instruct)** - AI model for assistance
- **[Python-dotenv](https://pypi.org/project/python-dotenv/)** - Environment configuration

## 🎯 Use Cases

### For QA Engineers
- **Migration Projects**: Convert existing Cypress test suites
- **Skill Development**: Learn modern test automation practices
- **Best Practices**: Improve test code quality and maintainability

### For Development Teams
- **Framework Design**: Build robust test automation frameworks
- **Code Reviews**: Apply SOLID principles to test code
- **CI/CD Integration**: Optimize test execution in pipelines

### For Educators
- **Training Materials**: Comprehensive curriculum for test automation
- **Hands-on Learning**: Interactive examples and exercises
- **Progress Tracking**: Monitor student advancement

### For Test Automation Consultants
- **Client Training**: Standardized learning materials
- **Migration Planning**: Structured approach to framework transitions
- **Best Practice Documentation**: Reference implementation patterns

## 🔧 Configuration

### Environment Variables (.env)
```bash
# Hugging Face token for AI features
HUGGINGFACE_TOKEN=your_token_here

# Database configuration (SQLite by default)
DATABASE_URL=sqlite:///./study_portal.db
```

### Customization Options
- **AI Model**: Change the Hugging Face model in `services/ai_service.py`
- **Database**: Switch from SQLite to PostgreSQL/MySQL in `models/database.py`
- **UI Theme**: Modify Gradio theme in `main.py`
- **Content**: Add new study modules in `data/` directory

## 🤝 Contributing

We welcome contributions! Here are ways you can help:

1. **Add Study Content**: Create new learning modules
2. **Improve AI Responses**: Enhance the AI prompt engineering
3. **Bug Fixes**: Report and fix issues
4. **Feature Requests**: Suggest new functionality
5. **Documentation**: Improve guides and examples

### Development Setup
```bash
# Clone the repository
git clone <repository-url>
cd playwright-cypress

# Setup development environment
./setup.sh

# Run in development mode
python main.py
```

## 📈 Roadmap

### Version 2.0
- [ ] **Multi-language Support** - TypeScript, Python, Java examples
- [ ] **Video Tutorials** - Embedded learning videos
- [ ] **Code Playground** - Interactive code editor
- [ ] **Team Features** - Multi-user progress tracking

### Version 3.0
- [ ] **Mobile App** - Native mobile application
- [ ] **Advanced Analytics** - Detailed learning insights
- [ ] **Certification** - Playwright proficiency certificates
- [ ] **Community Features** - User-generated content

## 🐛 Troubleshooting

### Common Issues

**AI Assistant not responding:**
- Ensure `HUGGINGFACE_TOKEN` is set in `.env`
- Check internet connectivity
- Verify token has access to the model

**Database errors:**
- Run `python init_data.py` to reset database
- Check file permissions in project directory

**Installation issues:**
- Ensure Python 3.8+ is installed
- Use virtual environment to avoid conflicts
- Update pip: `pip install --upgrade pip`

### Getting Help
- Check the **Resources** tab in the portal
- Review error messages in the terminal
- Consult [Playwright documentation](https://playwright.dev/)

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Microsoft Playwright Team** - For the amazing testing framework
- **Hugging Face** - For the Kimi-K2-Instruct model and platform
- **Gradio Team** - For the user-friendly web UI framework
- **SQLAlchemy** - For the robust database ORM

---

**Made with ❤️ for the test automation community**

*Empowering developers and QA engineers to master modern test automation with AI-assisted learning*
