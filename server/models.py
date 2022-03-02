import json
import uuid

class User:

  def __init__(self, name, email, password):
    self.name = name
    self.email = email
    self.password = password

  def verifyPassword(self, password):
    return self.password == password

  def map(self):
    map = {'name': self.name, 'email': self.email, 'password': self.password}
    return map

class Rule:

  def __init__(self, ip, action):
    self.id = str(uuid.uuid4())
    self.ip = ip
    self.action = action

  def map(self):
    map = {'id': self.id, 'ip': self.ip, 'action': self.action}
    return map