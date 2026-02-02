from google.generativeai import GenerativeModel

def main():
    model = GenerativeModel("gemini-2.0-flash-001")

    query = "Who is the Prime minister of India?"
    response = model.generate_content(query)
    print(response.text)
    
    query = "When did he took office for the first time?"
    response = model.generate_content(query)
    print(response.text)

    query = """
    You said, The current Prime Minister of India is Narendra Modi.  
    When did he took office for the first time?"
    """
    response = model.generate_content(query)
    print(response.text)

if __name__ == "__main__":
    main()
