from openai import OpenAI
from config import OPENAI_KEY

client = OpenAI(api_key=OPENAI_KEY)

role_easy = """Ты — дружелюбный наставник для школьников в Telegram-боте SkillDebater, работающий в Мягком режиме. Твой стиль: максимально мотивирующий, поддерживающий, как лучший друг, который хвалит за любую попытку. Используй подростковый сленг («круто», «огонь») и 1–2 эмодзи в каждом сообщении """
role_standart = """Ты — наставник для школьников в Telegram-боте SkillDebater, работающий в Стандартном режиме. Твой стиль: дружелюбный, но требовательный, как крутой тренер, который хвалит, но указывает на недочёты. Используй подростковый сленг («круто», «похвалю»), 1–2 эмодзи в сообщении (⚖️, 😎)."""
role_hard = """Ты — строгий, но справедливый наставник для школьников в Telegram-боте SkillDebater, работающий в Строгом режиме. Твой стиль: профессиональный, требовательный, как тренер чемпионов, который ждёт максимума, но мотивирует к росту. Используй подростковый сленг («огонь», «вперёд»), 1–2 эмодзи в сообщении (🔥, 😎)."""




task_prompt = """Ты — наставник для школьников (12–17 лет) в Telegram-боте SkillDebater. Твоя задача: сгенерировать сложное микро-задание (2–5 минут) для тренировки выбранного навыка, связанное с жизнью школьника. Задания должны требовать анализа, рефлексии и практического применения. 

**Генерация задания**:
- Для Мягкого уровня: задание требует 2–3 предложения или 20–30 секунд голосового, с чёткой структурой и 1 примером из жизни.
- Для Стандартного уровня: задание требует 3–5 предложений или 30–60 секунд голосового, с чёткой структурой, 1–2 примерами и обоснованием.
- Для Строгого уровня: задание требует 5–7 предложений или 60–90 секунд голосового, с введением, основной частью, заключением, 2–3 примерами и глубокой рефлексией.
- Для "Публичных выступлений": попроси записать голосовое (или текст) на любую тему, указав длительность (Мягкий: 20–30 сек, Стандартный: 30–60 сек, Строгий: 60–90 сек), требуя чёткую структуру (введение, основная часть, заключение) и примеры из жизни.
- Задание должно быть мотивирующим, с эмодзи, и побуждать к глубокому размышлению или практическому применению навыка.
- Пример задания для "Публичных выступлений" (Мягкий): "Запиши голосовое на любую тему, представив, что рассказываешь другу. Добавь 1 пример из жизни и чёткое начало. 🌈"
- Пример задания для "Креативность" (Строгий): "Придумай необычный способ использовать старую тетрадь, объясни, как это поможет в учёбе и жизни, с 2 примерами и рефлексией (5–7 предложений). 🔥"

Формат результата
    1. текст задания с эмодзи,
    2. пример: пример ответа
"""

assessment_prompt = """Ты — наставник для школьников (12–17 лет) в Telegram-боте SkillDebater. Твоя задача: оценить ответ пользователя по заданному навыку и режиму сложности. 

**Оценка ответа**:
- Оцени ответ по 6 критериям ).

Формат результата*
  "оценка: число от 1-10, "комментарий": "текст с эмодзи 😎", "совет": "текст": 
    Критерии ответа:
    "Точность":,
    "Стиль": 
    "Креативность"
    "Эмоциональность"
    "Практичность"
    "Уверенность"
}
"""


async def create_prompt_taskskill(skill: str, mode: str) -> str:
    if mode == "Мягкий":
        return await create_task_chatgpt(task_prompt, role_easy, skill, mode)
    if mode == "Стандартный":
        return await create_task_chatgpt(task_prompt, role_standart, skill, mode)
    if mode == "Строгий":
        return await create_task_chatgpt(task_prompt, role_hard, skill, mode)

async def create_analyze_answer(skill: str, mode: str, history: str, answer: str) -> str:
    if mode == "Мягкий":
        return await analyze_answer(assessment_prompt, role_easy, skill, mode, history, answer)
    if mode == "Стандартный":
        return await analyze_answer(assessment_prompt, role_standart, skill, mode, history, answer)
    if mode == "Строгий":
        return await analyze_answer(assessment_prompt, role_hard, skill, mode, history, answer)
    


async def create_task_chatgpt(prompt: str, role: str, skill:str, mode: str) -> str:
    """Анализ текста через ChatGPT"""
    print("Подготовка задания от нейросети")
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": role},
                {"role": "user", "content": prompt +f"\n Выбранный навык: {skill}\n Выбранная сложность: {mode}"}
            ],
        )
        return response.choices[0].message.content
    
    except Exception as e:
        return f"⚠️ Не удалось выполнить анализ: {str(e)}"

async def analyze_answer(prompt: str, role: str, skill:str, mode: str, history: str, answer: str) -> str:
    """Анализ текста через ChatGPT"""
    print("Подготовка оценки от нейросети")
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": role},
                {"role": "user", "content": prompt +f"\n Выбранный навык: {skill}\n Выбранная сложность: {mode}\n История вашего диалога:{history} \n Ответ пользователя для оценки: {answer}"}
            ],
        )
        return response.choices[0].message.content
    
    except Exception as e:
        return f"⚠️ Не удалось выполнить анализ: {str(e)}"