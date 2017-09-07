# -*- coding: UTF-8 -*-

import json

class HeartbeatRequestHeader:

  def __init__(self):
    # flag = 0 代表不压缩, 1代表压缩
    self.flag = 0

  def makeCustomHeaderToNet(self):
    return vars(self)

class HeartbeatData:
  def __init__(self, clientID, groupName):
    self.clientID = clientID
    self.producerDataSet = [{'groupName':groupName}]
    self.consumerDataSet = []

  def encode(self):
    return json.dumps(self.__dict__)