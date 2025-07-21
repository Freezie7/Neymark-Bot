from openai import OpenAI
from config import OPENAI_KEY

client = OpenAI(api_key=OPENAI_KEY)

async def analyze_with_chatgpt(text: str) -> str:
    """Анализ текста через ChatGPT"""
    try:
        prompt = f"{text}"
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "Ты бот "},
                {"role": "user", "content": prompt}
            ],
        )
        return response.choices[0].message.content
    
    except Exception as e:
        return f"⚠️ Не удалось выполнить анализ: {str(e)}"