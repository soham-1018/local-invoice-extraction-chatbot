
import requests

url = "http://localhost:11434/api/chat"

data = {
    "model": "llama3.2:1b",
    "messages": [
        {
            "role": "user",
            "content": "What is an invoice? Explain in simple words."
        }
    ],
    "stream": False
}

response = requests.post(url, json=data)

result = response.json()

print("Llama Response:")
print(result["message"]["content"])