#   /admin - admin control
#   /search - google scrap for gates
#   /bin - BIN lookup
#   /cb - check file bins
#   /len - how many file lines
#   /mix - shuffle and mix combo lines
#   /filter - extract cards with specific bin
#   /gef - genrate combo file
#   /gen - genrate 10 cards
#   /scr - scrap cards
#   /sk - check sk key
#   /chk - check single card with braintree
#   /str - check single card with stripe
#   /pay - check single card with paypal
#   /filestr - check combo file with stripe
#   /file - check combo file with braintree
#   /filep - check combo file with paypal
#   /start - start the bot
#———–———–———–———–———–———#
#pylint:disable=W0603
#pylint:disable=W0703
#pylint:disable=W0622
#———–———–———–———–———–———#
import telebot, time, os, asyncio, datetime, re, io, csv
from telebot import types
#———–———–———–———–———–———#
from braintree_Api import main as api
from bin_info_v1 import bin_info
from paypal import process_card_p
from stripe import process_card
from braintree import process_card_b
from genfun import gen_card
from search import perform_search
from len_fun import count_lines
from mix_fun import mix_lines
from filter_fun import filter
from sk_check import check_key
from binlookup import get_bin_info
from check_bins_fun import extract_bins
from scrap_fun import get_last_messages,save_to_file
#———–———–———–———–———–———#
bot_token = "توكن بوتك"
admin_id = 5894339732 #ايديك

bot = telebot.TeleBot(f"{bot_token}", parse_mode='html')

bot.send_message(admin_id,"Started")
iD = [f"{admin_id}"]
bot_working = True
is_card_checking = False
#—————–————–———————––———#
def is_user_allowed(user_id):
	allowed_user_ids = [str(id) for id in iD]
	return str(user_id) in allowed_user_ids
#—————–————–———————––———#
if not os.path.exists("Temps"):
	os.makedirs("Temps")
#—————–————–———————––———#
def create_main_menu_keyboard():
	markup = types.InlineKeyboardMarkup()
	
	markup.add(types.InlineKeyboardButton("Admin", callback_data="admin"),types.InlineKeyboardButton("Other", callback_data="other"))
	
	markup.add(types.InlineKeyboardButton("CC Check", callback_data="cc"))

	markup.add(types.InlineKeyboardButton("Scarp", callback_data="scr"))
	
	markup.add(types.InlineKeyboardButton("Combo Helper", callback_data="combo"))
	return markup

def create_back_button_keyboard():
	markup = types.InlineKeyboardMarkup()
	markup.add(types.InlineKeyboardButton("Back", callback_data="back"))
	return markup
#—————–————–———————––———#
@bot.message_handler(commands=['start'])
def send_main_menu(message):
	bot.send_video(message.chat.id, video="https://telegra.ph/file/368c5c5b4b76cfeb4d74b.mp4",
				   caption="""
Welcome to the bot please choose from the options below.
""", reply_markup=create_main_menu_keyboard())

@bot.callback_query_handler(func=lambda call: call.data == "admin")
def admin_callback(call):
	chat_id = call.message.chat.id
	message_id = call.message.message_id
	if chat_id == admin_id:
		bot.edit_message_caption("""
#———–———–——————–——#
#   /admin - admin control
#———–———–——————–——#
		""",chat_id, message_id, reply_markup=create_back_button_keyboard())
	else:
		bot.answer_callback_query(call.id, text="You cannot access the Admins commands because you are not an Admin.", show_alert=True)

@bot.callback_query_handler(func=lambda call: call.data == "cc")
def cards_callback(call):
	chat_id = call.message.chat.id
	message_id = call.message.message_id
	bot.edit_message_caption("""
#———–———–——————–——#
/chk - check single card with braintree
/str - check single card with stripe
/pay - check single card with paypal
/file - check combo file with braintree
/filestr - check combo file with stripe
/filep - check combo file with paypal
#———–———–——————–——#
	""", chat_id, message_id, reply_markup=create_back_button_keyboard())

