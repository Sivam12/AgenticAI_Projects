from vertexai.generative_models import Part
from vertexai.generative_models import GenerativeModel

def summarize_pdf_local():
    file_path = "/home/bhagavan/aura/Promptly-GenAI/resource/forgotten-history.pdf"
    with open(file_path, "rb") as f:
        pdf_file_data = f.read()

    pdf_part = Part.from_data(data=pdf_file_data, mime_type="application/pdf")

    prompt = """
    You are a professional document summarization specialist.
    Please summarize the given document, capturing the key points and main arguments.
    """
    model_name = "gemini-2.0-flash"
    contents = [pdf_part, prompt]

    multimodal_model = GenerativeModel(model_name)
    response = multimodal_model.generate_content(contents=contents)
    print(f"--- Summary from: {file_path} ---")
    print(response.text)

def summarize_pdf_url():
    file_url = "https://storage.googleapis.com/promptlyai-public-bucket/forgotten-history.pdf"    
    prompt = """
    You are a professional document summarization specialist.
    Please summarize the given document, capturing the key points and main arguments.
    """
    
    model_name = "gemini-2.0-flash"
    pdf_file = Part.from_uri(file_url, mime_type="application/pdf")
    
    contents = [pdf_file, prompt]
    
    multimodal_model = GenerativeModel(model_name)

    response = multimodal_model.generate_content(contents=contents)
    
    print(f"Summary from :{file_url}")
    print(response.text)
    print()

def summarize_pdf_gsuri():
    file_uri = "gs://promptlyai-public-bucket/forgotten-history.pdf"
    prompt = """
    You are a professional document summarization specialist.
    Please summarize the given document, capturing the key points and main arguments.
    """
    
    model_name = "gemini-2.0-flash"
    pdf_file = Part.from_uri(file_uri, mime_type="application/pdf")
    
    contents = [pdf_file, prompt]
    
    multimodal_model = GenerativeModel(model_name)

    response = multimodal_model.generate_content(contents=contents)
    
    print(f"Summary from :{file_uri}")
    print(response.text)
    print()

def main():
    # summarize_pdf_local()
    # summarize_pdf_url()
    summarize_pdf_gsuri()
    
if __name__ == "__main__":
    main()

