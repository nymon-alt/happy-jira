#usuwanie wczesniej stworzonego zadania w jira

import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth
import json

load_dotenv()

api_key = os.getenv("JIRA_API_KEY")
email = os.getenv("JIRA_EMAIL")

auth = HTTPBasicAuth(email, api_key)

url = "https://nymon.atlassian.net/rest/api/3/issue/HAP-4" #wpisujesz ID zadania bezposrednio, nie calosc

headers = {
  "Accept": "application/json",
  "Content-Type": "application/json"
}

response = requests.request(
   "DELETE",
   url,
   auth=auth
)

print(response.text)