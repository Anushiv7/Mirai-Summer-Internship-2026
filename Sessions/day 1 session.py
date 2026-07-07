from google import genai 
client = genai.Client(api_key="YOUR_API_KEY_HERE")
response=client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain to me how does a gemini API work in one sentence."
)
print(response.text)
