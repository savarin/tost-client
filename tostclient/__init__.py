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
            "msg": "successful {} for {} with id {}"\
                   .format(cmd, email, auth_token),
            "data": {
                "email": email,
                "auth_token": auth_token
            }
        }
