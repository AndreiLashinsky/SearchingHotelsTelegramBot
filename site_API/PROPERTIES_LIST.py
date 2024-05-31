import requests
import json
from settings import site


def request(regionId, checkInDay, checkInMonth, checkInYear, checkOutDay, checkOutMonth, checkOutYear, adults, children,
																min_price, max_price):
	url = "https://hotels4.p.rapidapi.com/properties/v2/list"

	payload = {
		"currency": "USD",
		"eapid": 1,
		"locale": "en_US",
		"siteId": 300000001,
		"destination": {"regionId": regionId},
		"checkInDate": {
			"day": checkInDay,
			"month": checkInMonth,
			"year": checkInYear
		},
		"checkOutDate": {
			"day": checkOutDay,
			"month": checkOutMonth,
			"year": checkOutYear
		},
		"rooms": [
			{
				"adults": adults,
				"children": children
			}
		],
		"resultsStartingIndex": 0,
		"resultsSize": 200,
		"sort": "PRICE_LOW_TO_HIGH",
		"filters": {"price": {
				"max": max_price,
				"min": min_price
			}
		}
	}
	headers = {
		"content-type": "application/json",
		"X-RapidAPI-Key": site.api_key,
		"X-RapidAPI-Host": site.host_api
	}

	response = requests.post(url, json=payload, headers=headers)
	data = response.json()["data"]["propertySearch"]["properties"]
	properties = []
	for i_item in data:
		properties.append({
			"id": i_item['id'],
			'name': i_item['name'],
			"propertyImage": i_item["propertyImage"]["image"]["url"]
		})
	return properties
#
# print(response.json())
#
# with open('properties_list.json', 'w')as file:
# 	json.dump(response.json(), file, indent=4)


# with open('properties_list.json', 'r') as file:
# 	data = json.load(file)
# properties = []
# for i_item in data["data"]["propertySearch"]["properties"]:
# 	properties.append({"id": i_item['id'], 'name': i_item['name']})
# print(properties)
