from google.generativeai import GenerativeModel

def main():
    model_name = "gemini-2.0-flash"

    query1 = "Who is the Prime minister of India"
    query2 = "Help me with his top 20 achievements"

    print(f"--- Querying Model: {model_name} (Streaming) ---")
    print(f"Prompt 1: {query1}")
    print(f"Prompt 2: {query2}\n")


    try:
        model = GenerativeModel(model_name=model_name)

        response_iterator = model.generate_content(contents=[query1, query2], stream=True)

        print("Streaming response:\n")
        full_response_text = ""

        i = 1
        for chunk in response_iterator:
            try:
                print(f"=={i}==. {chunk.text}", end="")
                i = i + 1
                full_response_text += chunk.text
            except ValueError:
                print(f"\n[Received chunk without text content]", end="")
                pass 

        print(f"\n\n--- Streaming Complete in {i} chunks ---")
        
    except Exception as e:
        print(f"\nAn error occurred during streaming generation: {e}")
    print("\n--- Example Finished ---")


if __name__ == "__main__":
    main()