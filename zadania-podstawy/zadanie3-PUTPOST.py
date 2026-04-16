# Zadanie 3: "Masowa edycja" (PUT/POST)
# Cel: Napisz skrypt, który do konkretnego zadania doda komentarz i jednocześnie zmieni jego priorytet na "Highest" oraz zmieni status na In progres

# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth
import json

load_dotenv()

url_transition = "https://nymon.atlassian.net/rest/api/3/issue/HAP-8/transitions"
url_priority = "https://nymon.atlassian.net/rest/api/3/priority"
url_priority_set = "https://nymon.atlassian.net/rest/api/3/issue/HAP-8"
url_comment = "https://nymon.atlassian.net/rest/api/3/issue/HAP-8/comment"

api_key = os.getenv("JIRA_API_KEY")
email = os.getenv("JIRA_EMAIL")
auth = HTTPBasicAuth(email, api_key)
headers = {
  "Accept": "application/json",
  "Content-Type": "application/json"
}

def gettingTransition(url_transition=url_transition, auth=auth, headers=headers):
    response = requests.request(
    "GET",
    url_transition,
    headers=headers,
    auth=auth
    )
    data = response.json()
    
    for item in data['transitions']:
        print(f"{item['name']} ma id {item['id']}")

def settingTransition(url_transition=url_transition, auth=auth, headers=headers):
    payload = json.dumps({
    "transition": {
    "id": "21" }
    })
    
    response = requests.request(
    "POST",
    url_transition,
    data=payload,
    headers=headers,
    auth=auth)

    if response.status_code == 204:
        print("set transition: ok")
    else:
        print(f"set transition: nok {response.status_code}")
        print(response.text)

def gettingPriority(url_priority=url_priority, auth=auth, headers=headers):
    response = requests.request(
    "GET",
    url_priority,
    headers=headers,
    auth=auth
    )
    data = response.json()
    for item in data:
        print(f"{item['name']} ma id: {item['id']}")

def settingPriority(url_priority_set=url_priority_set, auth=auth, headers=headers):
    payload = json.dumps( {
    "fields": {
    "priority": {
      "id": "1"}
    }
    } )
    response = requests.request(
    "PUT",
    url_priority_set,
    data=payload,
    headers=headers,
    auth=auth
    )
    if response.status_code == 204:
        print("set priority: ok")
    else:
        print(f"set priority: nok: {response.status_code}")
        print(response.text)
    
def addingComment(url_comment=url_comment, auth=auth, headers=headers):
    payload = json.dumps( {
    "body": {
    "content": [
      {
        "content": [
          {
            "text": "potrojny skrypcior.",
            "type": "text"
          }
        ],
        "type": "paragraph"
      }
    ],
    "type": "doc",
    "version": 1
    }
    } )

    response = requests.request(
    "POST",
    url_comment,
    data=payload,
    headers=headers,
    auth=auth
    )
    if response.status_code == 201:
        print("komentarz dodany")
    else:
        print("cos nie pyklo:" + response.json())

#gettingTransition()
settingTransition()
#gettingPriority()
settingPriority()
addingComment()