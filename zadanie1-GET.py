# Zadanie 1: "Szybki podgląd" (GET)
# Cel: Pobierz szczegóły konkretnego zgłoszenia (np. BUG-101) i wyświetl jego status oraz osobę przypisaną.

import requests
from requests.auth import HTTPBasicAuth
import json

url = "https://nymon.atlassian.net/rest/api/3/issue/HAP-5"

auth = HTTPBasicAuth("natanek402@gmail.com", "ATATT3xFfGF0VCQLnTOu2qk2k38D6oFWpJD9cLya6QeIV9msPYShSpyzeBgDnyGQKsb3kTdgd52GCTQY9o1dcgPVmQk9Zlne0LsJegeJKMjmV7NXPAyckTzv_zv9KEsWsQV2bF9g3JsJTuE_6feIyTsVI4ZA71HY4twWh3OLjrcjxfUHDZxVhP0=93D16BCD") #cholernie glupie

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