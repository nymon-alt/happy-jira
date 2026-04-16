# Zadanie 1: "Szybki podgląd" (GET)
# Cel: Pobierz szczegóły konkretnego zgłoszenia (np. BUG-101) i wyświetl jego status oraz osobę przypisaną.

import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth
import json

load_dotenv()

api_key = os.getenv("JIRA_API_KEY")
email = os.getenv("JIRA_EMAIL")

auth = HTTPBasicAuth(email, api_key)

url = "https://nymon.atlassian.net/rest/api/3/issue/HAP-5"

headers = {
  "Accept": "application/json",
  "Content-Type": "application/json"
}

response = requests.request(
   "GET",
   url,
   headers=headers,
   auth=auth
)

#print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

data = response.json()
name = data['fields'].get('summary')
status = data['fields'].get('status').get('name')
assignee = data['fields'].get('assignee').get('displayName')
print(f"""Zgloszenie o nazwie:
{name} 
jest w statusie:
{status} 
a osoba przypisana to 
{assignee}""")