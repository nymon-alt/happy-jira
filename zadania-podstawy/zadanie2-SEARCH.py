# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json

url_search = "https://your-domain.atlassian.net/rest/api/3/search/jql"

auth = HTTPBasicAuth("email@example.com", "<api_token>")

headers = {
  "Accept": "application/json"
}

startAt = 0
maxResults = 50
allKeys = []

while True:

  query = {
    'jql': 'project = SRV AND status!=Done AND updated>=-30d',
    'maxResults': maxResults,
    'fields': 'summary',
    'startAt': startAt
  }

  response = requests.request(
    "GET",
    url_search,
    headers=headers,
    params=query,
    auth=auth
  )

  data = response.json()
  issues = data.get('issues')

  if len(issues) < maxResults:
    break

  for item in issues:
    allKeys.append(item.get('key'))

  startAt = startAt + maxResults


