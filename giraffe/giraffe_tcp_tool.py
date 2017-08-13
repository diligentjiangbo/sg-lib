#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import imp
import sys
import socket #for sockets

from giraffe.RemotingCommand import RemotingCommand
from giraffe.CreateTopicRequestHeader import CreateTopicRequestHeader
from giraffe.DeleteTopicRequestHeader import DeleteTopicRequestHeader

#字符串编码统一为utf8
imp.reload(sys)

#TCP请求码
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
  remotingCommand = RemotingCommand(UPDATE_AND_CREATE_TOPIC, {})
  remotingCommand.putKeyValue('defaultTopic', requestHeader.defaultTopic)
  remotingCommand.putKeyValue('perm', requestHeader.perm)
  remotingCommand.putKeyValue('topicFilterType', requestHeader.topicFilterType)
  remotingCommand.putKeyValue('topicSysFlag', requestHeader.topicSysFlag)
  remotingCommand.putKeyValue('order', requestHeader.order)
  remotingCommand.putKeyValue('topic', requestHeader.topic)
  remotingCommand.putKeyValue('readQueueNums', requestHeader.readQueueNums)
  remotingCommand.putKeyValue('writeQueueNums', requestHeader.writeQueueNums)

  try:
    s.sendall(remotingCommand.encodeHeader())
  except socket.error:
    print('topic=' + topic + 'create failed') 

#从broker删除topic
def delete_broker_topic(s, topic):
  requestHeader = DeleteTopicRequestHeader(topic)
  remotingCommand = RemotingCommand(DELETE_TOPIC_IN_BROKER, {})
  remotingCommand.putKeyValue('topic', requestHeader.topic)
  
  try:
    s.sendall(remotingCommand.encodeHeader())
  except socket.error:
    print('delete topic=' + topic + " from broker failed")
  
#从namesrv删除topic
def delete_namesrv_topic(s, topic):
  requestHeader = DeleteTopicRequestHeader(topic)
  remotingCommand = RemotingCommand(DELETE_TOPIC_IN_NAMESRV, {})
  remotingCommand.putKeyValue('topic', requestHeader.topic)
  
  try:
    s.sendall(remotingCommand.encodeHeader())
  except socket.error:
    print('delete topic=' + topic + " from namrsrv failed")
    

