import requests
import os

# Test the post-audio-get endpoint
url = "http://127.0.0.1:8000/post-audio-get/"

print("Testing post-audio-get endpoint...")
print(f"URL: {url}")

try:
    response = requests.get(url, timeout=30)

    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")

    if response.status_code == 200:
        print("✅ Endpoint responded successfully!")
        try:
            data = response.json()
            print("Response JSON:")
            print(data)
        except:
            print("Response Text:")
            print(response.text)
    else:
        print(f"❌ Endpoint returned error {response.status_code}")
        print("Response Text:")
        print(response.text)

except requests.exceptions.ConnectionError:
    print("❌ Connection error - server may not be running")
except requests.exceptions.Timeout:
    print("❌ Request timed out")
except Exception as e:
    print(f"❌ Error testing endpoint: {e}")
