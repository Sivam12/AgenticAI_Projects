from vertexai.generative_models import Part
from vertexai.generative_models import GenerativeModel

def count_people_from_image():
    model_name = "gemini-2.0-flash"

    image_uri = "gs://promptlyai-public-bucket/images/03_group.jpg"
    image_mime_type = "image/jpeg"

    image_part = Part.from_uri(uri=image_uri, mime_type=image_mime_type)

    prompt = """From the given image 
    1. Which person's dress color is highliting more?
    2. What is the person's position from the left?
    3. Is the picture is taken at day or night time?
    4. Can you describe the location of the picture?
    """

    contents = [image_part, prompt]

    multimodal_model = GenerativeModel(model_name)
    response = multimodal_model.generate_content(contents=contents)

    print(response.text)

def main():
    count_people_from_image()

if __name__ == "__main__":
    main()
    