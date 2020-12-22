import os

import base64
import random
import requests

BASE_URL = f'http://www.safe182.go.kr/api/lcm/findChildList.do?esntlId={os.environ["API_ID"]}&authKey={os.environ["API_TOKEN"]}'
BADGE = '[![182](https://img.shields.io/badge/%EC%8B%A4%EC%A2%85%EC%8B%A0%EA%B3%A0%EB%8A%94%20%EA%B5%AD%EB%B2%88%EC%97%86%EC%9D%B4-182-blue)](http://safe182.go.kr/index.do)'


def fetch_total():
    response = requests.post(BASE_URL + '&rowSize=1')

    return response.json()['totalCount']


def fetch_random_data():
    response = requests.post(
        BASE_URL + f'&rowSize=1&page={random.randint(1, fetch_total())}'
    )

    return response.json()['list'][0]


def process_data(data):
    for key, value in data.items():
        if key in ('occrAdres', 'etcSpfeatr'):
            data[key] = value.replace('/', '.').replace('\n', '</br>')
        elif key == 'occrde':
            data[key] = value[:4] + '/' + value[4:6] + '/' + value[6:]

    return data


def generate_image(data):
    with open('missing_person.jpg', 'wb') as f:
        f.write(base64.b64decode(data['tknphotoFile']))


def generate_readme(data):
    with open('README.md', 'w', -1, 'utf-8') as f:
        f.writelines(
            [
                BADGE,
                '\n\n',
                '# MISSING PERSON',
                '\n\n',
                '<img src="./missing_person.jpg">',
                '\n\n',
                '# INFO',
                '\n\n',
                '|🔑|💎|\n|--|:--:|\n',
                f'|**이름**|{data["nm"]}|\n',
                f'|**성별**|{data["sexdstnDscd"]}|\n',
                f'|**현재 나이**|{data["ageNow"]}|\n',
                f'|**당시 나이**|{data["age"]}|\n',
                f'|**실종일**|{data["occrde"]}|\n',
                f'|**실종 장소**|{data["occrAdres"]}|\n',
                f'|**특이사항**|{data["etcSpfeatr"]}|\n',
            ]
        )


def build():
    while True:
        data = process_data(fetch_random_data())
        if data['tknphotoFile'] is not None:
            break
    generate_image(data)
    generate_readme(data)


if __name__ == '__main__':
    build()
