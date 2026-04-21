import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth
import json
import tenacity

load_dotenv()

url = "https://nymon.atlassian.net/rest/api/3/search/jql"

api_key = os.getenv("JIRA_API_KEY")
email = os.getenv("JIRA_EMAIL")

auth = HTTPBasicAuth(email, api_key)

headers = {
  "Accept": "application/json",
  "Content-Type": "application/json"
}

@tenacity.retry(wait=tenacity.wait_exponential(multiplier=1, min=4, max=10))
def simpleQuery():
    query = {
        'jql': 'issuetype = Bug',
        'maxResults': '50',
        'fields': 'summary',
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query,
        auth=auth
    )

    response.raise_for_status()

    data = response.json()
    print(json.dumps(data, indent=4))
simpleQuery()