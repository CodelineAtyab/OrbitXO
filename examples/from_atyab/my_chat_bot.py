import requests

API_KEY = r"12u362183712987iuqwyedhuiqweqyh912371289"

user_question = input("Enter your question: ")

json_payload = {
  "contents": [{
      "parts":[
          {"text": user_question}
        ]
    }]
}

response = requests.post(
  url=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={API_KEY}",
  json=json_payload
)

text_response = response.json()['candidates'][0]['content']['parts'][0]['text']
print(text_response)