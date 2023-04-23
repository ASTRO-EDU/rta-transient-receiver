import voeventparse as vp

from voeventhandler.voeventsorting import VoeventSorting
from dummy_notices import DummyNotices

class DummyEvent(object):
    """
    Class containing standard voevent from different networks
    """

if __name__ == "__main__":
    """
    this main test the correct working of the sorting and extractors mechanism
    as input is given a generic voevent, then the sorting mechanism is used to 
    sort the voevent in the correct extractor, then the extractor is used to
    extract the data from the voevent.
    """
    assert VoeventSorting(vp.loads(DummyNotices.from_event(DummyNotices.DUMMY_VOEVENT_AGILE, {})))

    

