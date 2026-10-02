import os
import json
import requests
import urllib3

# Sertifikat xəbərdarlıqlarını gizlədirik
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# GitHub Secrets-dən məlumatları oxuyuruq
QRADAR_IP = os.environ.get("QRADAR_IP")
TOKEN = os.environ.get("QRADAR_TOKEN")

headers = {
    'SEC': TOKEN,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

RULES_DIR = "qradar/rules"

def sync_rules():
    base_url = f"https://{QRADAR_IP}/api/analytics/rules"
    
    print("QRadar-dakı mövcud qaydalar əldə edilir...")
    response = requests.get(base_url, headers=headers, verify=False)
    
    if response.status_code != 200:
        print(f"Xəta: Qaydalar çəkilə bilmədi. Status: {response.status_code}")
        return

    existing_rules = response.json()
    existing_rules_map = {rule['name']: rule['id'] for rule in existing_rules}

    # GitHub-dakı JSON fayllarını oxuyuruq
    for filename in os.listdir(RULES_DIR):
        if filename.endswith(".json"):
            file_path = os.path.join(RULES_DIR, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                rule_data = json.load(f)
            
            rule_name = rule_data.get("name")
            rule_id = rule_data.get("id")
            
            # 1. Əgər JSON faylında ID birbaşa qeyd olunubsa
            if rule_id:
                update_url = f"{base_url}/{rule_id}"
                print(f"'{rule_name}' qaydası ID ({rule_id}) ilə yenilənir (PUT)...")
                update_res = requests.put(update_url, headers=headers, json=rule_data, verify=False)
                if update_res.status_code in [200, 201]:
                    print(f"Uğurlu! '{rule_name}' yeniləndi.")
                else:
                    print(f"Yenilənmə xətası: {update_res.text}")
            
            # 2. ID yoxdursa, amma QRadar-da adı mövcuddursa
            elif rule_name in existing_rules_map:
                r_id = existing_rules_map[rule_name]
                update_url = f"{base_url}/{r_id}"
                print(f"'{rule_name}' qaydası ada görə tapıldı (ID: {r_id}), yenilənir...")
                update_res = requests.put(update_url, headers=headers, json=rule_data, verify=False)
                if update_res.status_code in [200, 201]:
                    print(f"Uğurlu! '{rule_name}' yeniləndi.")
                else:
                    print(f"Yenilənmə xətası: {update_res.text}")
            
            # 3. Yeni qaydadırsa
            else:
                print(f"'{rule_name}' tapılmadı, yeni qayda olaraq yaradılır...")
                create_res = requests.post(base_url, headers=headers, json=rule_data, verify=False)
                if create_res.status_code in [200, 201]:
                    print(f"Uğurlu! Yeni qayda yaradıldı.")
                else:
                    print(f"Yaratma xətası: {create_res.text}")

if __name__ == "__main__":
    sync_rules()
