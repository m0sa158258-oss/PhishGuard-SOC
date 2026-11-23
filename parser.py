import re
from urllib.parse import urlparse

def parse_email_content(raw_email_text: str):
    # استخدام re.IGNORECASE والتعامل مع المسافات بمرونة أكبر
    sender_match = re.search(r"From:\s*(.*)", raw_email_text, re.IGNORECASE)
    subject_match = re.search(r"Subject:\s*(.*)", raw_email_text, re.IGNORECASE)
    
    sender = sender_match.group(1).strip() if sender_match else "Unknown"
    subject = subject_match.group(1).strip() if subject_match else "Unknown"

    # استخراج جميع الروابط الموجودة في الإيميل
    urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', raw_email_text)
    unique_urls = list(set(urls))

    parsed_urls_info = []
    for url in unique_urls:
        parsed = urlparse(url)
        parsed_urls_info.append({
            "url": url,
            "domain": parsed.netloc,
            "path": parsed.path
        })

    return {
        "sender": sender,
        "subject": subject,
        "extracted_urls": parsed_urls_info,
        "total_urls": len(unique_urls)
    }

if __name__ == "__main__":
    sample_email = """
    From: security-alert@paypa1-update.com
    Subject: Urgent: Verify your account immediately!
    
    Dear customer, please click the link below to verify your account:
    https://login.paypa1-update.com/auth/login?token=xyz123
    """
    
    result = parse_email_content(sample_email)
    print("--- Phishing Email Analysis Result ---")
    print(f"Sender: {result['sender']}")
    print(f"Subject: {result['subject']}")
    print(f"Extracted URLs: {result['extracted_urls']}")