@bot.callback_query_handler(func=lambda call: call.data == "scr")
def scarp_callback(call):
	chat_id = call.message.chat.id
	message_id = call.message.message_id
	bot.edit_message_caption("""
#———–———–——————–——#
#   /scr - scrap cards
#———–———–——————–——#
	""", chat_id, message_id, reply_markup=create_back_button_keyboard())

@bot.callback_query_handler(func=lambda call: call.data == "combo")
def combo_callback(call):
	chat_id = call.message.chat.id
	message_id = call.message.message_id
	bot.edit_message_caption("""
#———–———–——————–——#
#   /cb - check file bins
#   /len - how many file lines
#   /mix - shuffle combo lines
#   /filter - extract cards with specific bin
#   /gef - genrate combo file
#   /gen - genrate 10 cards
#———–———–——————–——#
	""", chat_id, message_id, reply_markup=create_back_button_keyboard())

@bot.callback_query_handler(func=lambda call: call.data == "other")
def other_callback(call):
	chat_id = call.message.chat.id
	message_id = call.message.message_id
	bot.edit_message_caption("""
#———–———–——————–——#
#   /search - google scrap for gates
#   /sk - check sk key
#   /bin - BIN lookup
#———–———–——————–——#
	""", chat_id, message_id, reply_markup=create_back_button_keyboard())

@bot.callback_query_handler(func=lambda call: call.data == "back")
def back_callback(call):
	chat_id = call.message.chat.id
	message_id = call.message.message_id
	bot.edit_message_caption("Welcome to the bot please choose from the options below.", chat_id, message_id, reply_markup=create_main_menu_keyboard())
#—————–————–———————––———#
@bot.message_handler(commands=['admin'])#1
def admin_command(message):
	if message.from_user.id == admin_id:
		keyboard = telebot.types.InlineKeyboardMarkup()
		if bot_working:
			status_text = "The bot is working ✅"
			button_text = "Set bot as not working ❌"
		else:
			status_text = "The bot is not working ❌"
			button_text = "Set bot as working ✅"
		
		keyboard.add(telebot.types.InlineKeyboardButton(text=button_text, callback_data='toggle_status'))
		bot.send_message(message.chat.id, status_text, reply_markup=keyboard)
	else:
		pass

@bot.callback_query_handler(func=lambda call: call.data == 'toggle_status')
def toggle_status_callback(call):
	global bot_working
	bot_working = not bot_working
	if bot_working:
		new_status = "The bot is working ✅"
		new_button_text = "Set bot as not working ❌"
	else:
		new_status = "The bot is not working ❌"
		new_button_text = "Set bot as working ✅"
	
	keyboard = telebot.types.InlineKeyboardMarkup()
	keyboard.add(telebot.types.InlineKeyboardButton(text=new_button_text, callback_data='toggle_status'))
	bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=new_status, reply_markup=keyboard)
#—————–————–———————––———#
@bot.message_handler(commands=['search']) #2
def search_command(message):
	if bot_working:
		chat_id = message.chat.id
		initial_message = bot.reply_to(message, "Search Started...⏳")
		args = message.text.split()[1:]
		if len(args) != 3:
			bot.edit_message_text(chat_id=chat_id, message_id=initial_message.message_id, text="Please provide three arguments in the format: \n/search [payment] [name] [domain]")
			return
		
		v1, v2, v3 = args
		result = perform_search(v1, v2, v3)
		bot.edit_message_text(chat_id=chat_id, message_id=initial_message.message_id, text=result,disable_web_page_preview=True)
	else:
		pass
#—————–————–———————––———#
@bot.message_handler(commands=['bin'])#3
def bin_lookup_command(message):
	if bot_working:
		chat_id = message.chat.id
		try:
			initial_message = bot.reply_to(message, "Lookup Started...⏳")
			biN = message.text.split()[1]
			bin_inf = bin_info(biN)
			bot.edit_message_text(chat_id=chat_id, message_id=initial_message.message_id, text=bin_inf)
		except Exception as ex:
			bot.edit_message_text(chat_id=chat_id, message_id=initial_message.message_id, text=f"An error occurred: {str(ex)}")
	else:
		pass
