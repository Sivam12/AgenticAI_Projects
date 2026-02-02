from vertexai.generative_models import Part
from vertexai.generative_models import GenerativeModel

def count_people_from_image():
    model_name = "gemini-2.0-flash"
    # model_name = "gemini-2.5-pro"

    image_uri = "gs://promptlyai-public-bucket/images/rameswaram-temple.jpeg"
    image_mime_type = "image/jpeg"

    image_part = Part.from_uri(uri=image_uri, mime_type=image_mime_type)

    prompt = """
    Can you identify the location of the image?
    """

    contents = [image_part, prompt]

    multimodal_model = GenerativeModel(model_name)
    response = multimodal_model.generate_content(contents=contents)

    print(response.text)
    print(response.usage_metadata)
    
def main():
    count_people_from_image()

if __name__ == "__main__":
    main()
    