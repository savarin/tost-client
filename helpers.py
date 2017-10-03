import re
from itertools import izip


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
