from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os
from dotenv import load_dotenv
from typing import Optional, List, Dict, Any
import json

load_dotenv()

class KimiAIService:
    """AI service using Kimi-K2-Instruct model for Playwright education assistance"""
    
    def __init__(self):
        self.model_name = "moonshotai/Kimi-K2-Instruct"
        self.tokenizer = None
        self.model = None
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the Kimi-K2-Instruct model"""
        try:
            print("Loading Kimi-K2-Instruct model...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                token=os.getenv("HUGGINGFACE_TOKEN"),
                trust_remote_code=True
            )
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                token=os.getenv("HUGGINGFACE_TOKEN"),
                trust_remote_code=True,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None
            )
            
            if not torch.cuda.is_available():
                self.model = self.model.to(self.device)
                
            print("Model loaded successfully!")
            
        except Exception as e:
            print(f"Error loading model: {e}")
            # Fallback to a simple response system
            self.model = None
            self.tokenizer = None
    
    def generate_response(self, prompt: str, max_length: int = 512, temperature: float = 0.7) -> str:
        """Generate AI response for educational queries"""
        if self.model is None or self.tokenizer is None:
            return self._fallback_response(prompt)
        
        try:
            # Format prompt for educational context
            formatted_prompt = self._format_educational_prompt(prompt)
            
            # Tokenize input
            inputs = self.tokenizer.encode(formatted_prompt, return_tensors="pt").to(self.device)
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=max_length,
                    temperature=temperature,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    num_return_sequences=1
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the generated part
            response = response[len(formatted_prompt):].strip()
            
            return response
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return self._fallback_response(prompt)
    
    def _format_educational_prompt(self, user_query: str) -> str:
        """Format the prompt for educational context"""
        return f"""You are an expert Playwright testing instructor. Help students learn Playwright by providing clear, accurate, and practical guidance.

Student Question: {user_query}

Please provide a helpful, educational response that includes:
1. Clear explanation
2. Code examples when relevant
3. Best practices
4. Common pitfalls to avoid

Response:"""
    
    def _fallback_response(self, prompt: str) -> str:
        """Fallback response when model is unavailable"""
        responses = {
            "cypress": "To convert Cypress to Playwright, focus on these key areas: syntax differences, assertion methods, and configuration. Would you like specific examples?",
            "best practices": "Playwright best practices include using Page Object Model, proper selectors, parallel execution, and comprehensive error handling.",
            "oop": "Object-Oriented Programming in test automation helps create maintainable, scalable test suites through encapsulation, inheritance, and polymorphism.",
            "solid": "SOLID principles in test automation ensure clean, maintainable code: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion.",
            "framework": "Test automation frameworks should be modular, maintainable, and follow established patterns for maximum effectiveness."
        }
        
        query_lower = prompt.lower()
        for key, response in responses.items():
            if key in query_lower:
                return response
        
        return "I'm here to help you learn Playwright! Please ask about Cypress migration, best practices, OOP principles, SOLID principles, or framework design."

# Singleton instance
ai_service = KimiAIService()
