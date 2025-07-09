import os
import json
import requests
import datetime
import hashlib
import hmac
import base64

def send_log_to_loganalytics(log_type, log_data):
    workspace_id = os.environ.get('LOG_ANALYTICS_WORKSPACE_ID')
    shared_key = os.environ.get('LOG_ANALYTICS_SHARED_KEY')

    if not workspace_id or not shared_key:
        print("❌ Missing LOG_ANALYTICS_WORKSPACE_ID or LOG_ANALYTICS_SHARED_KEY environment variables.")
        return

    body = json.dumps(log_data)
    timestamp = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    string_to_hash = f'POST\n{len(body)}\napplication/json\nx-ms-date:{timestamp}\n/api/logs'
    bytes_to_hash = bytes(string_to_hash, encoding='utf-8')
    decoded_key = base64.b64decode(shared_key)
    encoded_hash = base64.b64encode(
        hmac.new(decoded_key, bytes_to_hash, digestmod=hashlib.sha256).digest()
    ).decode()

    uri = f'https://{workspace_id}.ods.opinsights.azure.com/api/logs?api-version=2016-04-01'
    headers = {
        'Content-Type': 'application/json',
        'Log-Type': log_type,
        'x-ms-date': timestamp,
        'Authorization': f'SharedKey {workspace_id}:{encoded_hash}'
    }

    print(f"Sending to Log Analytics: {len(log_data)} entries")
    print(f"POST {uri}")

    response = requests.post(uri, data=body, headers=headers)

    print(f"Response: {response.status_code} - {response.text}")

    if response.status_code not in [200, 202]:
        print(f"❌ Failed to send logs: {response.status_code} - {response.text}")
    else:
        print("✅ Logs sent to Log Analytics.")
