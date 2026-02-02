from vertexai.generative_models import Part
from vertexai.generative_models import GenerativeModel

def describe_image_from_gcs():
    # model_name = "gemini-2.0-flash"
    model_name = "gemini-2.5-pro"

    image_uri = "gs://promptlyai-public-bucket/images/03_group.jpg"
    image_mime_type = "image/jpeg"

    image_part = Part.from_uri(uri=image_uri, mime_type=image_mime_type)

    prompt = """Please describe this image briefly. What are the main objects, 
    setting, and any activities depicted?"""

    contents = [image_part, prompt]

    multimodal_model = GenerativeModel(model_name)
    response = multimodal_model.generate_content(contents=contents)

    print(f"\n--- Image Description ---")
    print(f"Source GCS URI: {image_uri}")
    print(f"MIME Type: {image_mime_type}")
    print("\nGenerated Description:")
    print(response.text)
    print(f"-------------------------")

def main():
    describe_image_from_gcs()

if __name__ == "__main__":
    main()
    