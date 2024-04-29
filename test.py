import asyncio
import re

import ollama


async def chat(answers: dict[int, str], request: str = 'музычку пожалуйста') -> str:
    answers_str = ''.join([f'{key}. {value}\n' for key, value in answers.items()])
    messages = [
        {
            'role': 'system',
            'content': 'Ты должен ответить на вопрос пользователя числом или набором чисел.'
                       'Пример твоего ответа: 1.'
                       'Ещё один пример: 4 и 3'
                       ' Вот список:\n' + answers_str
        },
        {
            'role': 'user',
            'content': request
        }
    ]
    async_client = ollama.AsyncClient()
    response = await async_client.chat(
        model='llama3:8b',
        messages=messages,
        options={
            'temperature': 0.5,
        }
    )
    return response.get("message").get("content")


async def main():
    answers = {
        1: "включить музыку",
        2: "остановить музыку",
        3: "следующая композиция",
        4: "предыдущая композиция",
        5: 'погода',
        99: "ничего из этого"
    }
    number = None
    while not number:
        response_content = await chat(answers, "останови музыку и скажи погоду")
        print(response_content)
        number = [
            int(i)
            for i in re.findall(r'\d+', response_content)
            if int(i) in answers.keys()
        ]
        if not number:
            print("Не удалось определить номер. Пожалуйста, попробуйте снова.")
    print(f"Выбранный номер: {number}")


if __name__ == '__main__':
    ollama.pull("llama3:8b")
    asyncio.run(main())
