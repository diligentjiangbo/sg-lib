#!/usr/bin/python

class CreateTopicRequestHeader:

  def __init__(self, topic, readQueueNums, writeQueueNums):
    # default value
    self.defaultTopic = 'TBW102'
    self.perm = '6'
    self.topicFilterType = 'SINGLE_TAG'
    self.topicSysFlag = '0'
    self.order = 'false'

    # special value
    self.topic = topic
    self.readQueueNums = readQueueNums
    self.writeQueueNums = writeQueueNums

  def makeCustomHeaderToNet(self):
    return vars(self)

