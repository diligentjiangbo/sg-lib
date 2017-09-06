#!/usr/bin/python

class DeleteTopicRequestHeader:

  def __init__(self, topic):
    self.topic = topic

  def makeCustomHeaderToNet(self):
    return vars(self)

