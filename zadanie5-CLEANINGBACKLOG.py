# Zadanie 5: "Masowe sprzątanie backlogu"
# Cel: Znajdź wszystkie zadania typu "Task", które nie były aktualizowane od ponad 10 godzin i dodaj do nich etykietę (label) stale_task.

import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth
import json

load_dotenv()

url_search = "https://nymon.atlassian.net/rest/api/3/search/jql"
api_key = os.getenv("JIRA_API_KEY")
email = os.getenv("JIRA_EMAIL")
auth = HTTPBasicAuth(email, api_key)

headers = {
  "Accept": "application/json",
  "Content-Type": "application/json"
}

def searchTaskBelowUpdate10h(url=url_search,credensials=auth, h=headers):
    query = {
      'jql': 'project = HAP AND updated <= -10h ORDER BY updated DESC, cf[10019] ASC',
      'fields': 'summary',
    }

    response = requests.request(
    "GET",
    url,
    headers=h,
    params=query,
    auth=credensials
    )
    data = response.json()
    itemsList = []
    for item in data['issues']:
        itemsList.append(item['self'])
    return itemsList

everyURL = searchTaskBelowUpdate10h()

def addingLabelsToTaskBelow10h(auth, headers, u):
        payload = json.dumps({
        "update": {
        "labels": [
        { "add": "stable_task" },]
        }
        })
        response = requests.request(
        "PUT",
        url = u,
        data=payload,
        headers=headers,
        auth=auth)
        data = response.json()
        print(data)
        if response.status_code == 204:
            print(f"set label: ok")
        else:
            print(f"set label: nok {response.status_code}")
            print(response.text)

for url in everyURL:
    addingLabelsToTaskBelow10h(auth,headers,url)
