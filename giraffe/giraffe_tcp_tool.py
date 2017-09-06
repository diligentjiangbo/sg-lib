#!/usr/bin/python
# -*- coding: UTF-8 -*-

import imp
import sys
import socket #for sockets

from giraffe.RemotingCommand import RemotingCommand
from giraffe.CreateTopicRequestHeader import CreateTopicRequestHeader
from giraffe.DeleteTopicRequestHeader import DeleteTopicRequestHeader
from giraffe.SendMessageRequestHeader import SendMessageRequestHeader

# protobuf
import dmb_pb2

#字符串编码统一为utf8
imp.reload(sys)

#TCP请求码
SEND_MESSAGE = 10
UPDATE_AND_CREATE_TOPIC = 17
DELETE_TOPIC_IN_BROKER = 215
DELETE_TOPIC_IN_NAMESRV = 216

#创建队列的基本参数
WRITE_QUEUE_NUM = '4'
READ_QUEUE_NUM = '4'

#创建一个socket连接
def connect(ip, port):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((ip, port))
  return s
  
#关闭一个socket连接
def close(s):
  s.close()
  
#创建一个topic
def create_topic(s, topic):
  requestHeader = CreateTopicRequestHeader(topic, READ_QUEUE_NUM, WRITE_QUEUE_NUM)
  remotingCommand = RemotingCommand(UPDATE_AND_CREATE_TOPIC, requestHeader)

  try:
    s.sendall(remotingCommand.encodeHeader())
  except socket.error:
    print('topic=' + topic + 'create failed') 

#从broker删除topic
def delete_broker_topic(s, topic):
  requestHeader = DeleteTopicRequestHeader(topic)
  remotingCommand = RemotingCommand(DELETE_TOPIC_IN_BROKER, requestHeader)
  
  try:
    s.sendall(remotingCommand.encodeHeader())
  except socket.error:
    print('delete topic=' + topic + " from broker failed")
  
#从namesrv删除topic
def delete_namesrv_topic(s, topic):
  requestHeader = DeleteTopicRequestHeader(topic)
  remotingCommand = RemotingCommand(DELETE_TOPIC_IN_NAMESRV, requestHeader)
  
  try:
    s.sendall(remotingCommand.encodeHeader())
  except socket.error:
    print('delete topic=' + topic + " from namrsrv failed")

# 发送一条消息
def send_message(s, msg):
  requestHeader = SendMessageRequestHeader("20101", "EC0-6012019999-01", {})
  remotingCommand = RemotingCommand(SEND_MESSAGE, requestHeader)

  message = dmb_pb2.Message()
  sysHeader = dmb_pb2.SystemHeader()
  sysHeader.serviceId = '6012019999'
  sysHeader.sceneId = '01'
  message.sysHead.CopyFrom(sysHeader)
  message.appHead.CopyFrom(dmb_pb2.AppHeader())
  message.body = msg
  # send_msg = remotingCommand.encodeHeader(bytearray("hello world", "utf8"))
  send_msg = remotingCommand.encodeHeader(bytearray(message.SerializeToString()))

  try:
    s.sendall(send_msg)
  except socket.error:
    print('send msg');


if __name__ == '__main__':
  # s = connect("localhost", 6609)
  s = connect("115.159.127.98", 6609)
  #create_topic(s, "12345678");
  send_message(s, "hello world")
    

