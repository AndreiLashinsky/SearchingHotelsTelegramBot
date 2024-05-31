import requests
import json
from settings import site, search


def request(req):
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"

    querystring = {"q": req, "locale": "en_US", "langid": "1033", "siteid": "300000001"}

    headers = {
            "X-RapidAPI-Key": site.api_key,
            "X-RapidAPI-Host": site.host_api
        }
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()['sr']
    return data


# a = request('new york')
# print(a)
# response = request(search.request)
# for i_elem in response:
#     print(i_elem['type'])
# print(response)
# with open('search_v3.json', 'w') as file:
#     json.dump(response.json(), file, indent=4)
#
# print(response.json())