#—————–————–———————––———#
@bot.message_handler(commands=['cb'])#4
def handle_bins_command(message):
    if bot_working:
        try:
            bins_count = extract_bins(message, bot)
            if bins_count is not None:
                sorted_bins = sorted(bins_count.items(), key=lambda item: item[1], reverse=True)
                with io.StringIO() as file_buffer:
                    writer = csv.writer(file_buffer)
                    writer.writerow(["Bin", "Count"])
                    for bin, count in sorted_bins:
                        writer.writerow([bin, count])
                    file_buffer.seek(0)
                    bot.send_document(message.chat.id, file_buffer,'bins.csv')
                bot.reply_to(message, "The bins have been sent as a file with the highest count bins at the top.")
            else:
                bot.reply_to(message, "Please reply to a combo file to get the bins it contains.")
        except Exception as e:
            bot.reply_to(message, str(e))
    else:
        pass

#—————–————–———————––———#
@bot.message_handler(commands=['len'])#5
def handle_len_command(message):
	if bot_working:
		chat_id = message.chat.id
		initial_message = bot.reply_to(message, "Count Started...⏳")
		response = count_lines(message,bot)
		bot.edit_message_text(chat_id=chat_id, message_id=initial_message.message_id, text=response)
	else:
		pass
#—————–————–———————––———#
@bot.message_handler(commands=['mix'])#6
def handle_mix_command(message):
	if bot_working:
		chat_id = message.chat.id
		try:
			if message.reply_to_message and message.reply_to_message.document:
				initial_message = bot.reply_to(message, "Mix Started...⏳")
				file_info = bot.get_file(message.reply_to_message.document.file_id)
				downloaded_file = bot.download_file(file_info.file_path)
				shuffled_content = mix_lines(downloaded_file)
				temp_file_path = os.path.join("Temps", 'shuffled_lines.txt')
				with open(temp_file_path, 'w') as shuffled_file:
					shuffled_file.write(shuffled_content)
				with open(temp_file_path, 'rb') as shuffled_file:
					bot.delete_message(message_id=initial_message.message_id,chat_id=chat_id)
					bot.send_document(message.chat.id, shuffled_file)
				os.remove(temp_file_path)
			else:
				bot.edit_message_text(chat_id=chat_id, message_id=initial_message.message_id, text="Please reply to a document to use this command.")
		except Exception as e:
			bot.edit_message_text(chat_id=chat_id, message_id=initial_message.message_id, text=f"An error occurred: {str(e)}")
	else:
		pass
#—————–————–———————––———#
@bot.message_handler(commands=['filter'])#7
def handle_filter(message):
	if bot_working:
		command_parts = message.text.split()
		chat_id = message.chat.id
		initial_message = bot.reply_to(message, "Filter Started...⏳")
		if len(command_parts) != 2:
			bot.edit_message_text(chat_id=chat_id, message_id=initial_message.message_id, text="Invalid command format. Please use '/filter <bin_to_search>'",parse_mode='None')
			return
		value = command_parts[1]
		fun_call = filter(bot, value, message)
		filtered_lines = fun_call[0]
		if filtered_lines:
			file_name = f'Temps/{value}.txt'
			with open(file_name, 'w') as output_file:
				output_file.write('\n'.join(filtered_lines))
			with open(file_name, 'rb') as file_to_send:
				bot.delete_message(message_id=initial_message.message_id,chat_id=chat_id)
				bot.send_document(message.chat.id, file_to_send, caption=f"Cards Found => {fun_call[1]}")
			os.remove(file_name)
		else:
			bot.edit_message_text(chat_id=chat_id, message_id=initial_message.message_id, text="No lines found with that bin in the file. or you didn't reply to a file.")
	else:
		pass
