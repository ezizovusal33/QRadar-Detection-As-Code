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

def check_api_root():
    # QRadar API-nin kök ünvanını yoxlayırıq ki, mövcud qovluqları görək
    test_url = f"https://{QRADAR_IP}/api/"
    print(f"API Kök ünvanı yoxlanılır: {test_url}")
    
    response = requests.get(test_url, headers=headers, verify=False)
    print(f"Status: {response.status_code}")
    # Cavab uzun ola biləcəyi üçün ilk 1000 simvolunu çap edirik
    print(f"Cavab: {response.text[:1000]}")

if __name__ == "__main__":
    check_api_root()
