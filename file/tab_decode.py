#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re

from file.service import Service

def decode(s):
  ss = re.split(r"\s+", s)
  if len(ss) < 3:
    return None
  service = Service(ss[0], ss[1], ss[2])
  return service