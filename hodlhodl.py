#!/usr/bin/env python3

# 2022 @j4imefoo

import json

class HodlHodl:

	def getOffers(curr, direction, refprice, session):

		curr = curr.upper()
		api = f"https://hodlhodl.com/api/v1/offers?filters[side]={direction}&filters[include_global]=true&filters[currency_code]={curr}&filters[only_working_now]=true&sort[by]=price"

		f = session.get(api)
		jsonweb = f.json() 
		f.close() 
		alloffers = jsonweb['offers']

		lista = []

		for offer in alloffers:
			offers = {}
			offers['exchange'] = "HodlHodl"
			offers['price'] = int(float(offer['price']))
			offers['dif']=(offers['price']/refprice - 1)*100
			offers['currency'] = offer['currency_code']
			offers['min_amount'] = int(float(offer['min_amount']))
			offers['max_amount'] = int(float(offer['max_amount']))
			offers['min_btc']=offers['min_amount']/offers['price']
			offers['max_btc']=offers['max_amount']/offers['price']
			status = offer['trader']['online_status']
			if (direction == "buy"):
				offers['method'] = offer['payment_methods'][0]['name']
			else:
				offers['method'] = offer['payment_method_instructions'][0]['payment_method_name']
			if "SEPA" in offers['method']:
				offers['method'] = "SEPA"
			elif "Any national bank" in offers['method']:
				offers['method'] = "NATIONAL_BANK"
			if (status=='online'):
				lista.append(offers)

		lista.sort(key=lambda item: item.get("price"))
		return lista
