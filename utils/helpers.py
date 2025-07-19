def format_code_block(code: str, language: str = "javascript") -> str:
    """Format code with proper syntax highlighting"""
    return f"```{language}\n{code}\n```"

def create_comparison_table(cypress_examples: list, playwright_examples: list) -> str:
    """Create a comparison table between Cypress and Playwright"""
    table = "| Cypress | Playwright |\n|---------|------------|\n"
    
    for cypress, playwright in zip(cypress_examples, playwright_examples):
        table += f"| `{cypress}` | `{playwright}` |\n"
    
    return table

def validate_javascript_syntax(code: str) -> tuple[bool, str]:
    """Basic JavaScript syntax validation"""
    try:
        # Basic checks for common syntax issues
        if code.count('(') != code.count(')'):
            return False, "Mismatched parentheses"
        if code.count('{') != code.count('}'):
            return False, "Mismatched curly braces"
        if code.count('[') != code.count(']'):
            return False, "Mismatched square brackets"
        
        return True, "Syntax appears valid"
    except Exception as e:
        return False, f"Validation error: {str(e)}"

def extract_test_patterns(code: str) -> dict:
    """Extract common test patterns from code"""
    patterns = {
        "describe_blocks": code.count("describe("),
        "test_cases": code.count("it(") + code.count("test("),
        "assertions": code.count("expect(") + code.count(".should("),
        "async_functions": code.count("async "),
        "await_calls": code.count("await "),
        "page_interactions": code.count("page.") + code.count("cy.")
    }
    
    return patterns

def generate_test_summary(patterns: dict) -> str:
    """Generate a summary of test patterns found"""
    summary = "**Test Analysis:**\n\n"
    
    if patterns["describe_blocks"] > 0:
        summary += f"• {patterns['describe_blocks']} test suite(s)\n"
    if patterns["test_cases"] > 0:
        summary += f"• {patterns['test_cases']} test case(s)\n"
    if patterns["assertions"] > 0:
        summary += f"• {patterns['assertions']} assertion(s)\n"
    if patterns["async_functions"] > 0:
        summary += f"• {patterns['async_functions']} async function(s)\n"
    if patterns["page_interactions"] > 0:
        summary += f"• {patterns['page_interactions']} page interaction(s)\n"
    
    return summary

def create_learning_progress_bar(completed: int, total: int) -> str:
    """Create a text-based progress bar"""
    if total == 0:
        return "No progress data available"
    
    percentage = (completed / total) * 100
    filled = int(percentage / 10)
    bar = "█" * filled + "░" * (10 - filled)
    
    return f"Progress: {bar} {percentage:.1f}% ({completed}/{total})"

def sanitize_user_input(user_input: str) -> str:
    """Sanitize user input for security"""
    # Remove potentially harmful characters
    dangerous_chars = ['<', '>', '&', '"', "'", ';', '(', ')', '{', '}']
    sanitized = user_input
    
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    return sanitized.strip()

def format_error_message(error: Exception) -> str:
    """Format error messages for user display"""
    error_type = type(error).__name__
    error_message = str(error)
    
    return f"**{error_type}:** {error_message}"

def create_code_diff(old_code: str, new_code: str) -> str:
    """Create a simple diff between old and new code"""
    old_lines = old_code.split('\n')
    new_lines = new_code.split('\n')
    
    diff = "**Changes:**\n\n"
    
    # Simple line-by-line comparison
    max_lines = max(len(old_lines), len(new_lines))
    
    for i in range(max_lines):
        old_line = old_lines[i] if i < len(old_lines) else ""
        new_line = new_lines[i] if i < len(new_lines) else ""
        
        if old_line != new_line:
            if old_line:
                diff += f"- {old_line}\n"
            if new_line:
                diff += f"+ {new_line}\n"
    
    return diff

def estimate_migration_effort(cypress_code: str) -> str:
    """Estimate migration effort based on code complexity"""
    lines = len(cypress_code.split('\n'))
    custom_commands = cypress_code.count('Cypress.Commands.add')
    complex_selectors = cypress_code.count('cy.get(') + cypress_code.count('cy.contains(')
    
    if lines < 50 and custom_commands == 0:
        effort = "Low"
        time = "1-2 hours"
    elif lines < 200 and custom_commands < 5:
        effort = "Medium" 
        time = "1-2 days"
    else:
        effort = "High"
        time = "3-5 days"
    
    return f"**Migration Effort:** {effort} (~{time})\n\n" \
           f"**Factors:**\n" \
           f"• {lines} lines of code\n" \
           f"• {custom_commands} custom commands\n" \
           f"• {complex_selectors} selector updates needed"
