from vertexai.generative_models import Part
from vertexai.generative_models import GenerativeModel

def get_structured_output():
    pdf_uri = "gs://promptlyai-public-bucket/forgotten-history.pdf"
    model_name = "gemini-2.0-flash"

    prompt = """
    Please analyze the content of the provided PDF document about ancient Indian dynasties.

    Based on the document, perform the following tasks:
    1. Who are all the rulers and their time period?
    2. Can you give me a structured output in a JSON format?
    """
    # 3. Make sure there is a column which specifies, duration of the ruler in years

    pdf_file = Part.from_uri(pdf_uri, mime_type="application/pdf")

    contents = [pdf_file, prompt]

    multimodal_model = GenerativeModel(model_name)

    response = multimodal_model.generate_content(contents=contents)
    print("\nExtraction Results:")
    print(response.text)

def main():
    get_structured_output()


if __name__ == "__main__":
    main()