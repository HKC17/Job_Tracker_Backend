import requests
import json

BASE_URL = 'http://127.0.0.1:8000/api'

# 1. Register and Login
print('1. Registering user...')
response = requests.post(f'{BASE_URL}/auth/register/', json={
    'email': 'testuser@example.com',
    'password': 'SecurePass123!',
    'password_confirm': 'SecurePass123!',
    'first_name': 'Test',
    'last_name': 'User'
})
print(f'Status: {response.status_code}')
if response.status_code == 201:
    tokens = response.json()['tokens']
    access_token = tokens['access']
    print(f'✅ Got access token')
else:
    print('❌ Registration failed, trying login...')
    response = requests.post(f'{BASE_URL}/auth/login/', json={
        'email': 'testuser@example.com',
        'password': 'SecurePass123!'
    })
    access_token = response.json()['access']

headers = {'Authorization': f'Bearer {access_token}'}

# 2. Create an application
print('\n2. Creating application...')
response = requests.post(f'{BASE_URL}/applications/', 
    headers=headers,
    json={
        'company': {
            'name': 'Google',
            'website': 'https://google.com',
            'industry': 'Technology',
            'size': '10000+',
            'location': 'Mountain View, CA'
        },
        'job': {
            'title': 'Backend Developer',
            'description': 'Work on backend systems',
            'employment_type': 'full-time',
            'work_mode': 'remote',
            'experience_level': 'mid',
            'salary_min': 80000,
            'salary_max': 120000,
            'currency': 'USD'
        },
        'application': {
            'status': 'applied',
            'source': 'LinkedIn'
        },
        'requirements': {
            'skills_required': ['Python', 'Django', 'MongoDB'],
            'years_experience': 2
        },
        'notes': 'Really interested in this role!'
    }
)
print(f'Status: {response.status_code}')
if response.status_code == 201:
    app_data = response.json()
    app_id = app_data['id']
    print(f'✅ Created application with ID: {app_id}')
else:
    print(f'❌ Failed: {response.text}')
    exit()

# 3. Get all applications
print('\n3. Getting all applications...')
response = requests.get(f'{BASE_URL}/applications/', headers=headers)
print(f'Status: {response.status_code}')
print(f'Total applications: {response.json()["count"]}')

# 4. Get specific application
print(f'\n4. Getting application {app_id}...')
response = requests.get(f'{BASE_URL}/applications/{app_id}/', headers=headers)
print(f'Status: {response.status_code}')
print(f'Company: {response.json()["company"]["name"]}')

# 5. Update status
print('\n5. Updating status to interview...')
response = requests.patch(f'{BASE_URL}/applications/{app_id}/status/',
    headers=headers,
    json={
        'status': 'interview',
        'notes': 'Scheduled for next week'
    }
)
print(f'Status: {response.status_code}')
print(f'New status: {response.json()["application"]["status"]}')

# 6. Add timeline event
print('\n6. Adding timeline event...')
response = requests.post(f'{BASE_URL}/applications/{app_id}/timeline/',
    headers=headers,
    json={
        'event_type': 'phone_screen',
        'title': 'Phone screening with HR',
        'notes': 'Discussed compensation and role details',
        'interviewer_name': 'Jane Smith'
    }
)
print(f'Status: {response.status_code}')

# 7. Get statistics
print('\n7. Getting statistics...')
response = requests.get(f'{BASE_URL}/applications/stats/', headers=headers)
print(f'Status: {response.status_code}')
print(json.dumps(response.json(), indent=2))

print('\n✅ All tests completed!')
