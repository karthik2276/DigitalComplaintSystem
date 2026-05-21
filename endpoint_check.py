import requests, json
endpoints = ['/login', '/api/docs', '/api/complaints']
base = 'http://127.0.0.1:5000'
for ep in endpoints:
    try:
        r = requests.get(base + ep)
        print(f'{ep} -> {r.status_code}')
        ct = r.headers.get('Content-Type', '')
        if 'application/json' in ct:
            print(json.dumps(r.json(), indent=2)[:200])
        else:
            print(r.text[:200])
    except Exception as e:
        print(f'Error on {ep}: {e}')
