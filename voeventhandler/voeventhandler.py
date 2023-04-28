import json
from time import time
from datetime import datetime
from voeventhandler.utils import Timer
from voeventhandler.voeventsorting import VoeventSorting
from voeventhandler.databaseinterface import DatabaseInterface
from voeventhandler.emailnotifier import EmailNotifier

class VoeventHandler:
    """
    This class meant to be a wrapper for the voeventhandler, it will handle the 
    voevent database insertion and email notification. 
    """
    
    def __init__(self, config_file, disable_email=False):
        """
        When the class is created, the database interface and the email notifier are created.
        """
        self.voevent_sorter = VoeventSorting()
        
        self.db = DatabaseInterface(config_file)

        self.email_notifier = EmailNotifier(config_file)

        with open(config_file) as f:
            self.disable_test_notices_seconds = self.config = json.load(f)["disable_test_notices_seconds"]

        self.timer = Timer()

    def canProcessTestNotice(self):
        if self.timer.check_elapsed() < self.disable_test_notices_seconds:
            print(f"Test notice received, but disabled for {self.disable_test_notices_seconds} seconds. latest_test_notice_time: {self.timer.get_time()}")
            return False
        print("Resetting timer for test notices")
        self.timer.reset()
        return True
        
    def handleVoevent(self, voevent):
        """
        This method is used to handle a voevent. It will first sort the voevent and then insert it in the database.
        Then it will handle the email notification.
        The parameter voevent is expected to be an xml object.
        """
        print(f"\n{datetime.now()} New notice! Handling voevent: {voevent.attrib['ivorn']}")
        
        try:
            voeventdata = self.voevent_sorter.sort(voevent)
            
            if voeventdata.isTestNotice() and not self.canProcessTestNotice():
                return False, [], voeventdata, []

            inserted = self.db.insert_voevent(voeventdata)
            correlations = self.db.find_correlated_instruments(voeventdata)
            sent, _ = self.email_notifier.sendEmails(voeventdata, correlations)

        except Exception as e:
            self.email_notifier.sendDiagnosticEmail(voevent.attrib['ivorn'], e+"\n\n\n"+str(voevent))
            raise e

        return inserted, sent, voeventdata, correlations