def filter(bot, value, message):
    if message.reply_to_message and message.reply_to_message.document:
        file_info = bot.get_file(message.reply_to_message.document.file_id)
        file_path = file_info.file_path
        downloaded_file = bot.download_file(file_path)

        content = downloaded_file.decode('utf-8').split('\n')

        filtered_lines = [line.strip() for line in content if line.startswith(value)]
        num_lines = len(filtered_lines)
        return filtered_lines, num_lines
    else:
        return []