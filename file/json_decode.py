#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
from file.service import Service

def decode(s):
  service = Service('1', '2', "default", "default")
  try:
    service.__dict__=json.loads(s)
  except:
    return None
  return service