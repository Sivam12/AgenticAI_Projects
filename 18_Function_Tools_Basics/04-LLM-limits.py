import os
from vertexai.generative_models import (
    GenerationConfig,
    GenerativeModel,
)


def validate(model, prompt):
    print(f"{prompt}")
    response = model.generate_content(prompt)
    print(response.text)
    print()

def main():
    MODEL = "gemini-2.0-flash-001"
    model = GenerativeModel(MODEL)
    
    prompt = "is 9 even?"
    validate(model, prompt)

    prompt = "What's the exchange rate for Rupees to dollars today?"
    validate(model, prompt)

    prompt = """Can you distribute 50% of its annual profit as bonuses to my employees, 
    weighted by their performance ratings?"""
    validate(model, prompt)

if __name__ == "__main__":
    main()
