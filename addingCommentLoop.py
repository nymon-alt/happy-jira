#dodawanie komentarza do wczesniej utworzonego zadania

import requests
from requests.auth import HTTPBasicAuth
import json

url = "https://nymon.atlassian.net/rest/api/3/issue/HAP-2/comment" #wpisujesz ID zadania bezposrednio, nie calosc

auth = HTTPBasicAuth("natanek402@gmail.com", "ATATT3xFfGF0VCQLnTOu2qk2k38D6oFWpJD9cLya6QeIV9msPYShSpyzeBgDnyGQKsb3kTdgd52GCTQY9o1dcgPVmQk9Zlne0LsJegeJKMjmV7NXPAyckTzv_zv9KEsWsQV2bF9g3JsJTuE_6feIyTsVI4ZA71HY4twWh3OLjrcjxfUHDZxVhP0=93D16BCD") #cholernie glupie

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