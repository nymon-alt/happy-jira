import requests
import json
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

url = "https://nymon.atlassian.net/rest/api/2/search"

headers = {'Accept' : 'application/json'}

load_dotenv()
email = os.getenv('JIRA_EMAIL')
api_key = os.getenv('JIRA_API_KEY')

auth = HTTPBasicAuth(email, api_key)

query = {
    "jql": "project = HAP",
    "startAt": 0,
    "maxResults": 1,
    "fields": [
        "summary",
        "status",
        "assignee"
    ]
}

response = requests.request(
    "POST",
    url = url,
    headers = headers,
    auth = auth,
    json=query
)

data = json.dumps(response.json(), indent=4)
print(data)