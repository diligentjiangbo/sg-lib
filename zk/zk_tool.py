#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
import re
import imp

from kazoo.client import KazooClient

#字符串编码统一为utf8
imp.reload(sys)

#路径分隔符
PATH_SEPARATOR = "/"
#根节点
ROUTE_PATH = "/cn/onebank/gns/route"
#叶子节点名称分隔符
SEPARATOR = "-"
#默认法人号
DEFAULT_ORGID = "8888"

#根据服务号和场景号构造zk节点全路径
def createNodeName(serviceId, sceneId, rootPath):
  path = rootPath + PATH_SEPARATOR + DEFAULT_ORGID + PATH_SEPARATOR
  path = path + serviceId[:1] + PATH_SEPARATOR
  path = path + serviceId + SEPARATOR + sceneId
  return path
  
#递归的创建一个zk节点
def createZkNode(zk, nodeName, value):
  print(value)
  print(nodeName)
  index = nodeName.rfind(PATH_SEPARATOR)
  if index == -1:
    zk.create(PATH_SEPARATOR + nodeName, value)
  elif index == 0:
    zk.create(nodeName, value)
  else:
    parentPath = nodeName[:index]
    if not zk.exists(parentPath):
      createZkNode(zk, parentPath, "no data".encode("ascii"))
    zk.create(nodeName, value)
    
#新增一个节点
def add_route(zk, serviceId, sceneId, dfaList, rootPath):
  zk_path = createNodeName(serviceId, sceneId, rootPath)
  if zk.exists(zk_path):
    dfaSet = set(dfaList)
    old_value = zk.get(zk_path)[0].decode("ascii")
    #将旧值分隔，放入新增的dfaSet中，重复的就过滤了
    old_dfas = re.sub('[\[\]]', '', old_value).split(",")
    for dfa in old_dfas:
      dfaSet.add(dfa.strip())
    new_value = "[" + ",".join(list(dfaSet)) + "]"
    zk.set(zk_path, new_value.encode("ascii"))
  else:
    new_value = "[" + ",".join(dfaList) + "]"
    createZkNode(zk, zk_path, new_value.encode("ascii"))
    
#删除一个节点
def delete_route(zk, serviceId, sceneId, dfaList, rootPath):
  zk_path = createNodeName(serviceId, sceneId, rootPath)
  if zk.exists(zk_path):
    old_value = zk.get(zk_path)[0].decode("ascii")
    old_dfa_set = set(re.sub('[\[\]]', '', old_value).split(","))
    for dfa in dfaList:
      if dfa in old_dfa_set:
        old_dfa_set.remove(dfa)
    #如果删除了还有值，还保留节点
    if old_dfa_set:
      new_value = "[" + ",".join(list(old_dfa_set)) + "]"
      zk.set(zk_path, new_value.encode("ascii"))
    else:
      zk.delete(zk_path, recursive=True)
      
if __name__ == '__main__':
  zk_host = "localhost:2181"
  zk = KazooClient(zk_host)
  zk.start()
  dfaList = list()
  dfaList.append("1C0")
  delete_route(zk, "67895", "01", dfaList)
  
    
