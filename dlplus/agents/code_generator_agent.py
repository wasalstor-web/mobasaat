"""
Code Generator Agent
وكيل توليد الأكواد البرمجية
"""

from typing import Dict, List, Optional
from .base_agent import BaseAgent


class CodeGeneratorAgent(BaseAgent):
    """
    Agent for generating code in multiple programming languages
    وكيل توليد الأكواد بلغات برمجة متعددة
    """
    
    def __init__(self):
        super().__init__(
            name="CodeGeneratorAgent",
            description="Generates code in multiple programming languages with documentation"
        )
        self.add_capability("code_generation")
        self.add_capability("code_documentation")
        self.add_capability("unit_tests")
        
        # Supported languages
        self.supported_languages = [
            "python", "javascript", "java", "c++", "go",
            "rust", "typescript", "php", "ruby", "swift"
        ]
        
        # Code templates
        self.templates = {
            "python": {
                "function": '''def {name}({params}):
    """
    {description}
    
    Args:
        {args_doc}
    
    Returns:
        {return_doc}
    """
    {body}
''',
                "class": '''class {name}:
    """
    {description}
    """
    
    def __init__(self{params}):
        {init_body}
    
    {methods}
'''
            },
            "javascript": {
                "function": '''/**
 * {description}
 * @param {{{type}}} {param}
 * @returns {{{return_type}}}
 */
function {name}({params}) {{
    {body}
}}
''',
                "class": '''/**
 * {description}
 */
class {name} {{
    constructor({params}) {{
        {init_body}
    }}
    
    {methods}
}}
'''
            }
        }
    
    async def execute(self, task: str, context: Optional[Dict] = None) -> Dict:
        """
        Execute code generation task
        تنفيذ مهمة توليد الكود
        """
        try:
            # Parse requirements from task
            requirements = self._parse_requirements(task)
            
            # Detect language
            language = self._detect_language(task, requirements)
            
            # Generate code
            code = self._generate_code(requirements, language)
            
            # Generate tests
            tests = self._generate_tests(requirements, language)
            
            # Generate documentation
            documentation = self._generate_documentation(requirements, language)
            
            result = {
                "success": True,
                "language": language,
                "code": code,
                "tests": tests,
                "documentation": documentation,
                "file_name": f"{requirements.get('name', 'output')}.{self._get_extension(language)}"
            }
            
            self._log_execution(task, result, success=True)
            return result
            
        except Exception as e:
            self._log_execution(task, str(e), success=False)
            return {
                "success": False,
                "error": str(e)
            }
    
    def _parse_requirements(self, task: str) -> Dict:
        """Parse code generation requirements from task"""
        requirements = {
            "name": "generated_function",
            "description": task,
            "type": "function",
            "params": [],
            "return_type": "None"
        }
        
        # Extract function/class name
        if "class" in task.lower() or "كلاس" in task or "صنف" in task:
            requirements["type"] = "class"
            requirements["name"] = "GeneratedClass"
        
        # Extract language hints
        if "python" in task.lower() or "بايثون" in task:
            requirements["language"] = "python"
        elif "javascript" in task.lower() or "جافا سكريبت" in task:
            requirements["language"] = "javascript"
        
        return requirements
    
    def _detect_language(self, task: str, requirements: Dict) -> str:
        """Detect programming language from task"""
        task_lower = task.lower()
        
        # Check explicit mentions
        for lang in self.supported_languages:
            if lang in task_lower:
                return lang
        
        # Check requirements
        if "language" in requirements:
            return requirements["language"]
        
        # Default to Python
        return "python"
    
    def _generate_code(self, requirements: Dict, language: str) -> str:
        """Generate code based on requirements"""
        code_type = requirements.get("type", "function")
        
        if language == "python":
            if code_type == "function":
                code = self._generate_python_function(requirements)
            else:
                code = self._generate_python_class(requirements)
        
        elif language == "javascript":
            if code_type == "function":
                code = self._generate_javascript_function(requirements)
            else:
                code = self._generate_javascript_class(requirements)
        
        else:
            code = f"# Code generation for {language} not yet implemented\n"
            code += f"# TODO: Implement {requirements['description']}\n"
        
        return code
    
    def _generate_python_function(self, req: Dict) -> str:
        """Generate Python function"""
        return f'''def {req['name']}():
    """
    {req['description']}
    """
    # TODO: Implement function logic
    pass
'''
    
    def _generate_python_class(self, req: Dict) -> str:
        """Generate Python class"""
        return f'''class {req['name']}:
    """
    {req['description']}
    """
    
    def __init__(self):
        """Initialize the class"""
        pass
    
    def main_method(self):
        """Main method"""
        # TODO: Implement method logic
        pass
'''
    
    def _generate_javascript_function(self, req: Dict) -> str:
        """Generate JavaScript function"""
        return f'''/**
 * {req['description']}
 */
function {req['name']}() {{
    // TODO: Implement function logic
}}
'''
    
    def _generate_javascript_class(self, req: Dict) -> str:
        """Generate JavaScript class"""
        return f'''/**
 * {req['description']}
 */
class {req['name']} {{
    constructor() {{
        // TODO: Initialize class
    }}
    
    mainMethod() {{
        // TODO: Implement method logic
    }}
}}
'''
    
    def _generate_tests(self, requirements: Dict, language: str) -> str:
        """Generate unit tests"""
        if language == "python":
            return f'''import unittest

class Test{requirements['name'].title()}(unittest.TestCase):
    def test_basic(self):
        """Test basic functionality"""
        # TODO: Add test cases
        pass

if __name__ == '__main__':
    unittest.main()
'''
        else:
            return f"// TODO: Generate tests for {language}"
    
    def _generate_documentation(self, requirements: Dict, language: str) -> str:
        """Generate documentation"""
        return f'''# {requirements['name']} Documentation

## Description
{requirements['description']}

## Language
{language}

## Usage
```{language}
# TODO: Add usage examples
```

## API Reference
- TODO: Document functions/methods
'''
    
    def _get_extension(self, language: str) -> str:
        """Get file extension for language"""
        extensions = {
            "python": "py",
            "javascript": "js",
            "typescript": "ts",
            "java": "java",
            "c++": "cpp",
            "go": "go",
            "rust": "rs",
            "php": "php",
            "ruby": "rb",
            "swift": "swift"
        }
        return extensions.get(language, "txt")
