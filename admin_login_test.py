import requests
from bs4 import BeautifulSoup

base_url = 'http://127.0.0.1:5000'
login_url = f'{base_url}/login'
admin_dashboard_url = f'{base_url}/admin_dashboard'

session = requests.Session()
# Get login page to get any hidden fields / cookies (if any)
session.get(login_url)

login_data = {
    'email': 'admin@example.com',
    'password': 'admin123'
}
resp = session.post(login_url, data=login_data)
print('Login response:', resp.status_code)
# Follow redirect if any
if resp.history:
    print('Redirect chain:', [r.status_code for r in resp.history])

# Access admin dashboard
admin_resp = session.get(admin_dashboard_url)
print('Admin dashboard response:', admin_resp.status_code)
if admin_resp.status_code == 200:
    # Print first part of page title or snippet
    soup = BeautifulSoup(admin_resp.text, 'html.parser')
    title = soup.title.string if soup.title else 'No title'
    print('Page title:', title)
    # Print a snippet of the HTML
    print('Snippet:', admin_resp.text[:500])
else:
    print('Failed to load admin dashboard')
