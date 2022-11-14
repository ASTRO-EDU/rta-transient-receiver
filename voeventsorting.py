from extractors.agiledataextractor import AgileDataExtractor
from extractors.chimedataextractor import ChimeDataExtractor
from extractors.gcndataextractor import GncDataExtractor
from extractors.integraldataextractor import IntegralDataExtractor
from extractors.ligodataextractor import LigoDataExtractor
from extractors.utilis.voeventdata import VoeventData

class VoeventSorting(object):
    def __init__(self) -> None:
        self.agile = AgileDataExtractor()
        self.chime = ChimeDataExtractor()
        self.gcn = GncDataExtractor()
        self.integral = IntegralDataExtractor()
        self.ligo = LigoDataExtractor()

    def sort(self, voevent) -> VoeventData:
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