#—————–————–———————––———#
@bot.message_handler(commands=['gef'])#8
def generate_cards(message):
	if bot_working:
		chat_id = message.chat.id
		try:
			initial_message = bot.reply_to(message, "Generating Started...⏳")
			start_time = datetime.datetime.now()
			command_args = message.text.split()[1:]
			a = command_args[0] if len(command_args) > 0 else ""
			e = int(command_args[1]) if len(command_args) > 1 else 5000
			b = command_args[2] if len(command_args) > 2 else ""
			c = command_args[3] if len(command_args) > 3 else ""
			d = command_args[4] if len(command_args) > 4 else ""
			cards_data = ""
			f = 0
			while f < e:
				card_number, exp_m, exp_y, cvv = gen_card(a, b, c, d)
				cards_data += f"{card_number}|{exp_m}|{exp_y}|{cvv}\n"
				f += 1
			file_name = "generated_cards.txt"
			with open(file_name, "w") as file:
				file.write(cards_data)
			end_time = datetime.datetime.now()
			time_taken_seconds = (end_time - start_time).total_seconds()
			time_taken_formatted = "{:.2f}".format(time_taken_seconds)
			with open(file_name, "rb") as file:
				bin_inf = bin_info(a)
				bot.delete_message(message_id=initial_message.message_id,chat_id=chat_id)
				bot.send_document(message.chat.id, file, caption=f"Count =>> {e}\n{bin_inf}\nTook =>>{time_taken_formatted}")
			os.remove(file_name)
		except Exception as ex:
			bot.edit_message_text(chat_id=chat_id, message_id=initial_message.message_id, text=f"An error occurred: {str(ex)}")
	else:
		pass
#—————–————–———————––———#
@bot.message_handler(commands=['gen'])#9
def generate_card(message):
	if bot_working:
		chat_id = message.chat.id
		try:
			initial_message = bot.reply_to(message, "Generating Started...⏳")
			card_info = message.text.split('/gen ', 1)[1]
			def multi_explode(delimiters, string):
				pattern = '|'.join(map(re.escape, delimiters))
				return re.split(pattern, string)
		
			split_values = multi_explode([":", "|", "⋙", " ", "/"], card_info)
			bin_value = ""
			mes_value = ""
			ano_value = ""
			cvv_value = ""
			
			if len(split_values) >= 1:
				bin_value = re.sub(r'[^0-9]', '', split_values[0])
			if len(split_values) >= 2:
				mes_value = re.sub(r'[^0-9]', '', split_values[1])
			if len(split_values) >= 3:
				ano_value = re.sub(r'[^0-9]', '', split_values[2])
			if len(split_values) >= 4:
				cvv_value = re.sub(r'[^0-9]', '', split_values[3])
			cards_data = ""
			f = 0
			while f < 10:
				card_number, exp_m, exp_y, cvv = gen_card(bin_value, mes_value, ano_value, cvv_value)
				cards_data += f"<code>{card_number}|{exp_m}|{exp_y}|{cvv}</code>\n"
				f += 1
			bot.edit_message_text(chat_id=chat_id, message_id=initial_message.message_id, text=cards_data)
		except Exception as e:
			bot.edit_message_text(chat_id=chat_id, message_id=initial_message.message_id, text=f"An error occurred: {e}")
	else:
		pass
#—————–————–———————––———#
@bot.message_handler(commands=['scr'])#10
def send_last_messages(message):
	if bot_working:
		chat_id = message.chat.id
		initial_message = bot.reply_to(message, "Scarping Started...⏳")
		start_time = datetime.datetime.now()
		command_parts = message.text.split()
		if len(command_parts) == 3 and command_parts[0] == '/scr':
			
			username = command_parts[1]
			limit = int(command_parts[2])
			try:
				username = int(username)
			except ValueError:
				pass
			loop = asyncio.new_event_loop()
			asyncio.set_event_loop(loop)
			messages_text = loop.run_until_complete(get_last_messages(username, limit))
			save_to_file(messages_text)
			file_len = len(messages_text.split('\n'))
			end_time = datetime.datetime.now()
			time_taken_seconds = (end_time - start_time).total_seconds()
			time_taken_formatted = "{:.2f}".format(time_taken_seconds)
			captain_info = f"Cards = {file_len}\nTook = {time_taken_formatted}\nSource = {command_parts[1]}"
			with open('combo.txt', 'rb') as file:
				bot.delete_message(message_id=initial_message.message_id,chat_id=chat_id)
				bot.send_document(message.chat.id, file,caption=captain_info)
		else:
			bot.edit_message_text(chat_id=chat_id, message_id=initial_message.message_id, text="command format. Use /scr [username] [limit]")
	else:
		pass
