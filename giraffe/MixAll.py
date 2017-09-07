# -*- coding: UTF-8 -*-

import random
import string

# gns默认服务ID
DEFAULT_GNS_SERVICEID = '6013010001'
# gns特殊topic
VIP_GNS_TOPIC = 'GNS-ROUTE'

# 生成32位msgId
def generateMsgId():
  return ''.join(random.sample(string.ascii_letters + string.digits,32))

