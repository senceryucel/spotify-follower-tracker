import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class GmailSender:
    def __init__(self, configs) -> None:
        # Email config
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = configs["mail_from"]
        self.sender_password = configs["mail_password"]  # created with gmail - app password
        self.receiver_email = configs["mail_to"]

    
    def send_message(self, message_subject, message):
        # Create the email message
        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = self.receiver_email
        msg["Subject"] = message_subject
        msg.attach(MIMEText(message, "plain"))

        # Connect to the SMTP server
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            text = msg.as_string()  # as_string() converts the MIMEMultipart object to string
            
            # Send the email
            server.sendmail(self.sender_email, self.receiver_email, text)
            print("Email sent successfully!")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
        finally:
            server.quit()