#—————–————–———————––———#
@bot.message_handler(commands=['sk'])#11
def handle_sk_message(message):
	if bot_working:
		chat_id = message.chat.id
		command_parts = message.text.split()
		initial_message = bot.reply_to(message, "Checking Started...⏳")
		if len(command_parts) != 2:
			bot.edit_message_text(chat_id=chat_id, message_id=initial_message.message_id, text= "Invalid command format. Please use '/sk <sk_key>'",parse_mode='none')
			return
		sk = command_parts[1]
		result = check_key(sk)
		bot.edit_message_text(chat_id=chat_id, message_id=initial_message.message_id, text=result)
	else:
		pass
#—————–————–———————––———#
@bot.message_handler(commands=['chk'])#12
def brinetree_chk_command(message):
	if bot_working:
		chat_id = message.chat.id
		try:
			card_details = message.text.split(' ')
			if len(card_details) != 2:bot.send_message(message.chat.id, "Invalid command format. Please use '/chk <card>'",parse_mode='none');return
			card_details = message.text.split(' ')[1]
			initial_message = bot.reply_to(message, "The Checking Started, Wait ⌛")
			result = api(card_details)
			bot_msg = result[4]
			bin_inf = bin_info(result[0])
			edited_message = bot_msg.replace("bin_info",f"═════『 𝐁𝐈𝐍 𝐈𝐍𝐅𝐎 』═════\n{bin_inf}")
			bot.edit_message_text(chat_id=chat_id, message_id=initial_message.message_id, text=edited_message)
		except Exception as e:
			bot.send_message(chat_id=chat_id, text="An error occurred: " + str(e))
	else:
		pass
#—————–————–———————––———#
@bot.message_handler(commands=['str'])#13
def stripe_chk_command(message):
	if bot_working:
		chat_id = message.chat.id
		try:
			card_details = message.text.split(' ')
			if len(card_details) != 2:bot.send_message(message.chat.id, "Invalid command format. Please use '/str <card>'",parse_mode='none');return
			card_details = message.text.split(' ')[1]
			initial_message = bot.reply_to(message, "The Checking Started, Wait ⌛")
			result = process_card(card_details)
			bot_msg = result[4]
			bin_inf = bin_info(result[0])
			edited_message = bot_msg.replace("bin_info",f"═════『 𝐁𝐈𝐍 𝐈𝐍𝐅𝐎 』═════\n{bin_inf}")
			bot.edit_message_text(chat_id=chat_id, message_id=initial_message.message_id, text=edited_message)
		except Exception as e:
			bot.send_message(chat_id=chat_id, text="An error occurred: " + str(e))
	else:
		pass
#—————–————–———————––———#
@bot.message_handler(commands=['pay'])#14
def paypal_chk_command(message):
    if bot_working:
        chat_id = message.chat.id
        try:
            card_details = message.text.split(' ')
            if len(card_details) != 2:
                bot.send_message(message.chat.id, "Invalid command format. Please use '/pay <card>'", parse_mode='none')
                return
            card_details = message.text.split(' ')[1]
            initial_message = bot.reply_to(message, "The Checking Started, Wait ⌛")
            for _ in range (5):
                try:
                    result = process_card_p(card_details)
                    card = result[4]
                    bin_inf = bin_info(result[0])
                    edited_message = (f"{card}")
                    edited_message = edited_message.replace("bin_info",f"═════『 𝐁𝐈𝐍 𝐈𝐍𝐅𝐎 』═════\n{bin_inf}")
                    print(edited_message)
                    bot.edit_message_text(chat_id=chat_id, message_id=initial_message.message_id, text=edited_message)
                    break
                except Exception:pass
        except Exception as e:
            bot.send_message(chat_id=chat_id, text="An error occurred: " + str(e))
    else:
        pass
