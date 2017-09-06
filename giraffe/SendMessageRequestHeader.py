import time
import json

class SendMessageRequestHeader:
  def __init__(self, group, topic, user_properties):
    # default value
    self.defaultTopic = 'TBW102'
    self.defaultTopicQueueNums = '4'
    self.queueId = '0'
    self.sysFlag = '0'
    self.flag = '0'
    self.reconsumeTimes = '0'
    self.unitMode = 'false'

    # var value
    self.producerGroup = group
    self.topic = topic
    self.bornTimestamp = str(int(round(time.time() * 1000)))
    properties_list = []
    for (k, v) in user_properties.items():
      s = k + "1" + v + "2"
      properties_list.append(s)
    self.properties = "".join(properties_list)

  def makeCustomHeaderToNet(self):
    # for name, value in vars(self).items():
    #     print "name=" + name + ":" + "value=" + value
    return vars(self)

if __name__ == '__main__':
  d = {}
  d.setdefault("onekey", "onevalue")
  d.setdefault("twokey", "twovalue")
  request = SendMessageRequestHeader("20101", "6012019999", d)
  dict = request.makeCustomHeaderToNet()
  for k, v in dict.items():
    print k + ":" + v
  print json.dumps(request.__dict__)