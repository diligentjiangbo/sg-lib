# -*- coding: UTF-8 -*-

import json
import select

# protobuf
import dmb_pb2
# 各种全局变量
import MixAll
import giraffe_tcp_tool

# 发消息方法
def sendRequest(brokerIp, brokerPort, serviceId, sceneId, topic, msg):
  # protobuf里的序列化对象
  message = dmb_pb2.Message()
  sysHead = dmb_pb2.SystemHeader()
  appHead = dmb_pb2.AppHeader()
  # 为sysHead填充值
  sysHead.serviceId = serviceId
  sysHead.sceneId = sceneId
  sysHead.targetAddress = topic
  sysHead.messageId = MixAll.generateMsgId()
  clientID = MixAll.generateMsgId()
  sysHead.customInfo = clientID
  # copy from
  message.sysHead.CopyFrom(sysHead)
  message.appHead.CopyFrom(appHead)
  message.body = msg
  # 建立到broker的socket连接
  s = giraffe_tcp_tool.connect(brokerIp, brokerPort)

  # 送心跳到broker，以便回包
  groupName = "10101"
  giraffe_tcp_tool.send_hearbeat(s, clientID, groupName)
  # send msg
  giraffe_tcp_tool.send_message(s, groupName, topic, message, {})
  print("send msg:" + msg)

  # 处理回包，10s超时
  s.setblocking(0)
  ret_msg = ''
  while True:
    ready = select.select([s], [], [], 10)
    if ready[0]:
      reply = s.recv(4096)
      ret_msg = processResponse(reply)
      if ret_msg:
        break
    else:
      print("同步请求异常")
      break

  if ret_msg:
    print("recv msg:" + ret_msg)

# 根据协议读取回包内容
def processResponse(reply):
  ret_bytes = bytearray(reply)

  # 前4个字节是整个报文长度
  all_length = getAllLength(ret_bytes[:4])
  # print("all_length:" + str(all_length))

  # 第5-8个字节包含报文头部长度
  header_length = getHeaderLength(ret_bytes[4:8])
  # print("header_length:" + str(header_length))

  # 获取头部内容
  header_body = str(ret_bytes[8:8+header_length])
  # print("header_body:" + header_body)
  header_dict = json.loads(header_body)
  header_code = header_dict['code']
  # print("header_dict:" + str(header_dict['code']))

  # 真正消息内容
  real_body = ''
  if all_length > header_length + 4:
    real_body_bytes = ret_bytes[8+header_length:len(ret_bytes)]
    # print("real_body_length:" + str(len(real_body_bytes)))
    real_body = str(real_body_bytes)
    #print("real_body:" + real_body)

  # protobuf解析消息内容
  if real_body:
    message = dmb_pb2.Message()
    message.ParseFromString(real_body)
    # print("body content:" + message.body)
    if header_code == 603:
      return message.body

# 获取头部长度
def getHeaderLength(arr):
  length = 0
  length = length | ((arr[1] & 0xFF) << 16)
  length = length | ((arr[2] & 0xFF) << 8)
  length = length | (arr[3] & 0xFF)
  return length

# 获取整个报文长度
def getAllLength(arr):
  length = 0
  length = length | ((arr[0] & 0xFF) << 24)
  length = length | ((arr[1] & 0xFF) << 16)
  length = length | ((arr[2] & 0xFF) << 8)
  length = length | (arr[3] & 0xFF)
  return length

if __name__ == '__main__':
  sendRequest("localhost", 6609, '6012019999', '01', 'EC0-6012019999-01', "hello dmb")