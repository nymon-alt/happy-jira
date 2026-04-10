# Zadanie 2: "Automatyczny raport" (SEARCH)
# Cel: Znajdź wszystkie zgłoszenia typu "Bug", które są otwarte (status 'To Do' lub 'In Progress') i wypisz ich klucze. Wykorzystaj do tego język JQL.

# This code sample uses the 'requests' library:
# http://docs.python-requests.org

import requests
from requests.auth import HTTPBasicAuth
import json

url = "https://nymon.atlassian.net/rest/api/3/search/jql"

auth = HTTPBasicAuth("natanek402@gmail.com", "ATATT3xFfGF0VCQLnTOu2qk2k38D6oFWpJD9cLya6QeIV9msPYShSpyzeBgDnyGQKsb3kTdgd52GCTQY9o1dcgPVmQk9Zlne0LsJegeJKMjmV7NXPAyckTzv_zv9KEsWsQV2bF9g3JsJTuE_6feIyTsVI4ZA71HY4twWh3OLjrcjxfUHDZxVhP0=93D16BCD") #cholernie glupie

headers = {
  "Accept": "application/json",
  "Content-Type": "application/json"
}

query = {
  'jql': 'issuetype = Bug AND (status = "In Progress" OR status = "To Do")',
  'maxResults': '50',
  'fields': 'summary',
}

response = requests.request(
   "GET",
   url,
   headers=headers,
   params=query,
   auth=auth
)

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))