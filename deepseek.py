from openai import OpenAI

cliente = OpenAI(api_key="aca va tu api key", 
                 base_url="https://openrouter.ai/api/v1")

chat = cliente.chat.completions.create(
    model="deepseek/deepseek-r1:free",
    messages=[
        {
            "role":"user",
            "content" : "Creame un codigo de python que calcule el factorial de un numero"
        }
    ]
)

# print(chat)
if __name__ == "__main__":
    print(chat.choices[0].message.content)