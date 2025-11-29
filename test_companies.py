import requests

BASE_URL = 'http://127.0.0.1:8000/api'

# Login
print('Logging in...')
response = requests.post(f'{BASE_URL}/auth/login/', json={
    'email': 'demo@example.com',
    'password': 'DemoPass123!'
})

access_token = response.json()['access']
headers = {'Authorization': f'Bearer {access_token}'}

print('✅ Logged in\n')

# 1. Sync companies from applications
print('1. Syncing companies from applications...')
response = requests.post(f'{BASE_URL}/companies/sync/', headers=headers)
print(f'Status: {response.status_code}')
if response.status_code == 200:
    print(f'✅ {response.json()["message"]}\n')

# 2. Get all companies
print('2. Getting all companies...')
response = requests.get(f'{BASE_URL}/companies/', headers=headers)
print(f'Status: {response.status_code}')
print(f'Total companies: {response.json()["count"]}\n')

# 3. Search companies
print('3. Searching for "Google"...')
response = requests.get(f'{BASE_URL}/companies/search/?q=Google', headers=headers)
print(f'Status: {response.status_code}')
if response.status_code == 200:
    companies = response.json()
    for company in companies:
        print(f'  - {company["name"]} ({company.get("application_count", 0)} applications)')
print()

# 4. Autocomplete
print('4. Autocomplete "Goo"...')
response = requests.get(f'{BASE_URL}/companies/autocomplete/?q=Goo', headers=headers)
print(f'Status: {response.status_code}')
if response.status_code == 200:
    results = response.json()
    for result in results:
        print(f'  - {result["name"]}')
print()

# 5. Industry breakdown
print('5. Industry breakdown...')
response = requests.get(f'{BASE_URL}/companies/industry-breakdown/', headers=headers)
print(f'Status: {response.status_code}')
if response.status_code == 200:
    data = response.json()
    for item in data[:5]:
        print(f'  {item["industry"]}: {item["count"]} companies')
print()

# 6. Top companies
print('6. Top 5 companies by applications...')
response = requests.get(f'{BASE_URL}/companies/top/?limit=5', headers=headers)
print(f'Status: {response.status_code}')
if response.status_code == 200:
    companies = response.json()
    for company in companies:
        print(f'  {company["name"]}: {company["application_count"]} applications')

print('\n✅ All company tests completed!')