#—————–————–———————––———#
@bot.message_handler(commands=['filestr']) #15
def stripe_fill_command(message):
	global is_card_checking
	chat_id = message.chat.id
	if bot_working:
		if not is_user_allowed(chat_id):bot.reply_to(message,"You are not allwod to use this bot");return
		bot.reply_to(message,"send the combo file")
		@bot.message_handler(content_types=['document'])
		def handle_card_file(message):
			global is_card_checking
			is_card_checking = True
			try:
				file_info = bot.get_file(message.document.file_id)
				
				downloaded_file = bot.download_file(file_info.file_path)
				
				file_content = downloaded_file.decode('utf-8')
				
				card_lines = file_content.strip().split('\n')
				msg = bot.send_message(chat_id=message.chat.id,text="The Checking Started, Wait ⌛")
#—————–————–———————––———#
				not_working_cards = []
				working_cards = []
				cards_3D_secure = [] 
				insufficient_founds = []
				ccn_cards = []
				live_cards = []
#—————–————–———————––———#
				for card in card_lines:
					if not is_card_checking:return
					result = process_card(card)
					num = result[3]
					lists_mapping = {
						1: working_cards,
						2: live_cards,
						3: insufficient_founds,
						4: ccn_cards,
						5: not_working_cards,
						6: cards_3D_secure}
	
					if num in lists_mapping:
						lists_mapping[num].append(card)
#—————–————–———————––———#
					msg_text = result[1]
					if result[2] == True:
						bot.send_message(chat_id,result[4])
#—————–————–———————––———#
					reply_markup = create_reply_markup(card, len(not_working_cards),len(live_cards), len(working_cards), len(cards_3D_secure) ,len(insufficient_founds),len(ccn_cards),msg_text,len(card_lines))
					try:
						bot.edit_message_text(
chat_id=message.chat.id,
message_id=msg.message_id,
text="Checking in progress Wait...",
reply_markup=reply_markup
					)
					except telebot.apihelper.ApiTelegramException:
						time.sleep(2)
				is_card_checking = False
			except Exception as e:
				print(e)
	else:
			pass
#—————–————–———————––———#
	def create_reply_markup(current_card, num_not_working, num_live, num_working,num_cards_3D_secure, num_insufficient_founds, num_ccn, message_text, All):
		
		markup = telebot.types.InlineKeyboardMarkup()
	
		current_card_button = telebot.types.InlineKeyboardButton(text=f"⌜ • {current_card} • ⌝", callback_data="current_card")
		
		message_button = telebot.types.InlineKeyboardButton(text=f" ⌯ {message_text} ⌯ ", callback_data="message")
		
		working_button = telebot.types.InlineKeyboardButton(text=f"Charged: {num_working}", callback_data="working")

		live_button = telebot.types.InlineKeyboardButton(text=f"Live: {num_live}", callback_data="live")
		
		insufficient_button = telebot.types.InlineKeyboardButton(text=f"Insuff Founds: {num_insufficient_founds}", callback_data="no thing")
		
		ccn_button = telebot.types.InlineKeyboardButton(text=f"CCN: {num_ccn}", callback_data="no thing")
			
		all_button = telebot.types.InlineKeyboardButton(text=f"⌞ • All: {All} ┇ Declined: {num_not_working} ┇OTP: {num_cards_3D_secure} • ⌟", callback_data="no thing")
	
		stop_button = telebot.types.InlineKeyboardButton(text="〄 STOP 〄", callback_data="stop")
	
		markup.row(current_card_button)
		markup.row(message_button)
		markup.row(working_button,live_button)
		markup.row(insufficient_button,ccn_button)
		markup.row(all_button)
		markup.row(stop_button)
		return markup
	@bot.callback_query_handler(func=lambda call: True)
	def handle_callback_query(call):
		global is_card_checking
		if call.data == "stop":
			is_card_checking = False
			bot.answer_callback_query(call.id, text="Card checking stopped.")
