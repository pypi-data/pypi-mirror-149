"""
    Send email/sms/discord
"""

import json
import requests

class Apisender:
    """
        Send email/sms/discord
    """
    def __init__(self,**kwargs):
        self.fromid = kwargs.get('fromid')
        self.toid = kwargs.get('toid')
        self.subject = kwargs.get('subject')
        self.fromname = kwargs.get('fromname')
        self.toname = kwargs.get('toname')
        self.bodytext = kwargs.get('bodytext')
        self.bodyhtml = kwargs.get('bodyhtml')
        self.headerjson = {"Content-Type": "application/json; charset=utf-8"}
        self.authpasskey = None
        self.authuser = None

    def getpass(self,name):
        """
            Get username and password or key from apisender.json
        """
        try:
            with open("apisender.json","r",encoding="utf-8") as api:
                api = json.loads(api.read())
                self.authuser = api.get(name).get("authuser")
                self.authpasskey = api.get(name).get("authpasskey")
                print(self.authuser)
                print(self.authpasskey)
        except FileNotFoundError as execption:
            raise FileNotFoundError("apisender.json not found") from execption

    def discord(self):
        """
            Send discord message
        """
        self.getpass("discord")
        data = {"content":f"{self.bodytext}","username": f"{self.fromid or self.fromname}"}
        return requests.post(f"https://discordapp.com/api/webhooks/{self.authpasskey}?wait=true",\
                                data=json.dumps(data),headers=self.headerjson)

    def mailjet(self):
        """
            Send mailjet message
        """
        self.getpass("mailjet")
        data = {'Messages': [{
                "From": {"Email": self.fromid,"Name": self.fromname},
                "To": [{"Email": self.toid,"Name": self.toname}],
                "Subject": self.subject,
                "TextPart": self.bodytext,
                "HTMLPart": self.bodyhtml}]}

        return requests.post("https://api.mailjet.com/v3.1/send",json.dumps(data),\
                            headers=self.headerjson,auth=(self.authuser,self.authpasskey))

    def smtp2go(self):
        """
            Send smtp2go message
        """
        self.getpass("smtp2go")
        data = {"api_key": self.authpasskey,
                "sender": self.fromid,
                "to": [self.toid],
                "subject": self.subject,
                "text_body": self.bodytext}

        return requests.post("https://api.smtp2go.com/v3/email/send",\
                            json.dumps(data),headers=self.headerjson)
