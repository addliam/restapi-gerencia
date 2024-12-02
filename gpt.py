import os
from openai import OpenAI
from dotenv import load_dotenv


class Gpt:
    def __init__(self) -> None:
        load_dotenv()
        self.prompt_system = """Analiza historial de gastos y datos personales en formato CSV, para generar recomendaciones financieras personalizadas y optimizar hábitos de gasto. Formato de salida JSON:
        { "recomendaciones": [ {"titulo": "", "descripcion": ""} ] }
        Genera tres objetos de recomendación en esta lista.
        """
        pass

    def answer(self, msg: str) -> str:
        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": self.prompt_system,
                },
                {
                    "role": "user",
                    "content": msg,
                }
            ],
            model="gpt-3.5-turbo",
        )
        response = chat_completion.choices[0].message.content
        return response
