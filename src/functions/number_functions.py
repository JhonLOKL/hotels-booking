import re

def ExtractNumber(text):
    match = re.search(r'\d+', text)
    if match:
        return int(match.group())
    return None