#——–——–——–—FILE——–——–—–—–—#
@bot.message_handler(commands=['file'])#16
def brintree_file_command(message):
	global is_card_checking
	chat_id = message.chat.id
	if bot_working:
		if not is_user_allowed(chat_id):bot.reply_to(message,"You are not allwod to use this bot");return
		bot.reply_to(message,"send the combo file")
		@bot.message_handler(content_types=['document'])
		def handle_card_file(message):
			global is_card_checking
			is_card_checking = True
			try:
				file_info = bot.get_file(message.document.file_id)
				
				downloaded_file = bot.download_file(file_info.file_path)
				
				file_content = downloaded_file.decode('utf-8')
				
				card_lines = file_content.strip().split('\n')
				msg = bot.send_message(chat_id=message.chat.id,text="The Checking Started, Wait ⌛")
#—————–————–———————––———#
				not_working_cards = []
				working_cards = []
				risk_cards = [] 
				insufficient_founds = []
				ccn_cards = []
				live_cards = []
#—————–————–———————––———#
				for card in card_lines:
					if not is_card_checking:return
					cc, mes, ano, cvv = map(str.strip, card.split('|'))
					card = (f"{cc}|{mes}|{ano}|{cvv}")
					result = process_card_b(card)
					num = result[3]
					lists_mapping = {
						1: working_cards,
						2: live_cards,
						3: insufficient_founds,
						4: ccn_cards,
						5: not_working_cards,
						6: risk_cards
						}
	
					if num in lists_mapping:
						lists_mapping[num].append(card)
#—————–————–———————––———#
					msg_text = result[1]
					if result[2] == True:
						bot.send_message(chat_id,result[4])
#—————–————–———————––———#
					reply_markup = breintree_markup(card, len(not_working_cards),len(live_cards), len(insufficient_founds),len(ccn_cards),msg_text,len(card_lines),len(risk_cards))
					try:
						bot.edit_message_text(
chat_id=message.chat.id,
message_id=msg.message_id,
text="Checking in progress Wait...",
reply_markup=reply_markup
					)
					except telebot.apihelper.ApiTelegramException:
						time.sleep(2)
				is_card_checking = False
			except Exception as e:
				print(e)
	else:
			pass
#—————–————–———————––———#
	def breintree_markup(current_card, num_not_working, num_live,  num_insufficient_founds, num_ccn, message_text, All,num_risk):
		
		markup = telebot.types.InlineKeyboardMarkup()
	
		current_card_button = telebot.types.InlineKeyboardButton(text=f"⌜ • {current_card} • ⌝", callback_data="current_card")
		
		message_button = telebot.types.InlineKeyboardButton(text=f" ⌯ {message_text} ⌯ ", callback_data="message")
		
		live_button = telebot.types.InlineKeyboardButton(text=f"Live: {num_live}", callback_data="live")
		
		insufficient_button = telebot.types.InlineKeyboardButton(text=f"Insuff Founds: {num_insufficient_founds}", callback_data="no thing")
		
		ccn_button = telebot.types.InlineKeyboardButton(text=f"CCN: {num_ccn}", callback_data="no thing")
			
		all_button = telebot.types.InlineKeyboardButton(text=f"⌞ • All: {All} ┇ Declined: {num_not_working} ┇Risk: {num_risk} • ⌟", callback_data="no thing")
	
		stop_button = telebot.types.InlineKeyboardButton(text="〄 STOP 〄", callback_data="stop")
	
		markup.row(current_card_button)
		markup.row(message_button)
		markup.row(live_button)
		markup.row(insufficient_button,ccn_button)
		markup.row(all_button)
		markup.row(stop_button)
		return markup
	@bot.callback_query_handler(func=lambda call: True)
	def handle_callback_query(call):
		global is_card_checking
		if call.data == "stop":
			is_card_checking = False
			bot.answer_callback_query(call.id, text="Card checking stopped.")
