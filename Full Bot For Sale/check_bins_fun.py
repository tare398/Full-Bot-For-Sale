import re

def extract_bins(message,bot):
    try:
        if message.reply_to_message and message.reply_to_message.document:
            file_info = message.reply_to_message.document
            file_id = file_info.file_id
            file_info = bot.get_file(file_id)
            file_path = file_info.file_path

            downloaded_file = bot.download_file(file_path)
            file_content = downloaded_file.decode('utf-8')

            bins_count = {}
            card_pattern = re.compile(r'^\d{6}')

            for line in file_content.splitlines():
                match = card_pattern.match(line)
                if match:
                    bin = match.group()
                    bins_count[bin] = bins_count.get(bin, 0) + 1

            return bins_count

        else:
            return None
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")

