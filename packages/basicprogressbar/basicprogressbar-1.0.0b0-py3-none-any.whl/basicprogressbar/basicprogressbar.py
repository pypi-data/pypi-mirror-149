"""
    Basic progress bar with no dependencies*
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
            if self.barfill == None or self.barfill[0] == "█":
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
            Increment current by 1, return or print progress bar
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
                messid:str="",
                timeout:float=10.0,
                **kwargs):

        super().__init__(current,total,**kwargs)

        self.idtoken = idtoken
        self.disuser = disuser
        self.throttle = throttle
        self.messtime = messtime
        self.messid = messid
        self.timeout = timeout
    
    def next(self):
        self.current += 1
        self.send()

    def send(self):
        import requests
        import time
        if self.messtime+self.throttle <= time.time() or self.current == self.total:
            webhook = "https://discord.com/api/webhooks/"+self.idtoken
            data= {"content":f"{self.bar()}","username": f"{self.disuser}"}
            if self.messid == "":
                try:
                    resp = requests.post(webhook+"?wait=true",json=data,timeout=self.timeout)
                    if resp.status_code == 200:
                        self.messid = resp.json()['id']
                except:
                    self.messid = "" # Failed to send message returns blank to try again
            else:
                try:
                    resp = requests.patch(webhook+"/messages/"+self.messid,json=data,timeout=self.timeout)
                except:
                    pass
            self.messtime = time.time()
        return self.messid,self.messtime
