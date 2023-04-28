from voeventhandler.extractors.templatedataextractor import TemplateDataExtractor
from voeventhandler.utilis.instrumentid import InstrumentId
from voeventhandler.utilis.voeventdata import Voeventdata
from ligo.skymap.postprocess.contour import contour as ligo_contour
from ligo.skymap.io.fits import read_sky_map
from astropy.coordinates import SkyCoord
from astropy import units as u
from datetime import datetime
import voeventparse as vp
import numpy as np
import requests
import json
import re
import os


class LigoDataExtractor(TemplateDataExtractor):
    """
    This class is an implementation of the TemplateDataExtractor class.
    It implements the method that are specific for the Ligo data source.
    """
    def __init__(self) -> None:
        super().__init__("ligo")

    def extract(self, voevent) -> Voeventdata:
        return super().extract(voevent)

    def is_ste(self, voevent):
        top_params = vp.get_toplevel_params(voevent)
        significant = bool(int(top_params["Significant"]["value"]))
        return not significant
 
    def is_test(self, voevent):
        if "test" in voevent.attrib['role']:
            return True
        return False
    
    def get_instrumentID_and_name(self, voevent) -> tuple:
        packet_type = int(voevent.What.Param[0].attrib["value"])
        if packet_type in [150, 151, 152]: # Preliminary, Initial, Update https://emfollow.docs.ligo.org/userguide/content.html
            if  "test" in voevent.attrib['role']:
                return InstrumentId.LIGO_TEST.value, "LIGO_TEST"
            if  "observation" in voevent.attrib['role']:
                return InstrumentId.LIGO.value, "LIGO"
        else:
            raise Exception(f"Voevent with packet type {packet_type} not supported")

    def get_triggerID(self, voevent):
        top_params = vp.get_toplevel_params(voevent)
        graceID = top_params["GraceID"]["value"]
        last = str(ord(graceID[-1]) - 96)
        result = re.sub("[^0-9]", "", graceID) + last.zfill(2)
        return result

    def get_packet_type(self, voevent):
        top_params = vp.get_toplevel_params(voevent)
        return top_params["Packet_Type"]["value"]

    def get_networkID(self, voevent):
        return 1

    def get_l_b(self, voevent):
        return 0,0

    def get_position_error(self, voevent):
        return 0

    def get_configuration(self, voevent):
        top_params = vp.get_toplevel_params(voevent)
        return top_params["Instruments"]["value"]

    def get_ligo_attributes(self, voevent):
        top_params = vp.get_toplevel_params(voevent)
        grouped_params = vp.get_grouped_params(voevent)
        attributes = {}
        attributes["bbh"] = float(grouped_params["Classification"]["BBH"]["value"])
        attributes["bns"] = float(grouped_params["Classification"]["BNS"]["value"]) #special mail soglia configurabile
        attributes["far"] = float(top_params["FAR"]["value"])
        attributes["nsbh"] = float(grouped_params["Classification"]["NSBH"]["value"]) #special mail soglia configurabile
        attributes["has_ns"] = grouped_params["Properties"]["HasNS"]["value"] 
        attributes["grace_id"] = top_params["GraceID"]["value"]
        attributes["has_remnant"] = grouped_params["Properties"]["HasRemnant"]["value"]
        attributes["has_mass_gap"] = grouped_params["Properties"]["HasMassGap"]["value"]
        attributes["terrestrial"] = grouped_params["Classification"]["Terrestrial"]["value"]

        attributes["significant"] = int(top_params["Significant"]["value"])
        attributes["event_page"] = top_params["EventPage"]["value"]

        return attributes

    def get_contour(self, l, b, position, url):
        """
        For LIGO instrument we call contour function from ligo-contour tool
        """
        now = datetime.now().strftime("%Y-%m-%d:%H:%M:%S")
        target_path = f'/tmp/skymap_{now}.tar.gz'

        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(target_path, 'wb') as f:
                f.write(response.raw.read())

            #Implementing the code from ligo-countour tool, the level [90] is hardcoded

        m, meta = read_sky_map(target_path, nest=True)
        i = np.flipud(np.argsort(m))
        cumsum = np.cumsum(m[i])
        cls = np.empty_like(m)
        cls[i] = cumsum * 100
            

        cont = list(ligo_contour(cls, [90.0], nest=True, degrees=True, simplify=False))
            
        #Conversion to galactic: it computes the position without loops to be more efficient, it uses approx 3 GB RAM
        ra = []
        dec = []
        for level in cont:
            for poligon in level:
                for coord in poligon:
                    ra.append(coord[0])
                    dec.append(coord[1])
            
        c = SkyCoord(ra=ra*u.degree, dec=dec*u.degree)
        contour = ""
        for coords in c.galactic.to_string():
            contour = contour + f"{coords}\n"

        os.remove(target_path)
        return contour

    def get_url(self, voevent):
        grouped_params = vp.get_grouped_params(voevent)
        return  grouped_params["GW_SKYMAP"]["skymap_fits"]["value"]


