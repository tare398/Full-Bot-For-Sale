import re
from telethon.sync import TelegramClient

async def rearrange_format(text):
    if not isinstance(text, (str, bytes)):
        return None
    
    card_pattern3 = r"\b(\d{15,16})[\s|/-]*(\d{2})[\s|/-]*(\d{2,4})[\s|/-]*(\d{3,4})\b"

    match3 = re.search(card_pattern3, text)
    
    if match3:
        return f"{match3.group(1)}|{match3.group(2)}|{match3.group(3)}|{match3.group(4)}"
    else:
        return None


async def get_last_messages(username, limit):
    api_id = 17058698
    api_hash = "088f8d5bf0b4b5c0536b039bb6bdf1d2"
    phone_number = "رقم هاتفك مع رمز الدولة"
    
    async with TelegramClient(phone_number, api_id, api_hash) as client:
        if isinstance(username, int):
            entity = username
        else:
            entity = await client.get_entity(username)
        
        messages = await client.get_messages(entity, limit=limit)

        matching_texts = []
        for message in reversed(messages):
            formatted_text = await rearrange_format(message.text)
            if formatted_text is not None:
                matching_texts.append(formatted_text)
        
        return "\n".join(matching_texts)
        
        
def save_to_file(text):
    with open('combo.txt', 'w') as file:
        file.write(text)
        