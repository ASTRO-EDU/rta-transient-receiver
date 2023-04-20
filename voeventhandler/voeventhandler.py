from voeventhandler.voeventsorting import VoeventSorting
from voeventhandler.databaseinterface import DatabaseInterface
from voeventhandler.emailnotifier import EmailNotifier

class VoeventHandler:
    """
    This class meant to be a wrapper for the voeventhandler, it will handle the 
    voevent database insertion and email notification. 
    """
    
    def __init__(self, config_file):
        """
        When the class is created, the database interface and the email notifier are created.
        """
        self.db = DatabaseInterface(config_file)
        self.email_notifier = EmailNotifier(config_file)
        self.voevent_sorter = VoeventSorting()

    def handleVoevent(self, voevent):
        """
        This method is used to handle a voevent. It will first sort the voevent and then insert it in the database.
        Then it will handle the email notification.
        The parameter voevent is expected to be an xml object.
        """
        try:
            voeventdata = self.voevent_sorter.sort(voevent)
            self.db.insert_voevent(voeventdata)
            result_row = self.db.meange_correlated_instruments(voeventdata)
            self.email_notifier.sendEmails(voeventdata, result_row)
        except Exception as e:
            self.email_notifier.diagnosticEmails(voevent.attrib['ivorn'], e)
            raise e
        return voeventdata