#—————–————–———————––———#
@bot.message_handler(commands=['filep'])#17
def payal_file_command(message):
	global is_card_checking
	chat_id = message.chat.id
	if bot_working:
		if not is_user_allowed(chat_id):bot.reply_to(message,"You are not allwod to use this bot");return
		bot.reply_to(message,"send the combo file")
		@bot.message_handler(content_types=['document'])
		def handle_card_file(message):
			global is_card_checking
			is_card_checking = True
			try:
				file_info = bot.get_file(message.document.file_id)
				
				downloaded_file = bot.download_file(file_info.file_path)
				
				file_content = downloaded_file.decode('utf-8')
				
				card_lines = file_content.strip().split('\n')
				msg = bot.send_message(chat_id=message.chat.id,text="The Checking Started, Wait ⌛")
#—————–————–———————––———#
				not_working_cards = []
				working_cards = []
				risk_cards = [] 
				insufficient_founds = []
				ccn_cards = []
#—————–————–———————––———#
				for card in card_lines:
					if not is_card_checking:return
					cc, mes, ano, cvv = map(str.strip, card.split('|'))
					card = (f"{cc}|{mes}|{ano}|{cvv}")
					result = process_card_p(card)
					num = result[3]
					lists_mapping = {
						1: working_cards,
						2: insufficient_founds,
						3: ccn_cards,
						4: not_working_cards,
						5: risk_cards
						}
	
					if num in lists_mapping:
						lists_mapping[num].append(card)
#—————–————–———————––———#
					msg_text = result[1]
					if result[2] == True:
						bot.send_message(chat_id,result[4])
#—————–————–———————––———#
					reply_markup = breintree_markup(card, len(not_working_cards),len(working_cards), len(insufficient_founds),len(ccn_cards),msg_text,len(card_lines),len(risk_cards))
					try:
						bot.edit_message_text(
chat_id=message.chat.id,
message_id=msg.message_id,
text="Checking in progress Wait...",
reply_markup=reply_markup
					)
					except telebot.apihelper.ApiTelegramException:
						time.sleep(2)
				is_card_checking = False
			except Exception as e:
				print(e)
	else:
			pass
#—————–————–———————––———#
	def breintree_markup(current_card, num_not_working, num_working,  num_insufficient_founds, num_ccn, message_text, All,num_risk):
		
		markup = telebot.types.InlineKeyboardMarkup()
	
		current_card_button = telebot.types.InlineKeyboardButton(text=f"⌜ • {current_card} • ⌝", callback_data="current_card")
		
		message_button = telebot.types.InlineKeyboardButton(text=f" ⌯ {message_text} ⌯ ", callback_data="message")
		
		live_button = telebot.types.InlineKeyboardButton(text=f"Live: {num_working}", callback_data="live")
		
		insufficient_button = telebot.types.InlineKeyboardButton(text=f"Insufficient Funds: {num_insufficient_founds}", callback_data="no thing")
		
		ccn_button = telebot.types.InlineKeyboardButton(text=f"CCN: {num_ccn}", callback_data="no thing")
			
		all_button = telebot.types.InlineKeyboardButton(text=f"⌞ • All: {All} ┇ Declined: {num_not_working} ┇OTP: {num_risk} • ⌟", callback_data="no thing")
	
		stop_button = telebot.types.InlineKeyboardButton(text="〄 STOP 〄", callback_data="stop")
	
		markup.row(current_card_button)
		markup.row(message_button)
		markup.row(live_button)
		markup.row(insufficient_button,ccn_button)
		markup.row(all_button)
		markup.row(stop_button)
		return markup
	@bot.callback_query_handler(func=lambda call: True)
	def handle_callback_query(call):
		global is_card_checking
		if call.data == "stop":
			is_card_checking = False
			bot.answer_callback_query(call.id, text="Card checking stopped.")
#—————–————–———————––———#
bot.polling()