import json

html = ''

with open('data.json') as f:
    data = json.load(f)

for d in data['mahasiswa']:
    html += f"<tr><td>{d['nim']}</td><td>{d['nama']}</td><td>{d['angkatan']}</td></tr>"

print(html)
