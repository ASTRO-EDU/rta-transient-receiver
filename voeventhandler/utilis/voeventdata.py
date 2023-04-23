from enum import Enum
from voeventhandler.utilis.instrumentid import InstrumentId

class PacketType(Enum):
    Ligo_Preliminary = 150
    Ligo_Initial = 151
    Ligo_Update = 152
    
class Voeventdata:
    """
    This class is used to store the data relative to a specific voevent.
    When is created, it is filled with the data extracted from the voevent.
    Then during the database insertion the fiend seqNum and received_science_alert_id are set.
    """


    def __init__(self, datasource, is_ste, instrument_id, trigger_id,
                    packet_type, isoTime, UTC, network_id, l, b, position_error,
                    notice, configuration, url, contour, ligo_attributes : dict,
                    name, seqNum, tstart, tstop, last, isTest) -> None:
        
        self.datasource = datasource
        self.is_ste = is_ste
        self.instrument_id = instrument_id
        self.trigger_id = trigger_id
        self.packet_type = int(packet_type)
        self.isoTime = isoTime
        self.UTC = UTC
        self.network_id = network_id
        self.l = l
        self.b = b
        self.position_error = position_error
        self.notice = notice
        self.configuration = configuration
        self.url = url
        self.contour = contour
        self.ligo_attributes = ligo_attributes
        self.name = name
        self.seqNum = seqNum
        self.tstart = tstart
        self.tstop = tstop
        self.last = last
        self.isTest = isTest

    def isTestNotice(self):
        return self.isTest

    def set_seq_num(self, seqNum):
        self.seqNum = seqNum

    def set_received_science_alert_id(self, receivedsciencealertid):
        self.receivedsciencealertid = receivedsciencealertid

    def __str__(self):
        return f"InstrumentID: {self.instrument_id}, name:{self.name}, seqNum {self.seqNum}, triggerid: {self.trigger_id}, packetType: {self.packet_type},time: {self.UTC}, l: {self.l}, b: {self.b}, url: {self.url}"
    

    
    def get_email_body(self, instrument_id, correlations=[]):

        body = ""

        if self.packet_type in [e.value for e in PacketType]:
            body += f"\nNotice type: {PacketType(self.packet_type).name}\n"

        if instrument_id in [InstrumentId.LIGO.value, InstrumentId.LIGO_TEST.value]:
            body += f'bns={round(self.ligo_attributes["bns"], 10)}%\n'
            body += f'nsbh={round(self.ligo_attributes["nsbh"], 10)}%\n'
            body += '\n'
            body += f'significant={self.ligo_attributes["significant"]}\n'
            body += f'far={self.ligo_attributes["far"]}\n'
            body += f'Event page={self.ligo_attributes["event_page"]}\n'
            body += '\n'

        if len(correlations) > 0:
            body += 'Correlations found: \n'
            for correlation in correlations:
                body += f'- {correlation}\n'        

        return body

    def is_significant(self):
        if self.packet_type in [PacketType.Ligo_Initial.value, PacketType.Ligo_Preliminary.value, PacketType.Ligo_Update.value]:
            if self.ligo_attributes["significant"] == 1:
                return True
        return False