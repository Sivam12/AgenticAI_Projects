from vertexai.generative_models import Part
from vertexai.generative_models import GenerativeModel

def count_people_from_image():
    # model_name = "gemini-2.0-flash"
    model_name = "gemini-2.5-pro"

    image_uri = "gs://promptlyai-public-bucket/images/03_group.jpg"
    image_mime_type = "image/jpeg"

    image_part = Part.from_uri(uri=image_uri, mime_type=image_mime_type)

    prompt = """From the given image can you count number of people?"""

    contents = [image_part, prompt]

    multimodal_model = GenerativeModel(model_name)
    response = multimodal_model.generate_content(contents=contents)

    print(response.text)

def main():
    count_people_from_image()

if __name__ == "__main__":
    main()
    