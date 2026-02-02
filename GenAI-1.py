import google.generativeai as genai
 
model = genai.GenerativeModel('gemini-2.0-flash')
response = model.generate_content("Explain LLM")
print(response.text)