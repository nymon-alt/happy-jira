# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth
import json

load_dotenv()

url = "https://nymon.atlassian.net/rest/api/3/issue/HAP-3/transitions"

api_key = os.getenv("JIRA_API_KEY")
email = os.getenv("JIRA_EMAIL")

auth = HTTPBasicAuth(email, api_key)

headers = {
  "Accept": "application/json",
  "Content-Type": "application/json"
}

def gettingTransiziton(url, auth, headers):
    response = requests.request(
    "GET",
    url,
    headers=headers,
    auth=auth)

    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

def settingTranzition(url, auth, headers):
    payload = json.dumps({
    "transition": {
    "id": "31" }
    })
    
    response = requests.request(
    "POST",
    url,
    data=payload,
    headers=headers,
    auth=auth)

    if response.status_code == 204:
        print("Sukces! Status został zmieniony.")
    else:
        print(f"Błąd: {response.status_code}")
        print(response.text)

gettingTransiziton(url, auth, headers)
settingTranzition(url, auth, headers)