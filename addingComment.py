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

url = "https://nymon.atlassian.net/rest/api/3/issue/HAP-3/comment" #wpisujesz ID zadania bezposrednio, nie calosc

headers = {
  "Accept": "application/json",
  "Content-Type": "application/json"
}

payload = json.dumps( {
    "body": {
    "type": "doc",
    "version": 1,
    "content": [
      {
        "type": "paragraph",
        "content": [
          {
            "text": "jestem bogiem tej gierki",
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