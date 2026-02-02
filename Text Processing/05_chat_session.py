from google.generativeai import GenerativeModel

def main():
    model = GenerativeModel("gemini-2.0-flash-001")

    # print(type(model))
    # print(dir(model))
    chat = model.start_chat()

    print("Sending first message...")
    query = "Who is the Prime minister of India?"
    response = chat.send_message(query)
    
    print(f"Query :{query}")
    print(f"Response :{response.text}")

    print("\nSending second message (uses previous context)...")
    query = "When did he took office for the first time?"
    response = chat.send_message(query)

    print(f"Query :{query}")
    print(f"Response :{response.text}")

    print("\n--- Chat History ---")
    for message in chat.history:
        print(f"{message.role}: {message.parts[0].text}")
        
if __name__ == "__main__":
    main()
