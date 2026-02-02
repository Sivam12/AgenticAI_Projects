from google.generativeai import GenerativeModel

def texual_data_queries_01():
    query = """What will be average croud gathering in Tirumala, Andhrapradesh, 
    India in the middle of Summer?"""
    
    instructions = """
    Considering the weather, please provide some precautions and suggestions. 
    Give examples for the daytime and the evening.
    """
    # instructions = ""

    model = "gemini-2.0-flash"
    
    multimodal_model = GenerativeModel(model)
    prompt = [query, instructions]

    response = multimodal_model.generate_content(prompt)
    
    print(response.text)
    
def main():
    texual_data_queries_01()

if __name__ == "__main__":
    main()
    
