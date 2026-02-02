from vertexai.generative_models import Part
from vertexai.generative_models import GenerativeModel

def count_people_from_image():
    model_name = "gemini-2.0-flash-001"

    image1_uri = "gs://promptlyai-public-bucket/images/06_books.jpg"
    image2_uri = "gs://promptlyai-public-bucket/images/07_books.jpg"
    image3_uri = "gs://promptlyai-public-bucket/images/08_books_objects.jpg"
    image4_uri = "gs://promptlyai-public-bucket/images/09_os_book.jpg"

    image_mime_type = "image/jpeg"
    image1_part = Part.from_uri(uri=image1_uri, mime_type=image_mime_type)
    image2_part = Part.from_uri(uri=image2_uri, mime_type=image_mime_type)
    image3_part = Part.from_uri(uri=image3_uri, mime_type=image_mime_type)
    image4_part = Part.from_uri(uri=image4_uri, mime_type=image_mime_type)

    prompt = f"""You are an expert image analyst specializing in identifying different objects from complex scenes.
    You will be given four images containing bookshelves.

    Your goal is to identify and list as many objects as possible visible across *all* 
    provided images. Follow these steps:

    1.  **Examine Each Image:** Carefully analyze each of the four images provided.
    2.  **Focus on objects other than books:** 
    3.  **Include image name associated with the identified object**
    """

    contents = [image1_part, image2_part, image3_part, image4_part, prompt]

    multimodal_model = GenerativeModel(model_name)
    response = multimodal_model.generate_content(contents=contents)

    print(response.text)

def main():
    count_people_from_image()

if __name__ == "__main__":
    main()
    