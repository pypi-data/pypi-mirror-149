# -*- coding: utf-8 -*-
# Copyright (C) 2021 Tobias Weber <tobi-weber@gmx.de>

from foliolib.config import Config
from foliolib.okapi.okapiClient import OkapiClient


def get_node():
    try:
        nodes = OkapiClient().get_nodes()
    except:
        nodes = []
    try:
        host = Config().okapicfg().get("Okapi", "host")
    except:
        host = "localhost"
    try:
        port = Config().okapicfg().get("Okapi", "port")
    except:
        port = "9130"
    for node in nodes:
        if "nodeName" in node:
            if f"{host}:{port}" in node["url"]:
                return node["nodeName"]

    return host


def get_mod_name_from_id(s):
    """
    \d+         : one or more digits
    \.           : one point
    (\.\d+)+ : one or more occurences of point-digits

    If you want to exclude decimal numbers like 2.5 and expect a version number to have at least 3 parts, you can use a quantifier like this

\d+(\.\d+){2,}


By version number, do you mean any sequence of digits interspersed with dots?

\d+(\.\d+)+
    """
