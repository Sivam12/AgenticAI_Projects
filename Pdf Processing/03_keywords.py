from vertexai.generative_models import Part
from vertexai.generative_models import GenerativeModel

def extract_keywords_topics_entities():
    pdf_uri = "gs://promptlyai-public-bucket/forgotten-history.pdf"
    model_name = "gemini-2.0-flash"

    prompt = """
    Please analyze the content of the provided PDF document about ancient Indian dynasties.

    Based on the document, perform the following tasks:
    1. Keyword Extraction: Identify and list the most relevant single words or short phrases (keywords).
    2. Topic Identification: Identify and list the main topics or themes discussed throughout the document.
    Please format your output clearly with distinct sections for Keywords, Topics, and Entities.
    """

    pdf_file = Part.from_uri(pdf_uri, mime_type="application/pdf")

    contents = [pdf_file, prompt]

    multimodal_model = GenerativeModel(model_name)

    response = multimodal_model.generate_content(contents=contents)
    print("\nExtraction Results:")
    print(response.text)

def main():
    extract_keywords_topics_entities()


if __name__ == "__main__":
    main()