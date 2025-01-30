import imaplib
import email
import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Hardcoded Gmail credentials
EMAIL_ACCOUNT = "simonsteve1076@gmail.com"
EMAIL_PASSWORD = "yrfa nlez qcrm tcoi"

# Gmail IMAP and SMTP settings
IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Predefined responses
RESPONSES = {
    "cost": "Our service costs $50 per month.",
    "services": "We offer AI automation and chatbot solutions.",
    "contact": "You can contact us at support@ruby.com.",
    "hello": "Hello! How can I assist you today?",
    "price": "Our service costs $50 per month. Let us know if you need more details!"
}

# Ignore automated emails
IGNORED_SENDERS = ["no-reply", "noreply", "newsletter", "automated", "info@", "support@", "noreply@"]

def check_email():
    """Checks inbox for new, unread emails from real senders."""
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    mail.select("inbox")

    # Search for unread emails
    result, data = mail.search(None, "UNSEEN")
    mail_ids = data[0].split()

    emails = []
    for mail_id in mail_ids:
        result, msg_data = mail.fetch(mail_id, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                sender_email = email.utils.parseaddr(msg["From"])[1]
                subject = msg["Subject"]
                body = ""

                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            break
                else:
                    body = msg.get_payload(decode=True).decode()

                # Filter out automated emails
                if not any(keyword in sender_email.lower() for keyword in IGNORED_SENDERS):
                    emails.append((sender_email, subject, body))

    mail.logout()
    return emails

def generate_response(email_body):
    """Generates an automatic response based on email content."""
    email_body = email_body.lower()

    for key, response in RESPONSES.items():
        if key in email_body:
            return response
    
    return "Thank you for reaching out! We will get back to you shortly."

def send_email(recipient, response):
    """Sends an automated email response."""
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ACCOUNT
        msg["To"] = recipient
        msg["Subject"] = "Re: Your Inquiry"

        msg.attach(MIMEText(response, "plain"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ACCOUNT, recipient, msg.as_string())
        server.quit()

        print(f"Replied to {recipient} with: {response}")

    except Exception as e:
        print(f"Failed to send email to {recipient}: {e}")

def run_email_bot():
    """Runs the bot continuously and replies when a new email arrives."""
    print("Email bot is running...")

    while True:
        emails = check_email()
        if emails:
            for sender, subject, body in emails:
                print(f"New email from: {sender}\nSubject: {subject}\nBody: {body}\n")

                response = generate_response(body)
                send_email(sender, response)
        
        time.sleep(10)  # Waiting time

if __name__ == "__main__":
    run_email_bot()
