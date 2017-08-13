#!/usr/bin/python

import json

class CreateTopicRequestHeader:
  defaultTopic = 'TBW102'
  perm = '6'
  topicFilterType = 'SINGLE_TAG'
  topicSysFlag = '0'
  order = 'false'

  def __init__(self, topic, readQueueNums, writeQueueNums):
    self.topic = topic
    self.readQueueNums = readQueueNums
    self.writeQueueNums = writeQueueNums

