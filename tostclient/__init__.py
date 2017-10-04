import os
import re
import requests
import sys
from itertools import izip


class TostClient(object):

    def __init__(self, base_url, debug_log=False):
        self.base_url = base_url
        self.debug_log = debug_log

    def start(self, args, cmd):
        url = self.base_url + "/" + cmd

        if self.debug_log:
            sys.stderr.write("POST {} {}\n".format(str(url), str(args)))

        response = requests.post(url, data=args)
        status_code, response = response.status_code, response.json()

        if self.debug_log:
            sys.stderr.write("{} {}\n".format(str(status_code), str(response)))

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
        url = self.base_url + "/tost"

        if self.debug_log:
            sys.stderr.write("GET {} {}\n".format(str(url), str(args)))

        response = requests.get(url, headers=args["headers"])
        status_code, response = response.status_code, decode_response(response)

        if self.debug_log:
            sys.stderr.write("{} {}\n".format(str(status_code), str(response)))

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

        url = self.base_url + "/tost" + path

        if self.debug_log:
            sys.stderr.write("{} {} {}\n".format(str(request_type[cmd]).upper(),
                                                 str(url), str(args)))

        exec('response = requests.{}(url, headers=args["headers"], data=args["data"])'
             .format(request_type[cmd]))
        status_code, response = response.status_code, decode_response(response)

        if self.debug_log:
            sys.stderr.write("{} {}\n".format(str(status_code), str(response)))

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
        url = self.base_url + "/tost/" + args["ppgn_token"] \
                + "/propagation"

        if self.debug_log:
            sys.stderr.write("GET {} {}\n".format(str(url), str(args)))

        response = requests.get(url, headers=args["headers"])
        status_code, response = response.status_code, decode_response(response)

        if self.debug_log:
            sys.stderr.write("{} {}\n".format(str(status_code), str(response)))

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
        url = self.base_url + "/tost/" + args["ppgn_token"] \
                + "/propagation/" + cmd

        if self.debug_log:
            sys.stderr.write("POST {} {}\n".format(str(url), str(args)))

        response = requests.post(url, headers=args["headers"], data=args["data"])
        status_code, response = response.status_code, decode_response(response)

        if self.debug_log:
            sys.stderr.write("{} {}\n".format(str(status_code), str(response)))

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


def decode_bencode(string):

    def decode(string):
        digits = [str(item) for item in xrange(10)]

        if string == "":
            return None, ""

        elif string.startswith("i"):
            match = re.match("i(-?\d+)e", string)
            return int(match.group(1)), string[match.span()[1]:]

        elif any([string.startswith(item) for item in digits]):
            match = re.match("(\d+):", string)
            start = match.span()[1]
            end = start + int(match.group(1))
            return string[start:end], string[end:]

        elif string.startswith("l") or string.startswith("d"):
            elements = []
            rest = string[1:]
            while not rest.startswith("e"):
                element, rest = decode(rest)
                elements.append(element)
            rest = rest[1:]
            if string.startswith("l"):
                return elements, rest
            else:
                return {k: v for k, v in izip(elements[::2], elements[1::2])}, rest

        else:
            raise ValueError("Malformed string.")

    return decode(string)[0]


def decode_response(response):
    return decode_bencode(response.json()["content"])
