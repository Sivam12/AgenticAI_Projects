from google.generativeai import GenerativeModel

def main():
    model_name = "gemini-2.0-flash"
    
    query1 = "Who is the Prime minister of India"
    query2 = "Who is the Prime minister of UK"

    model = GenerativeModel(model_name=model_name)
    response = model.generate_content(contents=[query1, query2])
    
    print(response.text)
    print()

if __name__ == "__main__":
    main()
    
