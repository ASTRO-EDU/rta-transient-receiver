import voeventparse as vp
from time import time, sleep
from dummy_notices import DummyNotices
from voeventhandler.voeventhandler import VoeventHandler

class TestVoeventHandler:

    def test_handler(self, config, clean_database):
        changeDict = {
            "name=\"GraceID\" value=\"MS230414r\"" : "name=\"GraceID\" "+f"value=\"{time()}\""
        }
        voe = vp.loads(DummyNotices.from_event(DummyNotices.DUMMY_VOEVENT_LIGO_INITIAL, changeDict))

        vh = VoeventHandler(config, disable_email=True)

        inserted, mail_sent, voeventdata, correlations = vh.handleVoevent(voe)
        assert not inserted
        assert not mail_sent

        sleep(10)

        voe.What.GraceID = str(time())
        inserted, mail_sent, voeventdata, correlations = vh.handleVoevent(voe)
        assert inserted
        assert not mail_sent

        voe.What.GraceID = str(time())
        inserted, mail_sent, voeventdata, correlations = vh.handleVoevent(voe)
        assert not inserted
        assert not mail_sent
        