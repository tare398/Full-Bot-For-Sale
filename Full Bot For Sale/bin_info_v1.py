import requests

def bin_info(bin_number):
    url = f"https://bins.antipublic.cc/bins/{bin_number}"
    response = requests.get(url)

    try:
        if response.status_code == 200:
	        data = response.json()
	        if data:
	            return f"Country: {data['country_name']} {data['country_flag']}\nBrand: {data['brand']}\nBank: {data['bank']}\nLevel - Type: {data['level']} - {data['type']}"
	        else:
	            return "No data available for the given BIN."
        else:
	        return "Invalid BIN or no data exists"
    except requests.exceptions.JSONDecodeError: 
        return "Invalid BIN or no data exists"