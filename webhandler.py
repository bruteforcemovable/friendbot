import requests
import logging
from datetime import datetime, timedelta

class WebsiteHandler():
    def __init__(self,url,fc,active,ver):
        self.url = url
        self.myFC = fc
        self.active = active
        self.ver = ver
        self.ErrorCount = 0

    def IsConnected(self):
        return self.ErrorCount == 0

    def SetActive(self,active):
        self.active = active
    def _ServerError(self):
        self.ErrorCount += 1
    def _ServerSuccess(self):
        self.ErrorCount=0

    def BottersOnlineCount(self):
        try:
            botter_list = requests.get(self.url+"/botters.php")
            if botter_list.status_code == 200:
                self._ServerSuccess
                try: 
                    return int(botter_list.text.split("\n")[0])
                except ValueError:
                    return 0
            else:
                logging.warning("Server responded with HTTP code %s",botter_list.status_code)
        except Exception as e:
            logging.error("Exception found: %s\n%s\n%s\n%s",e,sys.exc_info()[0].__name__, sys.exc_info()[2].tb_frame.f_code.co_filename, sys.exc_info()[2].tb_lineno)
        self._ServerError()
        return 0


    def getClaimedList(self):
        try:
            fc_req = requests.get(self.url+"/getList.php", params={'me': self.myFC})
            if fc_req.status_code == 200:
                if not fc_req.text.startswith('error') and not fc_req.text.startswith('nothing'):
                    fc_list = [x for x in fc_req.text.split("\n") if len(x)==12]
                    return fc_list
                else:
                    return []
            else:
                logging.warning("Server responded with HTTP code %s",fc_req.status_code)
        except:
            self._ServerError()
        return []

    def getNewList(self):
        try:
            fc_req = requests.get(self.url+"/getfcs.php", params={'me': self.myFC, 'active': self.active, 'ver': self.ver})
            if fc_req.status_code == 200:
                self._ServerSuccess()
                if not fc_req.text.startswith('error') and not fc_req.text.startswith('nothing'):
                    fc_list = [x for x in fc_req.text.split("\n") if len(x)==12]
                    return fc_list
            else:    
                logging.warning("Server responded with HTTP code %s",fc_req.status_code)
                print("[",datetime.now(),"] WebHandler: Generic Connection error",fc_req.status_code)
                self._ServerError()
        except:
            self._ServerError()
        return []

    def UpdateLFCS(self,fc,lfcs):
        try:
            lfcs_req = requests.get(self.url+"/setlfcs.php", params={'lfcs': '{:016x}'.format(lfcs),'fc':fc})
            if lfcs_req.status_code == 200:
                self._ServerSuccess()
                if not lfcs_req.text.startswith('error'):
                    return True
            else:
                logging.warning("Server responded with HTTP code %s",lfcs_req.status_code)
                logging.warning("Server response: %s",lfcs_req.text)
                print("[",datetime.now(),"] WebHandler: Generic Connection error",lfcs_req.status_code)
                print("[",datetime.now(),"] Server response:",lfcs_req.text)
                self._ServerError()
        except Exception as e:
            print("[",datetime.now(),"] Got exception!!", e,"\n",sys.exc_info()[0].__name__, sys.exc_info()[2].tb_frame.f_code.co_filename, sys.exc_info()[2].tb_lineno)
            logging.error("Exception found: %s\n%s\n%s\n%s",e,sys.exc_info()[0].__name__, sys.exc_info()[2].tb_frame.f_code.co_filename, sys.exc_info()[2].tb_lineno)
            self._ServerError()
        return False

    def TimeoutFC(self,fc):
        timeout_req = requests.get(self.url+"/timeout.php", params={'me': self.myFC, 'fc':fc})
        if timeout_req.status_code == 200:
            self._ServerSuccess()
            if not timeout_req.text.startswith('error'):
                return True
        else:
            logging.warning("Server responded with HTTP code %s",timeout_req.status_code)
            print("[",datetime.now(),"] WebHandler: Generic Connection error",timeout_req.status_code)
            self._ServerError()
        return False
    
    def ClaimFC(self,fc):
        resp = requests.get(self.url+"/claimfc.php",params={'fc':fc,'me':self.myFC})
        if resp.status_code == 200:
            self._ServerSuccess()
            if resp.text.startswith('success'):
                return True
        else:
            logging.warning("Server responded with HTTP code %s",resp.status_code)
            print("[",datetime.now(),"] Generic Connection issue:",resp.status_code)
            self._ServerError()
        return False
    def ResetFC(self, fc):
        reset_req = requests.get(self.url+"/trustedreset.php", params={'me': self.myFC, 'fc':fc})
        if reset_req.status_code == 200:
            self._ServerSuccess()
            if not reset_req.text.startswith('error'):
                return True
        else:
            logging.warning("Server responded with HTTP code %s",reset_req.status_code)
            print("[",datetime.now(),"] WebHandler: Generic Connection error",reset_req.status_code)
            self._ServerError()
        return False
    def GetBotSettings(self):
        try:
            run=True
            toggle=False
            settings_req = requests.get(self.url+"/botSettings.php", params={'me': self.myFC, 'active': self.active, 'ver': self.ver})
            if settings_req.status_code == 200:
                self._ServerSuccess()
                if not settings_req.text.startswith('error'):
                    for x in settings_req.text.split("\n"):
                        if x.startswith("toggleactive="):
                            if x.endswith("1"):
                                logging.debug("ToggleActive = %s",1)
                                toggle=True
                            else:
                                logging.debug("ToggleActive = %s",0)
                                toggle=False
                        if x.startswith("run="):
                            if x.endswith("0"):
                                logging.debug("Run = %s",0)
                                run=False
                            else:
                                logging.debug("Run = %s",1)
                                run=True
            else:    
                logging.warning("Server responded with HTTP code %s",settings_req.status_code)
                print("[",datetime.now(),"] WebHandler: Generic Connection error",settings_req.status_code)
                self._ServerError()
        except:
            self._ServerError()
        return toggle,run
    def ResetBotSettings(self):
        try:
            settings_req = requests.get(self.url+"/botSettings.php", params={'me': self.myFC, 'active': self.active, 'ver': self.ver, 'run': '1', 'toggle':'0'})
            if settings_req.status_code == 200:
                self._ServerSuccess()
            else:    
                logging.warning("Server responded with HTTP code %s",settings_req.status_code)
                print("[",datetime.now(),"] WebHandler: Generic Connection error",settings_req.status_code)
                self._ServerError()
        except:
            self._ServerError()
        return True
