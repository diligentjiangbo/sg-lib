# -*- coding: UTF-8 -*-

import socket #for sockets

from giraffe.RemotingCommand import RemotingCommand
from giraffe.CreateTopicRequestHeader import CreateTopicRequestHeader
from giraffe.DeleteTopicRequestHeader import DeleteTopicRequestHeader
from giraffe.SendMessageRequestHeader import SendMessageRequestHeader
from giraffe.HeartbeatRequestHeader import HeartbeatRequestHeader, HeartbeatData

#TCP请求码
SEND_MESSAGE = 10
UPDATE_AND_CREATE_TOPIC = 17
HEART_BEAT = 34
DELETE_TOPIC_IN_BROKER = 215
DELETE_TOPIC_IN_NAMESRV = 216

#创建队列的基本参数
WRITE_QUEUE_NUM = '4'
READ_QUEUE_NUM = '4'

#创建一个socket连接
def connect(ip, port):
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 10)
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

# 向broker发送心跳
def send_hearbeat(s, clientID, groupName):
  requestHeader = HeartbeatRequestHeader()
  remotingCommand = RemotingCommand(HEART_BEAT, requestHeader)
  heartbeatData = HeartbeatData(clientID, groupName)
  remotingCommand = remotingCommand.encodeHeader(bytearray(heartbeatData.encode()))
  try:
    s.sendall(remotingCommand)
  except socket.error:
    print('send hearbear failed')

# 发送一条消息
def send_message(s, groupName, topic, message, properties):
  requestHeader = SendMessageRequestHeader(groupName, topic, properties)
  remotingCommand = RemotingCommand(SEND_MESSAGE, requestHeader)
  remotingCommand = remotingCommand.encodeHeader(bytearray(message.SerializeToString()))

  try:
    s.sendall(remotingCommand)
  except socket.error:
    print('send msg failed');


if __name__ == '__main__':
  # s = connect("localhost", 6609)
  s = connect("115.159.127.98", 6609)
  #create_topic(s, "12345678");
  # send_message(s, "hello world")
  send_hearbeat(s, "123", "222")
    

