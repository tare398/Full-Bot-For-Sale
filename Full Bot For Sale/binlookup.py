import requests

def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def format_key(key):
    return ' '.join(word.capitalize() for word in key.split('_'))

def get_bin_info(bin_number):
    url = f"https://bins.antipublic.cc/bins/{bin_number}"
    response = requests.get(url)

    try:
        if response.status_code == 200:
	        data = response.json()
	        if data:
	            flat_data = flatten_dict(data, sep=' ')
	            info_lines = [f"{format_key(key)}: {value}" for key, value in flat_data.items()]
	            return "\n".join(info_lines)
	        else:
	            return "No data available for the given BIN."
        else:
	        return "Invalid BIN or no data exists"
    except requests.exceptions.JSONDecodeError: 
        return "Invalid BIN or no data exists"
        