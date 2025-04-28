import unicodedata
import re

def sanitize_search_string(text: str) -> str:
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text.lower()

def prepares_string_for_search(text: str) -> str:
    text = sanitize_search_string(text)
    return text.replace(' ', '+')