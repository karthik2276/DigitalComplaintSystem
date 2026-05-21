import requests, json

base = 'http://127.0.0.1:5000'

# 1. Login as user1 (email=user1@example.com, password=user123)
login_url = f'{base}/login'
login_data = {'email': 'user1@example.com', 'password': 'user123'}
session = requests.Session()
resp = session.post(login_url, data=login_data)
print('Login status:', resp.status_code)
print('Login response snippet:', resp.text[:200])

# 2. Submit a complaint via user dashboard (POST to /dashboard)
complaint_url = f'{base}/dashboard'
complaint_data = {
    'title': 'Test Complaint from script',
    'description': 'Automated test complaint submission.',
    'category': '1',  # assuming category id 1 exists
    'priority': 'High'
}
resp2 = session.post(complaint_url, data=complaint_data)
print('Complaint submission status:', resp2.status_code)
print('Complaint response snippet:', resp2.text[:200])

# 3. Verify complaint appears via API (admin login)
admin_login_data = {'email': 'admin@example.com', 'password': 'admin123'}
admin_session = requests.Session()
admin_session.post(login_url, data=admin_login_data)
api_url = f'{base}/api/complaints'
api_resp = admin_session.get(api_url)
print('API complaints status:', api_resp.status_code)
print('API response snippet:', api_resp.text[:500])
