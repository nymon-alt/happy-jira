#usuwanie wczesniej stworzonego zadania w jira

import requests
from requests.auth import HTTPBasicAuth

url = "https://nymon.atlassian.net/rest/api/3/issue/HAP-4" #wpisujesz ID zadania bezposrednio, nie calosc

auth = HTTPBasicAuth("natanek402@gmail.com", "ATATT3xFfGF0VCQLnTOu2qk2k38D6oFWpJD9cLya6QeIV9msPYShSpyzeBgDnyGQKsb3kTdgd52GCTQY9o1dcgPVmQk9Zlne0LsJegeJKMjmV7NXPAyckTzv_zv9KEsWsQV2bF9g3JsJTuE_6feIyTsVI4ZA71HY4twWh3OLjrcjxfUHDZxVhP0=93D16BCD") #cholernie glupie

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