import re

import requests
from bs4 import BeautifulSoup


def filter_string(input_string: str) -> str:
    allowed_chars = []
    for j in "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя1234567890 !,.?-":
        allowed_chars.append(j)
    input_string = re.sub(r'^\d+.\s+', '', input_string)
    return ''.join([char for char in input_string if char in allowed_chars])


repetition = 0
response = {}
soup = BeautifulSoup(
    requests.get('https://theportalwiki.com/wiki/GLaDOS_voice_lines/ru').text,
    features='html.parser'
)
for li in soup.find_all('li'):
    try:
        i = li.find('i').text
        url = li.find('span', class_=['audio-player']).find('a')['href']
        if i not in response.keys():
            response[i] = url
        else:
            repetition += 1
    except AttributeError:
        pass
    try:
        i = li.find('a').text
        url = li.find('a')['href']
        if i not in response.keys():
            response[i] = url
        else:
            repetition += 1
    except AttributeError:
        pass
print(f'Количество найденный элементов: {len(response)}')
print(f'Количество повторении: {repetition}')
with open('MyTTSDataset/transcript.txt', 'w') as f:
    for index, (key, value) in enumerate(response.items()):
        try:
            response = requests.get(value)
            if response.status_code == 200:
                key = filter_string(key)
                if key and len(key.replace(" ", "")) > 3:
                    with open(f"MyTTSDataset/wavs/wav{index}.wav", 'wb') as file:
                        file.write(response.content)
                    f.write(f'wav{index}|{key}\n')
        except requests.exceptions.MissingSchema:
            pass
        except requests.exceptions.InvalidSchema:
            pass
