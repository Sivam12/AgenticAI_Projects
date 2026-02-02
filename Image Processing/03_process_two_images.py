from vertexai.generative_models import Part
from vertexai.generative_models import GenerativeModel

def count_people_from_image():
    model_name = "gemini-2.5-pro"

    image_mime_type = "image/jpeg"
    image1_uri = "gs://promptlyai-public-bucket/images/01_01_group.jpg"
    image2_uri = "gs://promptlyai-public-bucket/images/01_02_group.jpg"
    image2_uri = "gs://promptlyai-public-bucket/images/03_group.jpg"

    image_part1 = Part.from_uri(uri=image1_uri, mime_type=image_mime_type)
    image_part2 = Part.from_uri(uri=image2_uri, mime_type=image_mime_type)

    prompt = """From given two images can you count number of people in each image?  
    Also, are they same people?"""

    contents = [image_part1, image_part2, prompt]

    multimodal_model = GenerativeModel(model_name)
    response = multimodal_model.generate_content(contents=contents)

    print(response.text)

def main():
    count_people_from_image()

if __name__ == "__main__":
    main()
    