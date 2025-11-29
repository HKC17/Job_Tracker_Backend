import requests
import json

BASE_URL = 'http://127.0.0.1:8000/api'

# Login first (use your existing user)
print('1. Logging in...')
response = requests.post(f'{BASE_URL}/auth/login/', json={
    'email': 'testuser@example.com',
    'password': 'SecurePass123!'
})

if response.status_code != 200:
    print('❌ Login failed. Make sure you have a user registered.')
    exit()

access_token = response.json()['access']
headers = {'Authorization': f'Bearer {access_token}'}

print('✅ Logged in successfully\n')

# Test all analytics endpoints
print('=' * 50)
print('TESTING ANALYTICS ENDPOINTS')
print('=' * 50)

# 1. Dashboard Stats
print('\n1. Dashboard Statistics')
print('-' * 50)
response = requests.get(f'{BASE_URL}/analytics/dashboard/', headers=headers)
print(f'Status: {response.status_code}')
if response.status_code == 200:
    data = response.json()
    print(f'Total Applications: {data["total_applications"]}')
    print(f'Success Rate: {data["success_rate"]}%')
    print(f'Response Rate: {data["response_rate"]}%')
    print(f'Last 30 Days: {data["applications_last_30_days"]}')
    print(f'Avg Days in Pipeline: {data["average_days_in_pipeline"]}')
    print(f'Status Breakdown: {data["status_breakdown"]}')
    print(f'Top Companies: {data["top_companies"]}')
    print(f'Top Sources: {data["top_sources"]}')

# 2. Applications Over Time
print('\n2. Applications Over Time (Monthly)')
print('-' * 50)
response = requests.get(f'{BASE_URL}/analytics/applications-over-time/?period=month', headers=headers)
print(f'Status: {response.status_code}')
if response.status_code == 200:
    data = response.json()
    for item in data:
        print(f"  {item['period']}: {item['count']} applications")

# 3. Success Rate Over Time
print('\n3. Success Rate Over Time')
print('-' * 50)
response = requests.get(f'{BASE_URL}/analytics/success-rate/', headers=headers)
print(f'Status: {response.status_code}')
if response.status_code == 200:
    data = response.json()
    for item in data:
        print(f"  {item['period']}: {item['success_rate']}% ({item['success']}/{item['total']})")

# 4. Skills Demand
print('\n4. Skills Demand')
print('-' * 50)
response = requests.get(f'{BASE_URL}/analytics/skills/', headers=headers)
print(f'Status: {response.status_code}')
if response.status_code == 200:
    data = response.json()
    for item in data[:10]:
        print(f"  {item['skill']}: {item['count']} times")

# 5. Timeline Analysis
print('\n5. Timeline/Interview Analysis')
print('-' * 50)
response = requests.get(f'{BASE_URL}/analytics/timeline/', headers=headers)
print(f'Status: {response.status_code}')
if response.status_code == 200:
    data = response.json()
    for item in data:
        print(f"  {item['event_type']}: {item['count']} events")

# 6. Salary Insights
print('\n6. Salary Insights')
print('-' * 50)
response = requests.get(f'{BASE_URL}/analytics/salary/', headers=headers)
print(f'Status: {response.status_code}')
if response.status_code == 200:
    data = response.json()
    print(f"  Average Min: ")
    print(f"  Average Max: ")
    print(f"  Lowest: ")
    print(f"  Highest: ")
    print(f"  Total with Salary: {data['total_with_salary']}")

# 7. Response Time
print('\n7. Response Time Analysis')
print('-' * 50)
response = requests.get(f'{BASE_URL}/analytics/response-time/', headers=headers)
print(f'Status: {response.status_code}')
if response.status_code == 200:
    data = response.json()
    print(f"  Average: {data['average_days']} days")
    print(f"  Fastest: {data['fastest']} days")
    print(f"  Slowest: {data['slowest']} days")
    print(f"  Total Responses: {data['total_responses']}")

print('\n' + '=' * 50)
print('✅ ALL ANALYTICS TESTS COMPLETED!')
print('=' * 50)
