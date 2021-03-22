# import json
#
# nama_mhs = []
# nim_mhs = []
# angkatan_mhs = []
#
# with open('data.json') as f:
#     data = json.load(f)
#
# print(data['mahasiswa'][0]['nama'])
#
#
# print(nim_mhs)

import requests

url = 'https://google.com'

respon = requests.get(url)

print(respon.headers)
