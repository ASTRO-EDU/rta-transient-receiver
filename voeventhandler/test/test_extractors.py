import pytest
import voeventparse as vp

from dummy_notices import DummyNotices
from voeventhandler.extractors.gcndataextractor import GncDataExtractor
from voeventhandler.extractors.chimedataextractor import ChimeDataExtractor
from voeventhandler.extractors.integraldataextractor import IntegralDataExtractor
from voeventhandler.extractors.ligodataextractor import LigoDataExtractor
from voeventhandler.extractors.agiledataextractor import AgileDataExtractor

class TestExtractors:

    @pytest.mark.parametrize("notice_str", ["ligo_initial.xml", "ligo_preliminary.xml", "ligo_no_model.xml"], indirect=True)
    def test_ligo(self, notice_str):
        voedata = LigoDataExtractor().extract(vp.loads(notice_str))
        print(LigoDataExtractor().get_ligo_attributes(vp.loads(notice_str)))
        assert voedata

    @pytest.mark.parametrize("notice_str", ["icecube_bronze.xml"], indirect=True)
    def test_gcn(self, notice_str):
        assert GncDataExtractor().extract(vp.loads(notice_str))
    
    def test_chime(self):
        voe = vp.loads(DummyNotices.from_event(DummyNotices.DUMMY_VOEVENT_CHIME, {}))
        chime = ChimeDataExtractor()
        assert chime.extract(voe)

    def test_integral(self):
        voe = vp.loads(DummyNotices.from_event(DummyNotices.DUMMY_VOEVENT_INTEGRAL, {}))
        integral = IntegralDataExtractor()
        assert integral.extract(voe)
    
    def test_agile(self):
        voe = vp.loads(DummyNotices.from_event(DummyNotices.DUMMY_VOEVENT_AGILE, {}))
        agile = AgileDataExtractor()
        assert agile.extract(voe)
    
    def test_fermi(self):
        voe = vp.loads(DummyNotices.from_event(DummyNotices.DUMMY_VOEVENT_GCN_FERMI, {}))
        fermi = GncDataExtractor()
        assert fermi.extract(voe)

    def test_maxi(self):
        voe = vp.loads(DummyNotices.from_event(DummyNotices.DUMMY_VOEVENT_GCN_MAXI, {}))
        maxi = GncDataExtractor()
        assert maxi.extract(voe)
    
        

