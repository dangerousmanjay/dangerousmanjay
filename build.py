import os

import base64
import random
import requests

BADGE = '[![182](https://img.shields.io/badge/%EC%8B%A4%EC%A2%85%EC%8B%A0%EA%B3%A0%EB%8A%94%20%EA%B5%AD%EB%B2%88%EC%97%86%EC%9D%B4-182-blue)](http://safe182.go.kr/index.do)'

if __name__ == '__main__':
    url = f"http://www.safe182.go.kr/api/lcm/findChildList.do?esntlId={os.environ['API_ID']}&authKey={os.environ['API_TOKEN']}"

    # find total count
    response = requests.post(url + '&rowSize=1')
    # get rondom missing person
    response = requests.post(
        url + f"&rowSize=1&page={random.randint(1, response.json()['totalCount'])}"
    )
    data = response.json()['list'][0]

    for key, value in data.items():
        if key in ('occrAdres', 'etcSpfeatr'):
            data[key] = value.replace('/', '.').replace('\n', '</br>')
        elif key == 'occrde':
            data[key] = value[:4] + '/' + value[4:6] + '/' + value[6:]

    txt = [
        f"|**이름**|{data['nm']}|\n",
        f"|**성별**|{data['sexdstnDscd']}|\n",
        f"|**현재 나이**|{data['ageNow']}|\n",
        f"|**당시 나이**|{data['age']}|\n",
        f"|**실종일**|{data['occrde']}|\n",
        f"|**실종 장소**|{data['occrAdres']}|\n",
        f"|**특이사항**|{data['etcSpfeatr']}|\n",
    ]

    with open('missing_person.jpg', 'wb') as f:
        f.write(base64.b64decode(data['tknphotoFile']))

    with open("README.md", 'w') as f:
        f.write(BADGE)
        f.write('\n\n')
        f.write('# MISSIONG PERSON')
        f.write('\n\n')
        f.write('<img src="./missing_person.jpg">')
        f.write('\n\n')
        f.write('# INFO')
        f.write('\n\n')
        f.write('|🔑|💎|\n|--|:--:|\n')
        f.writelines(txt)
