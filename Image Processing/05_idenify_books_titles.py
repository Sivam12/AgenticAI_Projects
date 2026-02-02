from vertexai.generative_models import Part
from vertexai.generative_models import GenerativeModel

def count_people_from_image():
    model_name = "gemini-2.0-flash"

    image1_uri = "gs://promptlyai-public-bucket/images/06_books.jpg"
    image2_uri = "gs://promptlyai-public-bucket/images/07_books.jpg"
    image3_uri = "gs://promptlyai-public-bucket/images/08_books_objects.jpg"
    image4_uri = "gs://promptlyai-public-bucket/images/09_os_book.jpg"

    image_mime_type = "image/jpeg"
    image1_part = Part.from_uri(uri=image1_uri, mime_type=image_mime_type)
    image2_part = Part.from_uri(uri=image2_uri, mime_type=image_mime_type)
    image3_part = Part.from_uri(uri=image3_uri, mime_type=image_mime_type)
    image4_part = Part.from_uri(uri=image4_uri, mime_type=image_mime_type)

    prompt = """From the given images 
    1. How many books are there?
    2. Can you list unique book titles?
    """

    contents = [image1_part, image2_part, image3_part, image4_part, prompt]

    multimodal_model = GenerativeModel(model_name)
    response = multimodal_model.generate_content(contents=contents)

    print(response.text)

def main():
    count_people_from_image()

if __name__ == "__main__":
    main()
    