from vertexai.generative_models import (
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

    prompt = "is nine even?"
    validate(model, prompt)

    prompt = "10 is even?"
    validate(model, prompt)

    prompt = "Is abc even?"
    validate(model, prompt)

if __name__ == "__main__":
    main()
