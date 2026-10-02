import os
import json
import requests
import urllib3

# Sertifikat xəbərdarlıqlarını gizlədirik
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

QRADAR_IP = os.environ.get("QRADAR_IP")
TOKEN = os.environ.get("QRADAR_TOKEN")

headers = {
    'SEC': TOKEN,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def check_endpoints():
    # SIEM qrupunun əsas səhifəsini yoxlayaq ki, hansı endpoint-lər mövcuddur
    test_url = f"https://{QRADAR_IP}/api/siem"
    print(f"SIEM endpointləri yoxlanılır: {test_url}")
    
    response = requests.get(test_url, headers=headers, verify=False)
    print(f"Status: {response.status_code}")
    print(f"Cavab: {response.text}")

if __name__ == "__main__":
    check_endpoints()
