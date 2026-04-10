import requests
from requests.auth import HTTPBasicAuth
import json

url = "https://nymon.atlassian.net/rest/api/2/issue"

# Upewnij się, że ten email i token są poprawne
auth = HTTPBasicAuth("natanek402@gmail.com", "ATATT3xFfGF0VCQLnTOu2qk2k38D6oFWpJD9cLya6QeIV9msPYShSpyzeBgDnyGQKsb3kTdgd52GCTQY9o1dcgPVmQk9Zlne0LsJegeJKMjmV7NXPAyckTzv_zv9KEsWsQV2bF9g3JsJTuE_6feIyTsVI4ZA71HY4twWh3OLjrcjxfUHDZxVhP0=93D16BCD") 

headers = {
  "Accept": "application/json",
  "Content-Type": "application/json"
}

# Minimalny zestaw pól potrzebny do stworzenia zadania
payload = json.dumps({
  "fields": {
    "project": {
      "key": "HAP"  # Używamy klucza tekstowego zamiast ID 10000
    },
    "summary": "Zadanie utworzone przez skrypt Python",
    "description": "Opis zadania testowego",
    "issuetype": {
      "name": "Task"  # Możesz też użyć "id": "10000", jeśli jesteś pewien, że to Task
    }
  }
})

response = requests.request(
   "POST",
   url,
   data=payload,
   headers=headers,
   auth=auth
)

if response.status_code == 201:
    print("Sukces!")
    print(response.text)
else:
    print(f"Błąd {response.status_code}")
    print(response.text)
