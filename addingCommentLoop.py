#dodawanie komentarza do wczesniej utworzonego zadania

import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth
import json

load_dotenv()

api_key = os.getenv("JIRA_API_KEY")
email = os.getenv("JIRA_EMAIL")

auth = HTTPBasicAuth(email, api_key)

url = "https://nymon.atlassian.net/rest/api/3/issue/HAP-2/comment" #wpisujesz ID zadania bezposrednio, nie calosc

headers = {
  "Accept": "application/json",
  "Content-Type": "application/json"
}

comments = ["it's bad", "it's good", "it's 50-50"]
for char in comments:
    payload = json.dumps( {
    "body": {
    "type": "doc",
    "version": 1,
    "content": [
      {
        "type": "paragraph",
        "content": [
          {
            "text": char,
            "type": "text"
          }
        ]
      }
    ]
  }
} )

    response = requests.request(
    "POST",
    url,
    data=payload,
    headers=headers,
    auth=auth
    )

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))