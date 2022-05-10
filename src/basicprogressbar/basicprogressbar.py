"""
    Basic progress bar with no dependencies
"""
class BasicProgressBar:
    """
        Basic progress bar with no dependencies
    """
    def __init__(self,
                current:float = 0,
                total:float = -1,
                posttext:str="",
                pretext:str="Progress:",
                length:int=60,
                endtext:str="",
                endline:str='\r'):

        self.current = current
        self.total = total
        self.posttext = posttext
        self.pretext = pretext
        self.length = length
        self.endtext = endtext
        self.endline = endline
        self.barfill = None
        self.percent = None

    def buildbar(self):
        """
            Generate Progress Bar
        """
        if self.total == -1: # endless progress bar
            if self.barfill is None or self.barfill[0] == "█":
                barchar = "░██░"
            else:
                barchar = "█░░█"
            self.barfill = barchar*int(self.length/4)
            return f"{self.pretext} {self.barfill} [{self.current}] {self.posttext}"
        else:
            self.percent=int((self.current/self.total)*100)
            barlen=int(self.percent/100*self.length)
            self.barfill = "█"*barlen+"░"*(self.length-barlen)
            if self.total == self.current: # bar is full
                self.endline = '\n' # newline at end when bar is full
                if self.endtext != "":
                    self.posttext = self.endtext+" "*(len(str(self.posttext))-len(str(self.endtext)))
                    # add space to posttext if it is shorter than endtext
            return f"{self.pretext} {self.barfill} {self.percent}% [{self.current}/{self.total}] {self.posttext}"

    def bar(self,printbar:bool=False):
        """
            Print or return Progress Bar
        """
        if printbar:
            print(self.buildbar(),end=self.endline)
        else:
            return self.buildbar()

    def next(self,printbar:bool=False):
        """
            # Increment current by 1, return when False or print progress bar when True
        """
        self.current += 1
        if printbar:
            self.bar(True)
        else:
            return self.buildbar()

class DiscordProgressBar(BasicProgressBar):
    """
        Send progress bar to discord
        depends on requests and time
    """
    def __init__(self,
                current:float = 0,
                total:float = -1,
                idtoken:str="",
                disuser:str="Progress Bar",
                throttle:float=0.5,
                messtime:float=0.0,
                messid:str=None,
                timeout:float=10.0,
                posttext:str="",
                pretext:str="Progress:",
                length:int=60,
                endtext:str="",): # Not using **kwargs to make input easier

        super().__init__(current = current,
                        total = total,
                        posttext = posttext,
                        pretext = pretext,
                        length = length,
                        endtext = endtext)

        self.idtoken = idtoken
        self.disuser = disuser
        self.throttle = throttle
        self.messtime = messtime
        self.messid = messid
        self.timeout = timeout

    def next(self):
        '''
            Increment current by 1, and sends bar to discord
        '''
        self.current += 1
        self.send()

    def send(self):
        '''
            Posts bar to discord or updates current bar
            Only using built in dependencies
        '''
        # importing here to avoid if only using basic progress bar
        import time
        import json

        class UrlRequest:
            """
                Putting urllib.request in a class to make it easier to use
            """
            def __init__(self, url:str,
                        data:str="",
                        method:str='GET',
                        headers:str="",
                        timeout:int = 10,
                        username=None,
                        password=None):

                # imporing here to keep it all contained
                import urllib.request
                import urllib.error

                if username and password: # Basic Auth
                    auth = urllib.request.HTTPPasswordMgrWithDefaultRealm()
                    auth.add_password(None, url, username, password)
                    opener = urllib.request.build_opener(urllib.request.HTTPBasicAuthHandler(auth))
                    urllib.request.install_opener(opener)
                req = urllib.request.Request(url,data=data.encode('utf-8'),method=method,headers=headers)
                try:
                    with urllib.request.urlopen(req, timeout=timeout) as request:
                        self.text = request.read().decode('utf-8')
                        self.status = request.status
                        self.headers = request.headers
                except urllib.error.HTTPError as exception:
                    self.text = exception.reason
                    self.status = exception.code
                    self.headers = exception.headers
                except urllib.error.URLError as exception:
                    self.text = exception.reason
                    self.status = 400
                    self.headers = ""

        if self.messtime+self.throttle <= time.time() or self.current == self.total:
            webhook = "https://discord.com/api/webhooks/"+self.idtoken
            webheader = {"Content-Type": "application/json, charset=utf-8",
                        'User-Agent': 'Python Basic Progress Bar'}
            data = {"content":f"{self.bar()}","username": f"{self.disuser}"}
            if self.messid is None:
                resp = UrlRequest(webhook+"?wait=true",data=json.dumps(data),headers=webheader,method="POST")
                if resp.status == 200:
                    self.messid = json.loads(resp.text).get('id')
                else:
                    print(f'[{resp.status}] {resp.text}')
                    self.messid = None # Failed to send message returns None to try again
            else:
                resp = UrlRequest(webhook+"/messages/"+self.messid,data=json.dumps(data),headers=webheader,method="PATCH")
                if resp.status != 200:
                    print(f'[{resp.status}] {resp.text}')

            self.messtime = time.time()
        return self.messid,self.messtime
