import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth
import json

load_dotenv()

api_key = os.getenv("JIRA_API_KEY")
email = os.getenv("JIRA_EMAIL")

auth = HTTPBasicAuth(email, api_key)

url = "https://nymon.atlassian.net/rest/api/3/search/jql" 

headers = {
  "Accept": "application/json",
  "Content-Type": "application/json"
}
maxResults = 2
allIssues = []
nextPageToken = None

while True:
    query = {
    'jql': 'project = HAP',
    'maxResults': maxResults,
    'fields': 'id',
    }

    if nextPageToken:
        query['nextPageToken'] = nextPageToken

    response = requests.request(
    "GET",
    url,
    headers=headers,
    params=query,
    auth=auth
    )

    data = response.json()
    issues = data.get('issues')
    allIssues.extend(issues)

    nextPageToken = data.get('nextPageToken')

    if data.get('isLast') == True or nextPageToken == None:
        break

print(f"pobrano lacznie: {len(allIssues)} rekordow")

# startAt = 0
# maxResults = 2
# allIssues = []
# while True:
#     query = {
#     'jql': 'project = HAP',
#     'maxResults': maxResults,
#     'startAt': startAt,
#     'fields': 'id',
#     }

#     response = requests.request(
#     "GET",
#     url,
#     headers=headers,
#     params=query,
#     auth=auth
#     )

#     data = response.json()
#     issues = data.get('issues')

#     allIssues.extend(issues)

#     if len(issues) < maxResults:
#         break

#     startAt = startAt + maxResults
