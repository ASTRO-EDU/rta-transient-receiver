from comet.plugins.extractors.agiledataextractor import AgileDataExtractor
from comet.plugins.extractors.chimedataextractor import ChimeDataExtractor
from comet.plugins.extractors.gcndataextractor import GncDataExtractor
from comet.plugins.extractors.integraldataextractor import IntegralDataExtractor
from comet.plugins.extractors.ligodataextractor import LigoDataExtractor
from comet.plugins.voeventdata import Voeventdata

class VoeventSorting(object):
    def __init__(self) -> None:
        self.agile = AgileDataExtractor()
        self.chime = ChimeDataExtractor()
        self.gcn = GncDataExtractor()
        self.integral = IntegralDataExtractor()
        self.ligo = LigoDataExtractor()

    def sort(self, voevent) -> Voeventdata:
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