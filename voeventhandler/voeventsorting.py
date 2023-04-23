from voeventhandler.extractors.agiledataextractor import AgileDataExtractor
from voeventhandler.extractors.chimedataextractor import ChimeDataExtractor
from voeventhandler.extractors.gcndataextractor import GncDataExtractor
from voeventhandler.extractors.integraldataextractor import IntegralDataExtractor
from voeventhandler.extractors.ligodataextractor import LigoDataExtractor

class VoeventSorting:
    def __init__(self) -> None:
        """
        When the class is created, the extractors are created too
        """
        self.agile = AgileDataExtractor()
        self.chime = ChimeDataExtractor()
        self.gcn = GncDataExtractor()
        self.integral = IntegralDataExtractor()
        self.ligo = LigoDataExtractor()

    def sort(self, voevent):
        """
        This method is used to sort the voevent. 
        The sorting method is based on the field ivorn of the voevent.
        If the instrument is not supported, the method raise an exception.
        """
        ivorn = voevent.attrib['ivorn']
        
        if "gcn" in ivorn:
            print("New GCN notice")
            return (self.gcn.extract(voevent))

        # Handle different networks
        
        if "gwnet" in ivorn:
            print("New LIGO notice")
            return (self.ligo.extract(voevent))

        if "chimenet" in ivorn:
            print("New CHIME notice")
            return (self.chime.extract(voevent))

        if "INTEGRAL" in ivorn:
            print("New INTEGRAL notice")
            return (self.integral.extract(voevent))

        if "AGILE" in ivorn:
            print("New AGILE notice")
            return (self.agile.extract(voevent))
        
        raise Exception(f"Notice not supported, ivorn is {ivorn}")