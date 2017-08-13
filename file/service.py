#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Service:
  def __init__(self, service_id, scene_id, dfa, s_version='default', operate='default'):
    self.service_id = service_id
    self.scene_id = scene_id
    self.dfa = dfa
    self.s_version = s_version
    self.operate = operate
    
  def __repr__(self):
    return "Service(service_id=%s,scene_id=%s,dfa=%s,s_version=%s)"\
            % (self.service_id, self.scene_id, self.dfa, self.s_version)
            
  def __eq__(self, other):
    if isinstance(other, Service):
      return ((self.service_id == other.service_id) and \
              (self.scene_id == other.scene_id) and \
              (self.dfa == self.dfa)) 
    else:
      return False
      
  def __hash__(self):
    return hash(self.service_id + " " + self.scene_id + " " + self.dfa)
    
if __name__=='__main__':
  service_a = Service('123', '01', 'CM', 'v1.0')
  service_b = Service('123', '01', 'CM', 'v2.0')
  print(service_a)
  print(service_b)
  print(service_a == service_b)