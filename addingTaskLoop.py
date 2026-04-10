# This code sample uses the 'requests' library:
# http://docs.python-requests.org

#tworzenie prostego zadania z summary, description

import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth
import json

load_dotenv()

api_key = os.getenv("JIRA_API_KEY")
email = os.getenv("JIRA_EMAIL")

auth = HTTPBasicAuth(email, api_key)

url = "https://nymon.atlassian.net/rest/api/3/issue"

headers = {
  "Accept": "application/json",
  "Content-Type": "application/json"
}

featureName = "CB00000-"
subFeatureName = ["A", "B", "C", "D", "E", "F"]

for n in subFeatureName:
    currentName = featureName + n
    payload = json.dumps({ # https://developer.atlassian.com/cloud/jira/platform/rest/v2/api-group-issues/#api-rest-api-2-issue-post
    "fields": {
        "project": {
            "key": "HAP" #klucz projektu z jiry
        },
        "summary": currentName,
        "description": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "text":
                            "Automated script for feature: " + currentName,
                            "type": "text"
                        }
                    ]
                }
            ]
        },
        "issuetype": {
            "name": "Task"  # moze byc bug, story itd
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

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))