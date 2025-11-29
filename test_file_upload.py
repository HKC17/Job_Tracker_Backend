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

# Create a test file
with open('test_resume.txt', 'w') as f:
    f.write('This is a test resume file.')

# Test 1: Upload generic file
print('1. Uploading test file...')
with open('test_resume.txt', 'rb') as f:
    files = {'file': f}
    data = {'file_type': 'document'}
    response = requests.post(
        f'{BASE_URL}/applications/upload/',
        headers=headers,
        files=files,
        data=data
    )

print(f'Status: {response.status_code}')
if response.status_code == 201:
    file_data = response.json()
    print(f'✅ File uploaded: {file_data["filename"]}')
    print(f'   URL: {file_data["file_url"]}\n')
else:
    print(f'❌ Error: {response.text}\n')

# Test 2: Upload resume
print('2. Uploading resume...')
with open('test_resume.txt', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        f'{BASE_URL}/applications/upload-resume/',
        headers=headers,
        files=files
    )

print(f'Status: {response.status_code}')
if response.status_code == 201:
    print(f'✅ Resume uploaded and profile updated\n')
else:
    print(f'❌ Error: {response.text}\n')

# Test 3: Attach file to application
print('3. Getting first application...')
response = requests.get(f'{BASE_URL}/applications/', headers=headers)
if response.status_code == 200:
    applications = response.json()['results']
    if applications:
        app_id = applications[0]['id']
        print(f'Found application: {app_id}')
        
        print('   Attaching file to application...')
        with open('test_resume.txt', 'rb') as f:
            files = {'file': f}
            response = requests.post(
                f'{BASE_URL}/applications/{app_id}/attach/',
                headers=headers,
                files=files
            )
        
        print(f'   Status: {response.status_code}')
        if response.status_code == 201:
            print(f'   ✅ File attached to application\n')
        else:
            print(f'   ❌ Error: {response.text}\n')

print('✅ All file upload tests completed!')
