from vertexai.generative_models import Part
from vertexai.generative_models import GenerativeModel

def create_quiz_prompt_string(num_items, topic):
    topic_instruction = f"""\nFocus specifically on the information related 
    to the topic: '{topic}' within the document."""

    prompt = f"""
    You are an expert educational assistant specializing in creating study aids.
    Analyze the content of the provided PDF document.

    {topic_instruction}

    Based *only* on the information present in the document, generate exactly {num_items} quiz questions.
    Each quiz item must strictly follow the format below, with a clear question ('Q:') and a 
    concise answer ('A:') derived directly from the text. Do not add any extra text before the
    first 'Q:' or after the last answer.

    Format for each question:
    Q: [Question about PDF content]?
    A: [Answer derived *directly* from PDF content]

    Example:
    Q: What was the primary export of the region mentioned on page 5?
    A: The primary export was grain, according to the document.
    """
    return prompt


def generate_quiz():
    file_uri = "gs://promptlyai-public-bucket/forgotten-history.pdf"
    output_type = "quiz"
    num_items = 5
    topic = "Chola Empire"

    prompt = create_quiz_prompt_string(num_items, topic)

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
    generate_quiz()

if __name__ == "__main__":
    main()
