import os
import json
import pytest
import voeventparse as vp
from voeventhandler.extractors.ligodataextractor import LigoDataExtractor
from voeventhandler.emailnotifier import EmailNotifier

class TestEmailNotifier:

    def writeConfig(enabled, packet_with_email_notification, skip_ligo_not_significant, skip_ligo_test, skip_ste, sender_email, sender_email_password, email_receivers, developer_email_receivers):
        config = {
            "enabled": enabled,
            "packet_with_email_notification": packet_with_email_notification,
            "skip_ligo_not_significant": skip_ligo_not_significant,
            "skip_ligo_test": skip_ligo_test,
            "skip_ste": skip_ste,
            "sender_email": sender_email,
            "sender_email_password": sender_email_password,
            "email_receivers" : email_receivers,
            "developer_email_receivers" : developer_email_receivers
        }
        with open("/tmp/config.json", "w") as f:
            json.dump(config, f)
        return "/tmp/config.json"

    @pytest.mark.skip
    @pytest.mark.parametrize("notice_str", ["ligo_initial.xml"], indirect=True)
    def test_real_send(self, notice_str):
        sender_email = ""
        sender_email_password = ""
        email_receivers = [""]
        configFile = TestEmailNotifier.writeConfig(True, [150, 151, 152], True, False, False, sender_email, sender_email_password, email_receivers, [])
        voe = LigoDataExtractor().extract(vp.loads(notice_str))
        correlations = [{"instrument_name" : "FERMI"}]
        emailMessages = EmailNotifier(configFile).sendEmails(voe, correlations)
        print(emailMessages[0].as_string())
        assert 1 == len(emailMessages)
        os.remove(configFile)


    #  "ligo_preliminary.xml"
    @pytest.mark.parametrize("notice_str", ["ligo_initial.xml"], indirect=True)
    def test_send_email(self, notice_str):
        
        # significant events, skip not-significant = True
        configFile = TestEmailNotifier.writeConfig(False, [150, 151, 152], True, False, False, "", "", [], [])
        voe = LigoDataExtractor().extract(vp.loads(notice_str))
        correlations = []
        sent, emailMessage = EmailNotifier(configFile).sendEmails(voe, correlations)
        assert not sent
        assert emailMessage

        # significant events, skip not-significant = False
        configFile = TestEmailNotifier.writeConfig(False, [150, 151, 152], False, False, False, "", "", [], [])
        voe = LigoDataExtractor().extract(vp.loads(notice_str))
        correlations = []
        sent, emailMessage = EmailNotifier(configFile).sendEmails(voe, correlations)
        assert not sent
        assert emailMessage

        # not-significant events, skip not-significant = True
        configFile = TestEmailNotifier.writeConfig(False, [150, 151, 152], True, False, False, "", "", [], [])
        voe = LigoDataExtractor().extract(vp.loads(notice_str))
        voe.ligo_attributes["significant"] = 0
        correlations = []
        sent, emailMessage = EmailNotifier(configFile).sendEmails(voe, correlations)
        assert not sent
        assert not emailMessage

        # not-significant events, skip not-significant = False
        configFile = TestEmailNotifier.writeConfig(False, [150, 151, 152], False, False, False, "", "", [], [])
        voe = LigoDataExtractor().extract(vp.loads(notice_str))
        voe.ligo_attributes["significant"] = 0
        correlations = []
        sent, emailMessage = EmailNotifier(configFile).sendEmails(voe, correlations)
        assert not sent
        assert emailMessage        

        # set ste, skip ste = True
        configFile = TestEmailNotifier.writeConfig(False, [150, 151, 152], True, False, True, "", "", [], [])
        voe = LigoDataExtractor().extract(vp.loads(notice_str))
        voe.is_ste = 1
        correlations = []
        sent, emailMessage = EmailNotifier(configFile).sendEmails(voe, correlations)
        assert not sent
        assert not emailMessage

        # skip ligo test = True
        configFile = TestEmailNotifier.writeConfig(False, [150, 151, 152], False, True, False, "", "", [], [])
        voe = LigoDataExtractor().extract(vp.loads(notice_str))
        voe.is_ste = 1
        correlations = []
        sent, emailMessage = EmailNotifier(configFile).sendEmails(voe, correlations)
        assert not sent
        assert not emailMessage

        # packet type not supported
        configFile = TestEmailNotifier.writeConfig(False, [99], False, False, False, "", "", [], [])
        voe = LigoDataExtractor().extract(vp.loads(notice_str))
        voe.is_ste = 1
        correlations = []
        sent, emailMessage = EmailNotifier(configFile).sendEmails(voe, correlations)
        assert not sent
        assert not emailMessage

        # correlations
        configFile = TestEmailNotifier.writeConfig(False, [150, 151, 152], True, False, False, "", "", [], [])
        voe = LigoDataExtractor().extract(vp.loads(notice_str))
        correlations = [{"instrument_name" : "FERMI"}]
        sent, emailMessage = EmailNotifier(configFile).sendEmails(voe, correlations)
        print(emailMessage.as_string())
        assert not sent
        assert emailMessage