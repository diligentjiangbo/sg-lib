#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
import imp

#自定义库
from file.tab_decode import decode
from file.service import Service

#字符串编码统一为utf8
imp.reload(sys)
#sys.setdefaultencoding('utf8')

#文件头部标志
HEADER_START = "HEADER_START"
HEADER_END = "HEADER_END"
#新增服务标志
SERVICE_ADD_START = "SERVICE_ADD_START"
SERVICE_ADD_END = "SERVICE_ADD_END"
#修改服务标志
SERVICE_UPDATE_START = "SERVICE_UPDATE_START"
SERVICE_UPDATE_END = "SERVICE_UPDATE_END"
#删除服务标志
SERVICE_DELETE_START = "SERVICE_DELETE_START"
SERVICE_DELETE_END = "SERVICE_DELETE_END"


#错误码
#header错误
header_error=1
#add错误
add_error=2
#update错误
update_error=3
#delete错误
delete_error=4
#某一模块标签重复，导致同时两个状态读取
multiple_error=5

def analyze(file):
  #返回的dict，结构为{"result":0,"version":1.0,"add":set(),"update":set(),"delete":set()}
  retDict = {}
  
  #头部状态
  head_status = 0 
  #新增栏状态，存储结构
  add_status = 0
  add_set = set()
  #更新栏状态，存储结构
  update_status = 0
  update_set = set()
  #删除栏状态，存储结构
  delete_status = 0
  delete_set = set()
  
  #读取文件内容并分析
  for line in file.readlines():
    line = line.decode('utf-8')
    line = line.strip()
    if line.startswith('#'):
      continue
    elif line == HEADER_START:
      #如果碰到头部开始标志，但是头部读取状态是1代表已开始，表示格式错误，退出。后面类似
      if head_status:
        retDict.setdefault('result', header_error)
        return retDict
      else:
        head_status = 1
    elif line == HEADER_END:
      if head_status:
        head_status = 0
      else:
        retDict.setdefault('result', header_error)
        return retDict
    elif line == SERVICE_ADD_START:
      if add_status:
        retDict.setdefault('result', add_error)
        return retDict
      else:
        add_status = 1
    elif line == SERVICE_ADD_END:
      if add_status:
        add_status = 0
      else:
        retDict.setdefault('result', add_error)
        return retDict
    elif line == SERVICE_UPDATE_START:
      if update_status:
        retDict.setdefault('result', update_error)
        return retDict
      else:
        update_status = 1
    elif line == SERVICE_UPDATE_END:
      if update_status:
        update_status = 0
      else:
        retDict.setdefault('result', update_error)
        return retDict
    elif line == SERVICE_DELETE_START:
      if delete_status:
        retDict.setdefault('result', delete_error)
        return retDict
      else:
        delete_status = 1
    elif line == SERVICE_DELETE_END:
      if delete_status:
        delete_status = 0
      else:
        retDict.setdefault('result', delete_error)
        return retDict
    else:
      if head_status:
        retDict.setdefault('version', line)
      else:
        print(line)
        service = decode(line)
        #service = file.json_decode.decode(line)
        if not service:
          continue
        if add_status:
          add_set.add(service)
        elif update_status:
          update_set.add(service)
        elif delete_status:
          delete_set.add(service)
    
  #判断文件是否完整，是否正常结束
  if head_status or add_status or update_status or delete_status:
    retDict.setdefault('result', multiple_error)
    return retDict
  
  #设置读取到的内容
  retDict.setdefault('result', 0)
  retDict.setdefault('add', add_set)
  retDict.setdefault('update', update_set)
  retDict.setdefault('delete', delete_set)
  return retDict
  
if __name__ == '__main__':
  if len(sys.argv) != 2:
    print("python ",sys.argv[0]," fileName")
    sys.exit()
  
  fileName = sys.argv[1]
  try:
    if os.path.exists(fileName):
      f = open(fileName, 'r')
    else:
      print("fileName do not exist")
      sys.exit()
    
    result = analyze(f)
    print(result)
  finally:
    if os.path.exists(fileName) and f:
      f.close()