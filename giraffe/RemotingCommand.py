#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json

class RemotingCommand:
  
  def __init__(self, code, extFields,\
    flag=0, language='PYTHON', opaque=0, serializeTypeCurrentRPC='JSON', version=1):
    self.code = code
    self.extFields = extFields
    self.flag = flag
    self.language = language
    self.opaque = opaque
    self.serializeTypeCurrentRPC = serializeTypeCurrentRPC
    self.version = version
  
  def headerEncode(self):
    return json.dumps(self.__dict__)

  def encodeHeader(self):
    length = 4
    headerData = self.headerEncode()
    headerLength = len(headerData)
    length += headerLength
    byteBuffer = bytearray(4 + length)
    #写入4字节的整个消息length
    byteBuffer[0] = (length >> 24) & 0xFF
    byteBuffer[1] = (length >> 16) & 0xFF
    byteBuffer[2] = (length >> 8) & 0xFF
    byteBuffer[3] = length & 0xFF
    #第5字节是序列化的方式，json是0，第6-8字节是header的length
    byteBuffer[4] = 0 & 0xFF
    byteBuffer[5] = (headerLength >> 16) & 0xFF
    byteBuffer[6] = (headerLength >> 8) & 0xFF
    byteBuffer[7] = headerLength & 0xFF
    dataBuffer = bytearray(headerData, 'utf8')
    for i in range(len(dataBuffer)):
      byteBuffer[i+8] = dataBuffer[i]
    return byteBuffer

  def putKeyValue(self, key, value):
    self.extFields.setdefault(key, value)

if __name__ == '__main__':
  command = RemotingCommand(17, {'hello':'world'})
  s = command.encodeHeader()
  for b in s:
    print(b)
