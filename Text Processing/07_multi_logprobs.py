from google.generativeai import GenerativeModel
import google.generativeai as genai
 
def query_by_model(model_name):
    model = GenerativeModel(model_name=model_name)
    
    contents = "Who is the Prime minister of India"
    print(f"Queriyng :{model_name}")
    response = model.generate_content(contents=contents)
    
    print(response.text)
    print(response)
    print()

def list_supported_models():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)

# avg_logprobs
def main():
    model_name = "gemini-2.0-flash"
    query_by_model(model_name)

    model_name = "gemini-2.5-pro"
    query_by_model(model_name)

    
if __name__ == "__main__":
    main()
    
