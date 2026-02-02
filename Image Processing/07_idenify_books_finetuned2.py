from vertexai.generative_models import Part
from vertexai.generative_models import GenerativeModel

def count_people_from_image():
    # model_name = "gemini-2.0-flash"
    model_name = "gemini-2.0-flash-001" # Use the latest powerful Pro model

    image1_uri = "gs://promptlyai-public-bucket/images/06_books.jpg"
    image2_uri = "gs://promptlyai-public-bucket/images/07_books.jpg"
    image3_uri = "gs://promptlyai-public-bucket/images/08_books_objects.jpg"
    image4_uri = "gs://promptlyai-public-bucket/images/09_os_book.jpg"

    image_mime_type = "image/jpeg"
    image1_part = Part.from_uri(uri=image1_uri, mime_type=image_mime_type)
    image2_part = Part.from_uri(uri=image2_uri, mime_type=image_mime_type)
    image3_part = Part.from_uri(uri=image3_uri, mime_type=image_mime_type)
    image4_part = Part.from_uri(uri=image4_uri, mime_type=image_mime_type)

    # prompt = """From the given images 
    # 1. How many books are there?
    # 2. Can you list unique book titles?
    # """

    prompt = f"""You are an expert image analyst specializing in text extraction (OCR) from complex scenes.
    You will be given four images containing bookshelves.

    Your goal is to identify and list as many unique book titles as possible visible across *all* 
    provided images. Follow these steps:

    1.  **Examine Each Image:** Carefully analyze each of the four images provided.
    2.  **Focus on Text Extraction:** Pay close attention to the spines of the books. 
        Attempt to extract any visible text fragments, even if partially obscured or at an angle. 
    3.  **Identify Titles:** From the extracted text fragments, identify strings that 
        represent book titles.
    4.  **Output:** Present the identified unique book titles as a clear, numbered list.
    5.  **Non English Books**: It is ok if you can print titles of Non english books as it is
        without you understanding it

    If you cannot read certain text clearly due to blurriness, angle, or language,
    note it as "Unreadable" in the output

    Regarding the book count: provide an *estimated range* (e.g., 60-70) based on visible spines, 
    acknowledging the difficulty of an exact count.

    **Output Format:**

    Estimated Number of Books: [Your estimated range]

    Identified Unique Book Titles:
    1. [Title 1]
    2. [Title 2]
    ...
    """

    contents = [image1_part, image2_part, image3_part, image4_part, prompt]

    multimodal_model = GenerativeModel(model_name)
    response = multimodal_model.generate_content(contents=contents)

    print(response.text)
    print(response.usage_metadata)
    
def main():
    count_people_from_image()

if __name__ == "__main__":
    main()


# * gemini-2.0-flash-001: This model has a larger context window and generally 
#   better reasoning and visual understanding capabilities, which can be beneficial 
#   for reading text in potentially challenging conditions (angles, partial visibility) 
#   and processing multiple images effectively.

# * Specific Role: Telling the model it's an "expert image analyst specializing in 
#   text extraction (OCR)" sets the right context.

# * Step-by-Step Instructions: Breaking down the task helps the model structure its 
#   analysis process (examine -> extract -> identify -> consolidate -> list).

# * Focus on OCR: Explicitly mentioning text extraction and accuracy pushes the 
#   model towards that specific capability.

# * Handling Uncertainty: Acknowledging the difficulty ("reasonable confidence", "do not guess")
#   guides the model on how to handle unreadable text.

# * Clear Output Format: Requesting a specific numbered list for titles and a separate line 
#   for the estimated count makes the output cleaner and easier to parse.

# * Explicit Consolidation: Telling it to combine and deduplicate across all images 
#   ensures it understands the scope.
