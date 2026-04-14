# Zadanie: "Smart Project Auditor"
# Twoim celem jest napisanie skryptu w Pythonie, który wykona głęboką analizę konkretnego projektu (lub wszystkich projektów) i wygeneruje raport w formie nowego zadania (Issue) z listą anomalii, a następnie automatycznie naprawi wybrane z nich.

# Funkcjonalności do zaimplementowania:
#1 Wykrywanie "Zombiaków": Znajdź zadania, które są w statusie "To Do", ale nie miały żadnej aktualizacji (komentarza, zmiany statusu, logowania czasu) od ponad -2h.

#2 Kontrola hierarchii (Epic Link Integrity): Wykryj wszystkie zadania typu Story lub Task, które nie są przypisane do żadnego Epica (tzw. "orphans").

#3 Weryfikacja estymacji: Znajdź zadania, bugi, storki zamknięte ("Done"), które nie mają zalogowanego czasu (worklog) lub nie miały uzupełnionego pola Original Estimate.

#4 Dynamiczny Raport HTML: Skrypt powinien zebrać te dane i stworzyć jeden zbiorczy bilet w Jirze (np. w projekcie administracyjnym), w którego opisie znajdzie się sformatowana tabela z wynikami.
# moja jira to Atlassian z zagniezdzonym JSON'em, nie mam pojecia jak to zrobic, zrobilem same summary

#5 Auto-Komentarz: Skrypt powinien dopisać komentarz do każdego "Zombiaka", oznaczając przypisaną do niego osobę (mention @username): "Cześć, czy to zadanie jest nadal aktualne? Brak aktywności od 30 dni."

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
    "Accept": "application/json",
    "Content-Type": "application/json"
}
def searchinJQLforKey(data):
    result = []
    for item in data['issues']:
        result.append(item['key'])
    print(result)
    return result

def responseFunction(method="", url=None, data=None, params=None, auth=None, headers=None):
    response = requests.request(
        method = method,
        url = url,
        data = data,
        params = params,
        auth = auth,
        headers = headers
    )
    return response

listOfQueries = {
    'zombies': {
        'jql': 'project = HAP AND type IN (Story, Task) AND status = "To Do" AND NOT updated >= -2h ORDER BY cf[10019] ASC'},
    'estimate': {
        'jql': 'project = HAP AND type IN (Story, Task, Bug) AND statuscategory = Complete AND (timeestimate = EMPTY OR timespent = EMPTY) ORDER BY cf[10019] ASC'},
    'orphan': {
        'jql': 'project = HAP AND type IN (Story, Task) AND parent = empty ORDER BY cf[10019] ASC'},
}

def getTasksFromJQL(d = domain, a = auth, query = None):
    url = f"{d}search/jql"
    if query == "zombies":
        nameQuery = query
        params = {
        'jql': listOfQueries['zombies']['jql'],
        'fields': 'summary'
        }
    elif query == "estimate":
        nameQuery = query
        params = {
        'jql': listOfQueries['estimate']['jql'],
        'fields': 'summary'
        }
    elif query == "orphan":
        nameQuery = query
        params = {
        'jql': listOfQueries['orphan']['jql'],
        'fields': 'summary'
        }
    else:
        print("Error! Wrong JQL querry or not existing!")
    
    response = responseFunction("GET",url,None,params,a,headers)
    data = response.json()
    if response.status_code == 200:
        print(f"Success! Data from {nameQuery} succeed.")
        return searchinJQLforKey(data)
    else:
        print(f"Error! Code: {response.status_code}")
        return []  

def postAutoZombieComment(d = domain, a = auth, h = headers, z = None):
    if not z:
        print("Error! Lista taskow zombie jest pusta!")
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
                                "text": "zombiaczek, ping3"
                            }
                        ]
                    }
                ]
            }
        })
        response = responseFunction("POST",url,payload,None,a,headers)
        if response.status_code == 201:
            print(f"Success! Task that are zombies: {z} are commented!")
        else:
            print(f"Error! Code: {response.status_code}")

def createSummaryJira(d = domain, a = auth, h = headers):
    u = f"{d}issue"
    try:
        payload = json.dumps({
        "fields": {
            "project": {
                "key": "HAP"
            },
            "summary": "Podsumowanie kazdego zadania (final version?)",
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": "Lista taskow ktore sa TODO i nie mialy aktualizacji od 1 dnia:"},
                            {"type": "hardBreak"},
                            {"type": "text", "text": f"{allZombies}"},
                            {"type": "hardBreak"},
                            {"type": "text", "text": "Lista taskow ktore nie maja przypisanego Epica:"},
                            {"type": "hardBreak"},
                            {"type": "text", "text": f"{allOrphan}"},
                            {"type": "hardBreak"},
                            {"type": "text", "text": "Lista taskow ktore sa zamkniete i nie maja zalogowanego czasu:"},
                            {"type": "hardBreak"},
                            {"type": "text", "text": f"{allEstimates}"}
                        ]
                    }
                ]
            },
            "issuetype": {
                "name": "Task"
            }
        }
        })
        response = responseFunction("POST",u,payload,None,a,headers)
        if response.status_code == 201:
            print(f"Success! Summary task created.")
        else:
            print(f"Error! Code: {response.status_code}")
    except NameError:
        print("Nie wszystkie listy zostaly zainicjalizowane!")

allZombies = getTasksFromJQL(query="zombies") 
allOrphan = getTasksFromJQL(query="orphan") 
allEstimates = getTasksFromJQL(query="estimate")
postAutoZombieComment(z = allZombies)
createSummaryJira()