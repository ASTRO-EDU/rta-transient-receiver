
import smtplib
from email.message import EmailMessage

class Mail:
    
    def __init__(self, gmail_user, gmail_password) -> None:
        """
        When the class is created, it sets the email parameters
        """
        self.gmail_user = gmail_user
        self.gmail_password = gmail_password

    def buildEmailMessage(self, to, subject, body):
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = self.gmail_user
        msg['To'] = ', '.join(to)
        return msg
    
    def send_email(self, emailMessage: EmailMessage):
        """
        Given a list of recipients, a subject and a body, this method sends an email to all the recipients
        """
        try:
            smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp_server.ehlo()
            smtp_server.login(self.gmail_user, self.gmail_password)
            smtp_server.send_message(emailMessage)
            smtp_server.close()
            print("Email sent successfully!")
            return True
        except Exception as ex:
            print("Something went wrong in send_email:", ex)
            return False
