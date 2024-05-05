import os

import requests
from bs4 import BeautifulSoup

# URL веб-страницы, которую нужно спарсить
url = 'https://theportalwiki.com/wiki/GLaDOS_voice_lines/ru'

# Получаем содержимое страницы
response = requests.get(url)
response.raise_for_status()  # Проверка на успешный запрос

# Парсим HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Находим все теги <a>
links = soup.find_all('a')

# Фильтруем ссылки, которые заканчиваются на .wav
wav_links = [
    link.get('href') for link in links if link.get('href') and link.get('href').endswith('.wav')
]

# Создаем директорию для сохранения файлов, если её нет
os.makedirs('wav_files', exist_ok=True)

# Скачиваем каждый wav-файл
for wav_link in wav_links:
    # Получаем имя файла из URL
    filename = wav_link.split('/')[-1]
    file_path = os.path.join('wav_files', filename)

    # Скачиваем файл
    response = requests.get(wav_link)
    response.raise_for_status()

    # Сохраняем файл
    with open(file_path, 'wb') as file:
        file.write(response.content)

    print(f"Downloaded {filename}")
