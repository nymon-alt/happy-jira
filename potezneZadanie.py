# Zadanie: "Smart Project Auditor"
# Twoim celem jest napisanie skryptu w Pythonie, który wykona głęboką analizę konkretnego projektu (lub wszystkich projektów) i wygeneruje raport w formie nowego zadania (Issue) z listą anomalii, a następnie automatycznie naprawi wybrane z nich.

# Funkcjonalności do zaimplementowania:
#1 Wykrywanie "Zombiaków": Znajdź zadania, które są w statusie "To Do", ale nie miały żadnej aktualizacji (komentarza, zmiany statusu, logowania czasu) od ponad 1 dnia.

#2 Kontrola hierarchii (Epic Link Integrity): Wykryj wszystkie zadania typu Story lub Task, które nie są przypisane do żadnego Epica (tzw. "orphans").

#3 Weryfikacja estymacji: Znajdź zadania, bugi, storki zamknięte ("Done"), które nie mają zalogowanego czasu (worklog) lub nie miały uzupełnionego pola Original Estimate.

#4 Dynamiczny Raport HTML: Skrypt powinien zebrać te dane i stworzyć jeden zbiorczy bilet w Jirze (np. w projekcie administracyjnym), w którego opisie znajdzie się sformatowana tabela z wynikami.

#5 Auto-Komentarz: Skrypt powinien dopisać komentarz do każdego "Zombiaka", oznaczając przypisaną do niego osobę (mention @username): "Cześć, czy to zadanie jest nadal aktualne? Brak aktywności od 30 dni."

# This code sample uses the 'requests' library:
# http://docs.python-requests.org

import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth
import json

load_dotenv()

domain = "https://nymon.atlassian.net/rest/api/3/"
email = os.getenv('JIRA_EMAIL')
api_key = os.getenv('JIRA_API_KEY')
auth = HTTPBasicAuth(email, api_key)
headers = {
  "Accept": "application/json"
}

def zombieTask(d = domain, a = auth, h = headers):
    url = f"{d}search/jql"
    query = {
    'jql': 'project = HAP AND type IN (Story, Task) AND status = "To Do" AND NOT updated >= -24h ORDER BY cf[10019] ASC',
    'fields': 'summary'
    }
    response = requests.request(
        "GET",
        url,
        headers=h,
        params=query,
        auth=a
    )   
    result = []
    data = response.json()
    for item in data['issues']:
        result.append(item['id'])
    return result

def orphanCheck(d = domain, a = auth, h = headers):
    url = f"{d}search/jql"
    query = {
    'jql': 'project = HAP AND type IN (Story, Task) AND parent = empty ORDER BY cf[10019] ASC',
    'fields': 'summary'
    }
    response = requests.request(
        "GET",
        url,
        headers=h,
        params=query,
        auth=a
    )   
    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

def estimateCheck(d = domain, a = auth, h = headers):
    url = f"{d}search/jql"
    query = {
    'jql': 'project = HAP AND type IN (Story, Task, Bug) AND statuscategory = Complete AND (timeestimate = EMPTY OR timespent = EMPTY) ORDER BY cf[10019] ASC',
    'fields': 'summary'
    }
    response = requests.request(
        "GET",
        url,
        headers=h,
        params=query,
        auth=a
    )   
    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

def autoComment(d = domain, a = auth, h = headers, z = allZombies):
    for item in z:
        url = f"{d}issue/{item}/comment"
        payload = json.dumps({
            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": "zombiaczek, ping"
                            }
                        ]
                    }
                ]
            }
        })

    response = requests.request(
       "POST",
       url,
       data=payload,
       headers=headers,
       auth=auth
    )
    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

