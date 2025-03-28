import ollama
response = ollama.chat(
    model="deepseek-r1:8b",
    messages=[
        {"role": "user", "content": "Explicame la segunda ley de newton"},
    ],
)
print(response["message"]["content"])