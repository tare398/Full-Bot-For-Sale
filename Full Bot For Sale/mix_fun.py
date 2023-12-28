import random
def mix_lines(file_content):
    try:
        lines = file_content.decode('utf-8').splitlines()
        random.shuffle(lines)
        return '\n'.join(lines)
    except Exception as e:
        return f"An error occurred: {str(e)}"