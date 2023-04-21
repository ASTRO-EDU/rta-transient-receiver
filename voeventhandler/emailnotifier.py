import json
from voeventhandler.mail import Mail
from voeventhandler.utilis.instrumentid import InstrumentId

class EmailNotifier:
    """
    This class is used to provides a simple interface to send emails.
    """
    def __init__(self, config_file):
        """
        When the class is created, it reads the configuration file and sets the email parameters
        """        
        with open(config_file) as f:
            self.config = json.load(f)

        if self.config["enabled"]:
            if self.config["sender_email"] == "" or self.config["sender_email_password"] == "":
                raise Exception("Email sender and password are required")
            if len(self.config["email_receivers"]) == 0:
                raise Exception("Email receivers are required")
        
        self.mail = Mail(self.config["sender_email"], self.config["sender_email_password"])
        

    def sendDiagnosticEmail(self, name, exception):
        if len(self.config["developer_email_receivers"]) > 0:
            self.mail.send_email(self.mail.buildEmailMessage(self, self.config["developer_email_receivers"], f"Exception alert for {name}", f"Exception: {exception}"))
            print("Diagnostic email sent successfully!")
            return True
        print("No developer email receivers, skipping email")
        return False

    def writeAlertEmail(self, voeventdata, correlations=[]):
        subject = f'Notice alert for {voeventdata.name} TriggerID={voeventdata.trigger_id}'
        body = f'The platform received a notice for the {voeventdata.name} event at {voeventdata.UTC} for trigger {voeventdata.trigger_id} with sequence number {voeventdata.seqNum} \n'
        body += voeventdata.get_email_body(voeventdata.instrument_id, correlations)
        return subject, body

    def checkIfEmailCanBeSent(self, voeventdata, correlations):
        """
        This method is used to filter the email that will be sent.
        """
        # if the instrument is not LIGO and there's correlations with LIGO events we send the email anyway
        if self.checkCorrelationWithGW(voeventdata, correlations):
            return True

        if voeventdata.packet_type not in self.config["packet_with_email_notification"]:
            print("Packet type is not in the list of packet with email notification, skipping email")
            return False

        if voeventdata.is_ste and self.config["skip_ste"]:
            print("Email notification for STE event are disabled and event is STE, skipping email")
            return False

        if voeventdata.instrument_id == InstrumentId.LIGO_TEST.value and self.config["skip_ligo_test"]:
            print("Email notification for LIGO_TEST are disabled and event is LIGO_TEST, skipping email")
            return False

        if voeventdata.instrument_id == InstrumentId.LIGO.value or voeventdata.instrument_id == InstrumentId.LIGO_TEST.value:
            if not voeventdata.is_significant() and self.config["skip_ligo_not_significant"]:
                print("Email notification for LIGO not significant event are disabled and event is not significant, skipping email")
                return False

        return True
    
    def checkCorrelationWithGW(self, voeventdata, correlations):
        # if the instrument is not LIGO we check correlations with LIGO events 
        if voeventdata.instrument_id not in [InstrumentId.LIGO.value, InstrumentId.LIGO_TEST.value]:
            for corr in correlations:
                if corr["instrument_name"] in ["LIGO", "LIGO_TEST"]:
                    print("Correlation with LIGO event found, sending email")
                    return True
        

    def sendEmails(self, voeventdata, correlations):
        """
        This method is used to send the emails corresponding to the given VoEvent.
        """
        emailMessage = None

        if(not self.checkIfEmailCanBeSent(voeventdata, correlations)):
            return False, None

        subject, body = self.writeAlertEmail(voeventdata, correlations)

        emailMessage = self.mail.buildEmailMessage(self.config["email_receivers"], subject, body)

        if not self.config["enabled"]:        
            print("The email send is disabled")
            return False, emailMessage

        self.mail.send_email(emailMessage)
        print("Email sent successfully!")
        return True, emailMessage
        

    
        
    