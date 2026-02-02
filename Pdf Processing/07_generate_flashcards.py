from vertexai.generative_models import Part
from vertexai.generative_models import GenerativeModel

def create_flashcard_prompt_string(num_items, topic):
    topic_instruction = f"""\nFocus specifically on identifying key terms and 
    concepts related to the topic: '{topic}' within the document." if topic else """

    prompt = f"""
    You are an expert educational assistant specializing in creating study aids.
    Analyze the content of the provided PDF document.

    {topic_instruction}

    Based *only* on the information present in the document, generate exactly {num_items} 
    flashcards covering key terms, concepts, or important names.
    Each flashcard must strictly follow the format below, with a 'Term:' (the key concept/name) 
    and a 'Definition:' (a concise explanation derived directly from the PDF). 
    Do not add any extra text before the first 'Term:' or after the last definition.

    Format for each flashcard:
    Term: [Key Term, Concept, or Name from PDF]
    Definition: [Concise explanation derived *directly* from PDF content]

    Example:
    Term: Mauryan Empire
    Definition: An ancient Indian empire founded by Chandragupta Maurya, 
    which existed from 322 BCE to 185 BCE, known for its centralized administration 
    as described in the document.
    """
    return prompt




def generate_flashcards():
    file_uri = "gs://promptlyai-public-bucket/forgotten-history.pdf"
    output_type = "quiz"
    num_items = 5
    topic = "Chola Empire"

    prompt = create_flashcard_prompt_string(num_items, topic)

    model_name = "gemini-2.0-flash"
    pdf_part = Part.from_uri(file_uri, mime_type="application/pdf")
    contents = [pdf_part, prompt]
    
    multimodal_model = GenerativeModel(model_name)
    response = multimodal_model.generate_content(contents=contents)

    output_title = f"--- Generated {output_type.capitalize()} ({num_items} items) from: {file_uri} ---"
    if topic:
        output_title += f" (Topic: {topic})"
    print(output_title)
    print(response.text)
    print("-" * len(output_title))

def main():
    generate_flashcards()

if __name__ == "__main__":
    main()
