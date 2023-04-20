from email.message import EmailMessage
from pathlib import Path
import smtplib
import json

class EmailNotifier:
    """
    This class is used to provides a simple interface to send emails.
    """
    def __init__(self, config_file):
        """
        When the class is created, it reads the configuration file and sets the email parameters
        """
        with open(config_file) as f:
            config = json.load(f)
            self.mail = Mail(config["sender_email"], config["sender_email_password"])
            self.to = config["email_recivers"]
            self.to_developers = config["diagnostic_email_receivers"]
            self.packet_with_email_notification = config["packet_with_email_notification"]
            self.important_email_subject = config["important_email_subject"]

    def diagnosticEmails(self, name, exception):
        self.mail.send_email(self.to_developers, f"Exception alert for {name}", f"Exception: {exception}")

    def sendEmails(self, voeventdata, result_row):
        """
        This method is used to send the emails corresponding to the given VoEvent.
        """
        if voeventdata.packet_type in self.packet_with_email_notification or voeventdata.is_ste: #it will send an email for GW, Neutrino event or STE events
            
            subject = f'Notice alert for {voeventdata.name}'
            
            body = f'The platform received a notice for the {voeventdata.name} event at {voeventdata.UTC} for trigger {voeventdata.trigger_id} with sequence number {voeventdata.seqNum} \n'
            
            if voeventdata.ligo_attributes:
                # load as json
                try:
                    for key, value in voeventdata.ligo_attributes.items():
                        body += f"\n{key}: {value}"
                except ValueError:
                    body += f"\n{voeventdata.ligo_attributes}"

            if self._is_important(voeventdata):
                subject = self.important_email_subject + " " + subject
            self.mail.send_email(self.to, subject, body)
        
        #check if there are correlated instruments and send an email if so
        if result_row:
            subject = f'Correlations for {voeventdata.name}'
            body = f'The platform received a notice for the {voeventdata.name} at {voeventdata.UTC} for trigge {voeventdata.trigger_id} with sequence number {voeventdata.seqNum} with the following correlated events: {str(result_row)}'
            self.mail.send_email(self.to, subject, body)

        return subject, body
    
    def _is_important(self, voeventdata) -> bool:
        """
        This method is used to check if the given VoEvent is important.
        Everione is using the code can change this method to define what is important for him using the 
        data saved in the object voeventdata.
        """

        return False

class Mail:
    
    def __init__(self, gmail_user, gmail_password) -> None:
        """
        When the class is created, it sets the email parameters
        """
        self.gmail_user = gmail_user
        self.gmail_password = gmail_password
    
    def send_email(self, to, subject, body):
        """
        given a list of recipients, a subject and a body, this method sends an email to all the recipients
        """
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = self.gmail_user
        msg['To'] = ', '.join(to)
    
        try:
            smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            smtp_server.ehlo()
            smtp_server.login(self.gmail_user, self.gmail_password)
            smtp_server.send_message(msg)
            smtp_server.close()
            print("Email sent successfully!")
        except Exception as ex:
            print("Something went wrong in send_email:", ex)