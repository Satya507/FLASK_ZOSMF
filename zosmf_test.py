import requests
from zoautil_py import datasets
HEADERS = {
    "X-CSRF-ZOSMF-HEADER": "",
    "Authorization": "Basic <Base64 encoding of ID and password, joined by a single colon (:)>"
          }

response=requests.get("https://204.90.115.200:10443/zosmf/LogOnPanel.jsp", HEADERS,
                   auth=("Z30658", "qazwsx32"), verify=False)
print(response)
if response.status_code==200:
   print('mert')
else:
   print('dert')
