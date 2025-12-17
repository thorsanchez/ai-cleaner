import re

def clean_text(text: str) -> str:
    #ef ekkis tring
    if not isinstance(text, str):
        return ""
    
    text = text.lower()
    #eypa öllu sem er ekki bil, numer eða stafir
    text = re.sub(r"[^\w\s]", "", text)
    #max eitt bil
    text = re.sub(r"\s+", " ", text)
    return text.strip() #taka bil að framan og aftan
