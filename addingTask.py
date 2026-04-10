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

payload = json.dumps({ # https://developer.atlassian.com/cloud/jira/platform/rest/v2/api-group-issues/#api-rest-api-2-issue-post
    "fields": {
        "project": {
            "key": "HAP" #klucz projektu z jiry
        },
        "summary": "pierwsze zadanie",
        "description": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "text":
"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam hendrerit vestibulum tellus, in tincidunt erat lacinia ut. Cras a est elit. Nulla laoreet suscipit leo eu aliquam. Pellentesque porta metus nisl, vel efficitur nisi gravida at. Etiam et mauris molestie, cursus enim at, consequat tellus. Fusce et maximus ante. Sed congue in turpis vel feugiat. Sed vitae efficitur leo. Vestibulum gravida finibus nisi nec mattis. Nulla facilisi. Donec sit amet ante et eros posuere egestas nec nec nunc. Phasellus dignissim vestibulum eleifend. Praesent vel tincidunt lacus. Maecenas venenatis eros vel sapien lacinia, at auctor ligula ultrices. Nam sit amet tempus tellus.",
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