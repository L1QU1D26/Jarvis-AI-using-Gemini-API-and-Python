from google import generativeai as genai

genai.configure(api_key="AIzaSyBeutP6EsnwNBbGm4hsNdnfc2m4lYM5EVA")

model = genai.GenerativeModel("gemini-1.5-pro")

response = model.generate_content("Tell me a joke")

print(response.text)
