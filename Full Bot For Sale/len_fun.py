def count_lines(message,bot):
    if message.reply_to_message and message.reply_to_message.document:
        file_info = message.reply_to_message.document
        file_id = file_info.file_id

        file_info = bot.get_file(file_id)
        file_path = file_info.file_path
        downloaded_file = bot.download_file(file_path)

        lines = downloaded_file.decode('utf-8').splitlines()
        num_lines = len(lines)

        return f'The file has {num_lines} lines.'
    else:
        return 'Please reply to a file with the /len command to count its lines.'