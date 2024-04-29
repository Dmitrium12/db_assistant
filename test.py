import asyncio
import re

import ollama
import yaml


def load_commands(file_path):
    with open(file_path) as file:
        data = yaml.safe_load(file)
        answers = {}
        command_mapping = {}
        idx = 1
        for category, items in data.items():
            answers[idx] = items
            command_mapping[idx] = category
            idx += 1
        return answers, command_mapping


async def chat(answers: dict[int, str], request: str = 'музычку пожалуйста') -> str:
    answers_str = ''.join([f'{key}. {", ".join(value)}\n' for key, value in answers.items()])
    messages = [
        {
            'role': 'system',
            'content': 'Пожалуйста, просмотрите список доступных команд и '
                       'выберите подходящую команду, указав ее номер. '
                       'Вы можете выбрать одну команду или несколько команд одновременно. '
                       'В ответе укажите только номер или номера команд, '
                       'например: "1" или "1, 3, 5". Вот список доступных команд:\n' + answers_str
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
            'mirostat_tau': 100.0,
            'repeat_last_n': 2,
            'num_predict': 20
        }
    )
    return response.get("message").get("content")


async def main():
    answers, command_mapping = load_commands('commands.yaml')
    number = None
    while not number:
        response_content = await chat(answers, "останови музыку и скажи погоду")
        number = [
            int(i)
            for i in re.findall(r'\d+', response_content)
            if int(i) in answers.keys()
        ]
    command_names = [command_mapping[n] for n in number]
    print(f"Выбранный номер: {command_names}")


if __name__ == '__main__':
    ollama.pull("llama3:8b")
    asyncio.run(main())
