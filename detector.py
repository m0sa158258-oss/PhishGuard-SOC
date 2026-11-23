import re

def analyze_phishing_indicators(parsed_data):
    """
    محرك كشف التصيد الاحتيالي (Detection Engine)
    يقوم بفحص المرسل، الموضوع، والروابط للبحث عن علامات مشبوهة
    """
    score = 0
    indicators = []

    sender = parsed_data.get("sender", "").lower()
    subject = parsed_data.get("subject", "").lower()
    urls = parsed_data.get("extracted_urls", [])

    # 1. فحص الكلمات المفتاحية المتعلقة بالاستعجال أو التهديد في العنوان أو المحتوى
    urgent_keywords = ["urgent", "immediate", "verify", "suspended", "action required", "locked"]
    for keyword in urgent_keywords:
        if keyword in subject:
            score += 25
            indicators.append(f"Suspicious keyword found in subject: '{keyword}'")
            break

    # 2. فحص الدومينات المشبوهة أو وجود استبدال حروف (Typosquatting مثل paypa1)
    suspicious_patterns = ["paypa1", "g00gle", "micros0ft", "app1e", "netflix-login", "verify-account"]
    for url_info in urls:
        domain = url_info.get("domain", "").lower()
        for pattern in suspicious_patterns:
            if pattern in domain:
                score += 50
                indicators.append(f"Typosquatting / Suspicious domain detected: {domain}")

    # 3. تحديد مستوى الخطورة بناءً على النتيجة الإجمالية (Risk Verdict)
    if score >= 60:
        verdict = "HIGH / Critical Phishing"
    elif score >= 30:
        verdict = "Medium Risk - Suspicious"
    else:
        verdict = "Low Risk / Clean"

    return {
        "risk_score": score,
        "verdict": verdict,
        "triggered_indicators": indicators
    }

if __name__ == "__main__":
    # عдина تجريبية لتحليل إيميل احتيالي
    sample_parsed = {
        "sender": "security-alert@paypa1-update.com",
        "subject": "urgent: verify your account immediately!",
        "extracted_urls": [
            {"url": "https://login.paypa1-update.com/auth", "domain": "login.paypa1-update.com", "path": "/auth"}
        ]
    }
    
    analysis = analyze_phishing_indicators(sample_parsed)
    print("--- Detection Engine Results ---")
    print(f"Risk Score: {analysis['risk_score']}/100")
    print(f"Verdict: {analysis['verdict']}")
    print(f"Indicators: {analysis['triggered_indicators']}")