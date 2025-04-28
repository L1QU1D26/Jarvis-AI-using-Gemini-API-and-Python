from google import generativeai as genai

genai.configure(api_key="[Enter your Gemini Api key here]")

model = genai.GenerativeModel("gemini-1.5-pro")

response = model.generate_content("Tell me a joke")

print(response.text)
