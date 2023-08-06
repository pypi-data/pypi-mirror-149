import geoip2.database
import json

def get_geo_ip(ip):
	result = {}

	with geoip2.database.Reader('./GeoLite2-City.mmdb') as reader:
		response = reader.city(ip)
		result['ip'] = response.traits.ip_address
		result['country'] = response.country.name
		result['continent'] = response.continent.names['en']
		result['iso'] = response.country.iso_code
		result['city'] = response.city.name
		result['zip'] = response.postal.code
		result['timezone'] = response.location.time_zone
		result['latitude'] = response.location.latitude
		result['longitude'] = response.location.longitude

		
	with geoip2.database.Reader('./GeoLite2-ASN.mmdb') as reader:
		response = reader.asn(ip)
		result['org'] = response.autonomous_system_organization

	return result

def get_geo_ip_json(ip):

	result = {}

	with geoip2.database.Reader('./GeoLite2-City.mmdb') as reader:
		response = reader.city(ip)
		result['ip'] = response.traits.ip_address
		result['country'] = response.country.name
		result['continent'] = response.continent.names['en']
		result['iso'] = response.country.iso_code
		result['city'] = response.city.name
		result['zip'] = response.postal.code
		result['timezone'] = response.location.time_zone
		result['latitude'] = response.location.latitude
		result['longitude'] = response.location.longitude

		
	with geoip2.database.Reader('./GeoLite2-ASN.mmdb') as reader:
		response = reader.asn(ip)
		result['org'] = response.autonomous_system_organization

	jsonString = json.dumps(result, indent=4)

	return(jsonString)

print(get_geo_ip('204.236.186.159')['country'])

