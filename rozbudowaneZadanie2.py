
# 1. Skrypt powinien połączyć się z Jirą i wyszukać (za pomocą JQL) zgłoszenia, które:
# firstQuery: Mają status "In Progress", ale nie były aktualizowane od ponad 2 dni.
# secondQuery: Mają status "To Do" i priorytet "Highest", ale leżą nietknięte od 4 dni.
# thirdQuery: Są przypisane do osób, które mają obecnie więcej niż 2 otwartych zadań (wykrywanie "wąskiego gardła"). #TODO

# 2. Dla znalezionych zgłoszeń skrypt musi podjąć akcje:
# Dodanie komentarza: Skrypt powinien automatycznie wspomnieć (@mention) osobę przypisaną, pytając o status (np. "Cześć, system wykrył brak aktywności. Czy potrzebujesz pomocy?").
# Aktualizacja pól: Jeśli zadanie o wysokim priorytecie leży zbyt długo, zmień mu etykietę na stale-alert.
# Przejście statusu: Jeśli zadanie jest w "In Progress", ale nie ma przypisanej osoby, przesuń je z powrotem do "To Do".

# 3. Etap: Generowanie Raportu PDF/HTML
# Po zakończeniu operacji, skrypt nie tylko wypisuje logi w konsoli, ale generuje plik (np. report_2026-04-16.html), który zawiera:
# Tabelę z listą zmodyfikowanych zadań.
# Statystyki: ile zadań "uratowano", kto jest najbardziej obciążony w zespole.

# Wymagania Techniczne
# Aby zadanie było naprawdę "rozbudowane", zastosuj poniższe standardy:
# Biblioteka: Użyj oficjalnego wrappera jira-python lub biblioteki requests (jeśli chcesz nauczyć się czystego REST API).
# Bezpieczeństwo: Nigdy nie wpisuj hasła/tokenu w kodzie. Użyj pliku .env i biblioteki python-dotenv.
# Programowanie obiektowe (OOP): Stwórz klasę JiraManager, która będzie miała metody takie jak .get_stale_issues(), .post_comment(), czy .generate_report().
# Obsługa błędów: Dodaj bloki try-except, aby skrypt nie wywalił się przy błędzie sieciowym lub braku uprawnień do konkretnego zgłoszenia.
# ///////////////////////////////////////////////////////////////////////////////////////////// #

#statusId: 10003 - do zrobienia, 10004 - w toku, 10005 - done
#priorityId: 4 - low, 3 - medium, 2 - high, 1 - highest


import requests
from requests.auth import HTTPBasicAuth
import json
import os
from dotenv import load_dotenv

url = "https://nymon.atlassian.net/rest/api/3/search/jql"

load_dotenv()
email = os.getenv('JIRA_EMAIL')
api_key = os.getenv('JIRA_API_KEY')
auth = HTTPBasicAuth(email, api_key)

headers = {
  "Accept": "application/json",
  "Content-Type": "application/json"
}

def getFromServerUsingJQL(u = url, a = auth, h = headers): #funkcja zwracajaca key z zapytan JQL w formie [[HAP-cos, HAP-cos],[HAP-cos]]
    #lista zapytan JQL
    listOfQueries = [
    'project = HAP AND status=10004 AND updated<=-2d',
    'project = HAP AND priority=1 AND updated<=-4d'
    ]
    allKeys = [] #lista do przechowywania wszystkich kluczy
    for item in listOfQueries:
        query = {
            'jql': item,
            'maxResults': 10,
            'fields': '*all',
        }
        while True: #obsluga paginacji w przypadku wielu rekordow
            singleQueryKey = []
            response = requests.request(
                "GET",
                url,
                headers=headers,
                params=query,
                auth=auth
            )
            if response.status_code == 200:
                print(f"REQUEST: {item} IS SUCCESSFUL!")
            else:
                print("something fucky with request!", json.dumps(data,indent=4))
            data = response.json()

            nextPageToken = data.get('nextPageToken')
            isLast = data.get('isLast')

            if nextPageToken:
                query = {'nextPageToken': nextPageToken}

            issues = data.get('issues')
            for item in issues:
                singleQueryKey.append((item.get('key')))

            if isLast:
                break
        allKeys.append(singleQueryKey)
    print(f"list of all keys from requests: {allKeys}")
    return allKeys
        
getFromServerUsingJQL()