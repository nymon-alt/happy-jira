# Zadanie 7: "Generator Sub-tasków" (Hierarchy)
# Cel: Napisz funkcję, która dla podanego klucza zadania (Parent Task) automatycznie utworzy 3 podzadania (np. "Analiza", "Implementacja", "Testy").

import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth
import json

load_dotenv()

url = "https://nymon.atlassian.net/rest/api/3/issue"
url_issue = "https://nymon.atlassian.net/rest/api/2/issue/HAP-17"

email = os.getenv("JIRA_EMAIL")
api_key = os.getenv("JIRA_API_KEY")

auth = HTTPBasicAuth(email, api_key)

headers = {
  "Accept": "application/json",
  "Content-Type": "application/json"
}

def getSubtaskIds(u = url_issue, a = auth, h = headers):
   response = requests.request(
   "GET",
   url = u,
   headers = h,
   auth = a
   )
   data = response.json()
   issueType = data['fields']['issuetype']['id']
   print(issueType)

subtaskTitles = ["Analiza", "Implementacja", "Testy"]

for item in subtaskTitles:
    payload = json.dumps( {
    "fields": {
    "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "text": f"{item} for parent task.",
                                "type": "text"
                            }
                        ]
                    }
                ]
            },
    "issuetype": {
      "id": "10011"
    },
    "parent": {
      "key": "HAP-7"
    },
    "priority": {
      "id": "4"
    },
    "project": {
      "key": "HAP"
    },
    "summary": item,
    "timetracking": {
      "originalEstimate": "10",
      "remainingEstimate": "5"
    },
    },
    })
    response = requests.request(
    "POST",
    url,
    data=payload,
    headers=headers,
    auth=auth
    )
data = response.json()
if response.status_code == 201:
    print(f"podzadania: {subtaskTitles} zostaly utworzone!")
else:
    print("something fucky: ", data)

