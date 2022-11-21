from voeventhandler.extractors.agiledataextractor import AgileDataExtractor
from voeventhandler.extractors.chimedataextractor import ChimeDataExtractor
from voeventhandler.extractors.gcndataextractor import GncDataExtractor
from voeventhandler.extractors.integraldataextractor import IntegralDataExtractor
from voeventhandler.extractors.ligodataextractor import LigoDataExtractor

class VoeventSorting(object):
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

        if "gcn" in voevent.attrib['ivorn']:
            return (self.gcn.extract(voevent))
        elif "gwnet" in voevent.attrib['ivorn']:
            return (self.ligo.extract(voevent))
        elif "chimenet" in voevent.attrib['ivorn']:
            return (self.chime.extract(voevent))
        elif "INTEGRAL" in voevent.attrib['ivorn']:
            return (self.integral.extract(voevent))
        elif "AGILE" in voevent.attrib['ivorn']:
            return (self.agile.extract(voevent))
        else:
            raise Exception(f"Notice not supported  ivorn is {self.voevent.attrib['ivorn']}")