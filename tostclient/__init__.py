import os
import requests


class TostClient(object):

    def __init__(self, base_domain):
        self.base_domain = base_domain
        # self.debug_log = os.environ["TOST_DEBUG"] == "1"

    def start(self, args, cmd):
        domain = self.base_domain + "/" + cmd
        response = requests.post(domain, data=args)
        status_code, response = response.status_code, response.json()

        if status_code == 400:
            raise Exception(response["msg"])

        try:
            email = response["user"]["email"]
            auth_token = response["user"]["id"]
        except:
            raise Exception("request failed")

        return {
            "msg": "successful {} for {} with id {}"
                   .format(cmd, email, auth_token),
            "data": {
                "email": email,
                "auth_token": auth_token
            }
        }

    def multiple(self, args, cmd):
        domain = self.base_domain + "/tost"
        response = requests.get(domain, auth=args["auth"])
        status_code, response = response.status_code, response.json()

        try:
            tosts = {}
            for k, v in response.iteritems():
                tosts[str(k)] = str(v)
        except:
            raise Exception("request failed")

        return {
            "msg": "successful {} request".format(cmd),
            "data": {
                "tosts": tosts
            }
        }

    def individual(self, args, cmd):
        path = "" if cmd == "create" else "/" + args["ppgn_token"]
        request_type = {
            "create": "post",
            "view": "get",
            "edit": "put"
        }

        domain = self.base_domain + "/tost" + path
        exec('response = requests.{}(domain, auth=args["auth"], data=args["data"])'
             .format(request_type[cmd]))
        status_code, response = response.status_code, response.json()

        if cmd == "create":
            if status_code == 400:
                raise Exception(response["msg"])
        if cmd in set(["view", "edit"]):
            if status_code == 404:
                raise Exception(response["msg"])
        if cmd == "edit":
            if status_code == 302:
                raise Exception(response["msg"] + " " + response["access-token"])

        try:
            tost = response["tost"]
            access_token = tost["access-token"]
        except:
            raise Exception("request failed")

        return {
            "msg": "successful {} for tost with access token {}"
                   .format(cmd, access_token),
            "data": {
                "tost": tost
            }
        }

    def permit(self, args, cmd):
        domain = self.base_domain + "/tost/" + args["ppgn_token"] \
                + "/propagation"
        response = requests.get(domain, auth=args["auth"])
        status_code, response = response.status_code, response.json()

        try:
            propagations = response["propagations"]
        except:
            raise Exception("request failed")

        return {
            "msg": "successful {} request".format(cmd),
            "data": {
                "propagations": propagations
            }
        }

    def switch(self, args, cmd):
        domain = self.base_domain + "/tost/" + args["ppgn_token"] \
                + "/propagation/" + cmd
        response = requests.post(domain, auth=args["auth"], data=args["data"])
        status_code, response = response.status_code, response.json()

        if status_code == 400:
            raise Exception(response["msg"])

        try:
            access_token = response["access-token"],
            parent_access_token = response["parent-access-token"]
        except:
            raise Exception("request failed")

        return {
            "msg": "successful {} for tost with access token {}"
                   .format(cmd, access_token[0]),
            "data": {
                "access-token": access_token[0],
                "parent-access-token": parent_access_token
            }
        }
