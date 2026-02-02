from vertexai.generative_models import Part
from vertexai.generative_models import GenerativeModel

def summarize_QnA():
    file_uri = "gs://promptlyai-public-bucket/forgotten-history.pdf"
    
    prompt = """
    Which dynasties ruled concurrently or had overlapping time periods?    
    """
    
    model_name = "gemini-2.0-flash"
    pdf_file = Part.from_uri(file_uri, mime_type="application/pdf")
    
    contents = [pdf_file, prompt]
    
    multimodal_model = GenerativeModel(model_name)

    response = multimodal_model.generate_content(contents=contents)
    
    print(response.text)
    print()

def generate_testpaper():
    file_url = "https://storage.googleapis.com/promptlyai-public-bucket/forgotten-history.pdf"    
    prompt = """
    You are a professional document summarization specialist
    Can you generate a test paper with 10 question on Pala Empire & Chola Dynasty"
    """
    
    model_name = "gemini-2.0-flash"
    pdf_file = Part.from_uri(file_url, mime_type="application/pdf")
    
    contents = [pdf_file, prompt]
    
    multimodal_model = GenerativeModel(model_name)

    response = multimodal_model.generate_content(contents=contents)
    
    print(f"Summary from :{file_url}")
    print(response.text)
    print()


def main():
    # summarize_QnA()
    generate_testpaper()
    
if __name__ == "__main__":
    main()
