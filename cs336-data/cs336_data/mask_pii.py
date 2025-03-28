import re

# Mask all email addresses in the input text
def mask_emails(text: str):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    masked_text, count = re.subn(email_pattern, '|||EMAIL_ADDRESS|||', text)
    return masked_text, count

# Mask common U.S. phone number formats in the input text
def mask_phone_numbers(text: str):
    phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    masked_text, count = re.subn(phone_pattern, '|||PHONE_NUMBER|||', text)
    return masked_text, count

# Mask IPv4 addresses in the input text
def mask_ip_addresses(text: str):
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    masked_text, count = re.subn(ip_pattern, '|||IP_ADDRESS|||', text)
    return masked_text, count
