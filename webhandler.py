import requests
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
        botter_list = requests.get(self.url+"/botters.php")
        if botter_list.status_code == 200:
            self._ServerSuccess
            try: 
                return int(botter_list.text.split("\n")[0])
            except ValueError:
                return 0
        else:
            self._ServerError()


    def getClaimedList(self):
        fc_req = requests.get(self.url+"/getList.php", params={'me': self.myFC})
        if fc_req.status_code == 200:
            if not fc_req.text.startswith('error') and not fc_req.text.startswith('nothing'):
                fc_list = [x for x in fc_req.text.split("\n") if len(x)==12]
                return fc_list
            else:
                return []
        return []

    def getNewList(self):
        fc_req = requests.get(self.url+"/getfcs.php", params={'me': self.myFC, 'active': self.active, 'ver': self.ver})
        if fc_req.status_code == 200:
            self._ServerSuccess()
            if not fc_req.text.startswith('error') and not fc_req.text.startswith('nothing'):
                fc_list = [x for x in fc_req.text.split("\n") if len(x)==12]
                return fc_list
        else:    
            print("[",datetime.now(),"] WebHandler: Generic Connection error",fc_req.status_code)
            self._ServerError()
        return []

    def UpdateLFCS(self,fc,lfcs):
        lfcs_req = requests.get(self.url+"/setlfcs.php", params={'lfcs': '{:016x}'.format(lfcs),'fc':fc})
        if lfcs_req.status_code == 200:
            self._ServerSuccess()
            if not lfcs_req.text.startswith('error'):
                return True
        else:
            print("[",datetime.now(),"] WebHandler: Generic Connection error",lfcs_req.status_code)
            self._ServerError()
        return False

    def TimeoutFC(self,fc):
        timeout_req = requests.get(self.url+"/timeout.php", params={'me': self.myFC, 'fc':fc})
        if timeout_req.status_code == 200:
            self._ServerSuccess()
            if not timeout_req.text.startswith('error'):
                return True
        else:
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
            print("[",datetime.now(),"] WebHandler: Generic Connection error",timeout_req.status_code)
            self._ServerError()
        return False