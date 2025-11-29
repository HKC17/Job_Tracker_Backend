import requests

BASE_URL = 'http://127.0.0.1:8000/api'

# Login
response = requests.post(f'{BASE_URL}/auth/login/', json={
    'email': 'demo@example.com',
    'password': 'DemoPass123!'
})

access_token = response.json()['access']
headers = {'Authorization': f'Bearer {access_token}'}

print('✅ Logged in\n')

# Test 1: Export applications to CSV
print('1. Exporting applications to CSV...')
response = requests.get(
    f'{BASE_URL}/analytics/export/applications/csv/',
    headers=headers
)
print(f'Status: {response.status_code}')
if response.status_code == 200:
    with open('applications_export.csv', 'wb') as f:
        f.write(response.content)
    print(f'✅ Saved to applications_export.csv\n')

# Test 2: Export applications to PDF
print('2. Exporting applications to PDF...')
response = requests.get(
    f'{BASE_URL}/analytics/export/applications/pdf/',
    headers=headers
)
print(f'Status: {response.status_code}')
if response.status_code == 200:
    with open('applications_report.pdf', 'wb') as f:
        f.write(response.content)
    print(f'✅ Saved to applications_report.pdf\n')

# Test 3: Export analytics to CSV
print('3. Exporting analytics to CSV...')
response = requests.get(
    f'{BASE_URL}/analytics/export/analytics/csv/',
    headers=headers
)
print(f'Status: {response.status_code}')
if response.status_code == 200:
    with open('analytics_export.csv', 'wb') as f:
        f.write(response.content)
    print(f'✅ Saved to analytics_export.csv\n')

# Test 4: Export companies to CSV
print('4. Exporting companies to CSV...')
response = requests.get(
    f'{BASE_URL}/analytics/export/companies/csv/',
    headers=headers
)
print(f'Status: {response.status_code}')
if response.status_code == 200:
    with open('companies_export.csv', 'wb') as f:
        f.write(response.content)
    print(f'✅ Saved to companies_export.csv\n')

# Test 5: Export filtered applications (only "interview" status)
print('5. Exporting filtered applications (interview status)...')
response = requests.get(
    f'{BASE_URL}/analytics/export/applications/csv/?status=interview',
    headers=headers
)
print(f'Status: {response.status_code}')
if response.status_code == 200:
    with open('applications_interview.csv', 'wb') as f:
        f.write(response.content)
    print(f'✅ Saved to applications_interview.csv\n')

print('✅ All export tests completed!')
print('\nGenerated files:')
print('  - applications_export.csv')
print('  - applications_report.pdf')
print('  - analytics_export.csv')
print('  - companies_export.csv')
print('  - applications_interview.csv')
