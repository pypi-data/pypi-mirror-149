import os
import random
import ipaddress
import validators as val

"""
To obtain available ports
"""


def network_ip():
    command = "hostname -I"
    retvalue = os.popen(command).readlines()
    return str(retvalue[0][0:-1]).strip()

def isIp(value):
    try:
        ipaddress.ip_address(value)
        return True
    except:
        return False

def isURL(value):
    return val.url(value)

def validURL(value):
    http_value="http://%s" %value
    https_value="http://%s" %value
    if isIp(value):
        return True
    elif isURL(value):
        return True
    elif isURL(http_value):
        return True
    elif isURL(https_value):
        return True
    else:
        return False
