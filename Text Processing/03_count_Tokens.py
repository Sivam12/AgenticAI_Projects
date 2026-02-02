from google.generativeai import GenerativeModel

def main():
    model = GenerativeModel("gemini-2.0-flash-001")

    response = model.count_tokens("Who is the Prime minister of India")
    print(response)
    
if __name__ == "__main__":
    main()

