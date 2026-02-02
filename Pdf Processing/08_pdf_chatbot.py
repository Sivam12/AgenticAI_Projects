from vertexai.generative_models import Part
from vertexai.generative_models import GenerativeModel

questions = [
    "What were some of the major achievements of the Chola dynasty mentioned in the document?",
    "What was the specific recipe for gunpowder used by the Song dynasty?",
    "Can you tell me about the administrative structure described for the Mauryan Empire?",    
]

      
def run_chat_session():
    pdf_uri = "gs://promptlyai-public-bucket/forgotten-history.pdf"
    model_name = "gemini-2.0-flash-001"

    prompt_template = """You are a specialized Question Answering assistant.
    Your task is to answer the user's *current* question based *exclusively* on the content
    of the provided PDF document ('forgotten-history.pdf').
    **Ignore any previous questions or answers in this chat session.**
    Do not use any external knowledge or information outside of the provided PDF document for this answer.

    User Question: "{user_question}"

    Carefully review the **provided document content** to find the answer to this question.
    If the information required to answer the question is present in the document,
    provide a concise and accurate answer derived solely from the document text.
    If the information is *not* found within the document, respond exactly with:
    "Based on the provided document, I cannot answer that question."
    """

    pdf_file = Part.from_uri(pdf_uri, mime_type="application/pdf")

    model = GenerativeModel(model_name)
    chat: ChatSession = model.start_chat()

    for user_question in questions:
        prompt = prompt_template.format(user_question=user_question)
        response = chat.send_message([pdf_file, prompt])
        print(f"Prompt :{prompt}")
        print(f"Chatbot: {response.text}")
        print("-" * 30)
        
if __name__ == "__main__":
    run_chat_session()