# Zadanie 6: "Logowanie czasu (Worklog)"
# Cel: Dodaj wpis o przepracowaniu 2 godzin i 30 minut do konkretnego buga, z opisem wykonanej pracy.

import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth
import json

load_dotenv()

url_getPutWork = "https://nymon.atlassian.net/rest/api/3/issue/HAP-15/worklog/10001"
url_getWorklogID = "https://nymon.atlassian.net/rest/api/3/issue/HAP-15/worklog"
api_key = os.getenv("JIRA_API_KEY")
email = os.getenv("JIRA_EMAIL")
auth = HTTPBasicAuth(email, api_key)

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
    }

def getWorklogID(u = url_getWorklogID, a = auth, h = headers):
    response = requests.request(
    "GET",
    url=u,
    headers=h,
    auth=a
    )
    data = response.json()
    for item in data['worklogs']:
        print(item['id'])

def putWork(u = url_getPutWork, a = auth, h = headers):
    payload = json.dumps( {
    "comment": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "text": "I did some work here.",
                            "type": "text"
                        }
                    ]
                }
            ]
        },
    "started": "2026-04-11T11:35:00.000+0000",
    "timeSpentSeconds": 12000,
    } )
    response = requests.request(
    "PUT",
    url = u,
    data=payload,
    headers=h,
    auth=a
    )
    data = response.json()
    if response.status_code == 200:
        print("worklog zostal pomyslnie dodany!")
    else:
        print("cos nie pyklo: ", data)

#getWorklogID()
putWork()




