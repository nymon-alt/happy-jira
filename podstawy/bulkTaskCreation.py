import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth
import json

load_dotenv()

api_key = os.getenv("JIRA_API_KEY")
email = os.getenv("JIRA_EMAIL")

auth = HTTPBasicAuth(email, api_key)

url = "https://nymon.atlassian.net/rest/api/3/issue/bulk?dryRun=true" #nie dziala, czemu?

headers = {
  "Accept": "application/json",
  "Content-Type": "application/json"
}

payload = json.dumps( {
  "issueUpdates": [
    {
      "fields": {
        "description": {
          "version": 1,
          "type": "doc",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {
                  "type": "text",
                  "text": "First issue of bulk issues."
                }
              ]
            }
          ]
        },
        "issuetype": {
          "name": "Task"
        },
        "labels": [
          "bulk_issue"
        ],
        "project": {
          "id": "10001"
        },
        "summary": "Don't overkill API payloads",
        "timetracking": {
          "originalEstimate": "10",
          "remainingEstimate": "5"
        }
      },
      "update": {
        "worklog": [
          {
            "add": {
              "started": "2026-04-14T11:05:00.000+0000",
              "timeSpent": "60m"
            }
          }
        ]
      }
    },
    {
      "fields": {
        "description": {
          "version": 1,
          "type": "doc",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {
                  "type": "text",
                  "text": "First issue of bulk issues."
                }
              ]
            }
          ]
        },
        "issuetype": {
          "name": "Task"
        },
        "labels": [
          "bulk_issue"
        ],
        "project": {
          "id": "10001"
        },
        "summary": "Don't overkill API payloads",
        "timetracking": {
          "originalEstimate": "10",
          "remainingEstimate": "5"
        }
      },
      "update": {
        "worklog": [
          {
            "add": {
              "started": "2026-04-14T11:05:00.000+0000",
              "timeSpent": "60m"
            }
          }
        ]
      }
    },
    {
      "fields": {
        "description": {
          "version": 1,
          "type": "doc",
          "content": [
            {
              "type": "paragraph",
              "content": [
                {
                  "type": "text",
                  "text": "First issue of bulk issues."
                }
              ]
            }
          ]
        },
        "issuetype": {
          "name": "Task"
        },
        "labels": [
          "bulk_issue"
        ],
        "project": {
          "id": "10001"
        },
        "summary": "Don't overkill API payloads",
        "timetracking": {
          "originalEstimate": "10",
          "remainingEstimate": "5"
        }
      },
      "update": {
        "worklog": [
          {
            "add": {
              "started": "2026-04-14T11:05:00.000+0000",
              "timeSpent": "60m"
            }
          }
        ]
      }
    }
  ]
})

response = requests.request(
   "POST",
   url,
   data=payload,
   headers=headers,
   auth=auth
)

data = response.json()
if response.status_code == 201:
    print("Success! Issues created!")
else:
    print(f"something funky: {response.status_code}", json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))