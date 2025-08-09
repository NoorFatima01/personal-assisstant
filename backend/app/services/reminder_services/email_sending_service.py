import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config.email_config import SMTP_SERVER, SMTP_PORT, SMTP_EMAIL, SMTP_PASSWORD

class EmailSendingService:
    @staticmethod
    def send_email(to_email:str, subject:str, body:str):
        msg = MIMEMultipart()
        msg['From'] = SMTP_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_EMAIL, SMTP_PASSWORD)
                server.sendmail(SMTP_EMAIL, to_email, msg.as_string())
        except Exception as e:
            print(f"Error sending email: {e}")