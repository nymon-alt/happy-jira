# Zadanie 2: "Automatyczny raport" (SEARCH)
# Cel: Znajdź wszystkie zgłoszenia typu "Bug", które są otwarte (status 'To Do' lub 'In Progress') i wypisz ich klucze. Wykorzystaj do tego język JQL.

# This code sample uses the 'requests' library:
# http://docs.python-requests.org

import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth
import json

load_dotenv()

url = "https://nymon.atlassian.net/rest/api/3/search/jql"

api_key = os.getenv("JIRA_API_KEY")
email = os.getenv("JIRA_EMAIL")

auth = HTTPBasicAuth(email, api_key)

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