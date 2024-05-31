import requests
import json
from settings import site


def request(id_for_summary):
	url = "https://hotels4.p.rapidapi.com/reviews/v3/get-summary"

	payload = {
		"currency": "USD",
		"eapid": 1,
		"locale": "en_US",
		"siteId": 300000001,
		"propertyId": id_for_summary
	}
	headers = {
		"content-type": "application/json",
		"X-RapidAPI-Key": site.api_key,
		"X-RapidAPI-Host": site.host_api
	}

	response = requests.post(url, json=payload, headers=headers)
	data = response.json()['data']["propertyReviewSummaries"][0]["propertyReviewCountDetails"]["fullDescription"]
	new_data = data + '\n'
	for i_elem in response.json()['data']["propertyReviewSummaries"][0]["reviewSummaryDetails"]:
		new_data += i_elem["label"] + ': ' + i_elem["formattedRatingOutOfMaxA11y"]["accessibilityLabel"] + '\n'
	return new_data
