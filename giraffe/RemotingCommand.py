#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
from giraffe.SendMessageRequestHeader import SendMessageRequestHeader

class RemotingCommand:
  
  def __init__(self, code, customHeader, flag=0, language='PYTHON', opaque=0, serializeTypeCurrentRPC='JSON', version=1):
    # default value
    self.flag = flag
    self.language = language
    self.opaque = opaque
    self.serializeTypeCurrentRPC = serializeTypeCurrentRPC
    self.version = version

    #special value
    self.code = code
    self.extFields = customHeader.makeCustomHeaderToNet()
  
  def headerEncode(self):
    return json.dumps(self.__dict__)

  def encodeHeader(self, body=''):
    length = 4
    headerData = self.headerEncode()
    headerLength = len(headerData)
    length += headerLength
    # 判断是否含有消息体
    if body:
      length = length + len(body)
    print "headerLength:" + str(headerLength)
    print "length:" + str(length)
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
    # byteBuffer的index
    byte_index = 8
    for i in range(len(dataBuffer)):
      byteBuffer[byte_index] = dataBuffer[i]
      byte_index = byte_index + 1
    # 将消息体放入报文
    if body:
      for i in range(len(body)):
        byteBuffer[byte_index] = body[i]
        byte_index = byte_index + 1
    return byteBuffer

if __name__ == '__main__':
  requestHeader = SendMessageRequestHeader("20101", "test", {})
  remotingCommand = RemotingCommand(10, requestHeader)
  s = remotingCommand.encodeHeader("hello world")
  # for b in s:
  #   print(b)
