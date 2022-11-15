from voeventhandler.test.test_voevents import DUMMY_VOEVENT_GCN, DUMMY_VOEVENT_INTEGRAL, DUMMY_VOEVENT_CHIME, DUMMY_VOEVENT_LIGO, DUMMY_VOEVENT_LIGO_INITIAL, DUMMY_VOEVENT_LIGO_PRELIMINARY, DUMMY_VOEVENT_GCN_FERMI, DUMMY_VOEVENT_GCN_MAXI, DUMMY_VOEVENT_AGILE
from voeventhandler.voeventhandler import VoeventHandler
import voeventparse as vp

"""
#trick for imoport from parent directory
import sys
from os.path import dirname, abspath
d = dirname(dirname(abspath(__file__)))
sys.path.append(d)
"""

class DummyEvent(object):
    """
    Class containing standard voevent from different networks
    """
    gcn = DUMMY_VOEVENT_GCN
    chime = DUMMY_VOEVENT_CHIME
    integral = DUMMY_VOEVENT_INTEGRAL
    fermi = DUMMY_VOEVENT_GCN_FERMI
    ligo = DUMMY_VOEVENT_LIGO
    ligo2 = DUMMY_VOEVENT_LIGO_PRELIMINARY
    ligo_initial = DUMMY_VOEVENT_LIGO_INITIAL
    maxi = DUMMY_VOEVENT_GCN_MAXI
    agile = DUMMY_VOEVENT_AGILE

if __name__ == "__main__":
    """
    this main test the correct working of the entire voeventhandler code.
    As imput takes a generic voevent, then it is sorted and  extracted.
    the usefull information are insert in the database, and a email notification
    is sent to the team 
    """
    dummyevents = DummyEvent()
    voe_chime = vp.loads(dummyevents.chime) #tested
    voe_gcn = vp.loads(dummyevents.gcn) #tested
    voe_integral = vp.loads(dummyevents.integral) #tested
    voe_fermi = vp.loads(dummyevents.fermi) #tested
    voe_ligo = vp.loads(dummyevents.ligo) #tested
    voe_ligo_2 = vp.loads(dummyevents.ligo2) #tested
    voe_ligo_init = vp.loads(dummyevents.ligo_initial) #tested
    voe_maxi = vp.loads(dummyevents.maxi) #tested
    voe_agile = vp.loads(dummyevents.agile) #tested

    voe_handler = VoeventHandler()
    voe_handler.handleVoevent(voe_chime)
    voe_handler.handleVoevent(voe_gcn)
    voe_handler.handleVoevent(voe_integral)
    voe_handler.handleVoevent(voe_fermi)
    voe_handler.handleVoevent(voe_ligo)
    voe_handler.handleVoevent(voe_ligo_2)
    voe_handler.handleVoevent(voe_ligo_init)
    voe_handler.handleVoevent(voe_maxi)
    voe_handler.handleVoevent(voe_agile)

