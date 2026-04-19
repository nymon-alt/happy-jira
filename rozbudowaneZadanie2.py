
# 1. Skrypt powinien połączyć się z Jirą i wyszukać (za pomocą JQL) zgłoszenia, które:

# Mają status "In Progress", ale nie były aktualizowane od ponad 5 dni.

# Mają status "To Do" i priorytet "Highest", ale leżą nietknięte od 14 dni.

# Są przypisane do osób, które mają obecnie więcej niż 2 otwartych zadań (wykrywanie "wąskiego gardła").

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

# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json
import os
import dotenv

dotenv.load_dotenv()

url = "https://nymon.atlassian.net/rest/api/3/search/jql"

key = os.getenv('JIRA_API_KEY')
email = os.getenv('JIRA_EMAIL')

auth = HTTPBasicAuth(email, key)

headers = {
  "Accept": "application/json"
}

allResults = []

queries = [
    'project = HAP AND status=10004 AND updated<=-5d',
    'project = HAP AND status=10003 AND updated<=-1d AND priority=High',
    'project = HAP AND assignee=712020:0054c47f-96b1-4a85-8d59-f928c4235d41 AND status!=Zrobione'
]

for item in queries:
    query = {
        'jql':item,
        'maxResults': 50,
        'fields': 'id',
    }
    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query,
        auth=auth
    )
    data = response.json()
    print(data['issues'])