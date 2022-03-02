from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread

from models import User, Rule, LoginRequest, CreateUserRequest, RemoveUserRequest, GetAllUsersRequest, AddRuleRequest, GetAllRulesRequest, RemoveRuleRequest, ApplyRulesRequest, RemoveRulesRequest

import json as Json


class GhostClient(Thread):

  def __init__(self, host, port):
    Thread.__init__(self)
    self.host = host
    self.port = port

  def run(self):
    with socket(AF_INET, SOCK_STREAM) as s:
      print(f'Realizando conexão com {self.host}:{self.port}')
      s.connect((self.host, self.port))

      print('Conexão estabelecida')
      while True:
        cmd = input('> ')

        if cmd.startswith('login') and len(cmd.split(' ')) == 3 and cmd.split(' ')[-1] != "":
          json = self.login_json(cmd)
          s.sendall(json.encode('utf8'))
          data = s.recv(1024)
          print(f'{data.decode("utf8")}')

        elif cmd.startswith('user create') and len(cmd.split(' ')) >= 5 and cmd.split(' ')[-1] != "":
          json = self.get_create_user_json(cmd)
          s.sendall(json.encode('utf8'))
          data = s.recv(1024)
          print(f'{data.decode("utf8")}')

        elif cmd.startswith('user remove') and len(cmd.split(' ')) == 3:
          json = self.remove_user_json(cmd)
          s.sendall(json.encode('utf8'))
          data = s.recv(1024)
          print(f'{data.decode("utf8")}')

        elif cmd == 'user list all':
          json = self.get_all_users_json()
          s.sendall(json.encode('utf8'))
          data = s.recv(1024)

          if data:
            try:
              data = Json.loads(data.decode("utf8"))

              if len(data) == 0:
                print('Nenhum usuário cadastro.')

              for i in data:
                print('--------------------')
                print(f'Name: {i["name"]}')
                print(f'Email: {i["email"]}')
                print(f'Password: {i["password"]}')
            except ValueError as e:
              print(f'{data.decode("utf8")}')

        elif cmd.startswith('rule add') and len(cmd.split(' ')) == 4 and cmd.split(' ')[-1] != "":
          json = self.add_rule_json(cmd)

          if json == 0:
            print('Campo action inválido.')
            continue

          s.sendall(json.encode('utf8'))
          data = s.recv(1024)
          print(f'{data.decode("utf8")}')

        elif cmd == 'rule list all':
          json = self.get_all_rules_json()
          s.sendall(json.encode('utf8'))
          data = s.recv(1024)

          if data:
            try:
              data = Json.loads(data.decode("utf8"))

              if len(data) == 0:
                print('Nenhuma regra adicionada.')

              for i in data:
                print('--------------------')
                print(f'ID: {i["id"]}')
                print(f'IP: {i["ip"]}')
                print(f'Action: {i["action"]}')
            except ValueError as e:
              print(f'{data.decode("utf8")}')

        elif cmd.startswith('rule remove') and len(cmd.split(' ')) == 3:
          json = self.remove_rule_json(cmd)
          s.sendall(json.encode('utf8'))
          data = s.recv(1024)
          print(f'{data.decode("utf8")}')

        elif cmd == 'firewall start':
          json = self.get_firewall_start_json()
          s.sendall(json.encode('utf8'))
          data = s.recv(1024)
          print(f'{data.decode("utf8")}')

        elif cmd == 'firewall stop':
          json = self.get_firewall_stop_json()
          s.sendall(json.encode('utf8'))
          data = s.recv(1024)
          print(f'{data.decode("utf8")}')

        elif cmd == 'quit':
          s.close()
          break
        else:
          print('Comando inválido')

  def login_json(self, cmd):
    aux = cmd.split(' ')
    map = {'email': aux[1], 'password': aux[2]}
    req = LoginRequest(map)

    return req.get_json()

  def get_create_user_json(self, cmd):
    aux = cmd.split(' ')
    name = ""

    for i in range(2, len(aux)-2):
      name += aux[i] + " "

    name = name.removesuffix(" ")

    usuario = User(name, aux[-2], aux[-1])
    req = CreateUserRequest(usuario.map())

    return req.get_json()

  def get_all_users_json(self):
    req = GetAllUsersRequest("")
    return req.get_json()

  def remove_user_json(self, cmd):
    aux = cmd.split(' ')

    email = aux[2]
    req = RemoveUserRequest(email)

    return req.get_json()

  def add_rule_json(self, cmd):
    aux = cmd.split(' ')

    if aux[3] != "ACCEPT" and aux[3] != "DENY":
      return 0

    rule = Rule(aux[2], aux[3])
    req = AddRuleRequest(rule.map())

    return req.get_json()

  def get_all_rules_json(self):
    req = GetAllRulesRequest("")
    return req.get_json()

  def remove_rule_json(self, cmd):
    aux = cmd.split(' ')

    id = aux[2]
    req = RemoveRuleRequest(id)

    return req.get_json()

  def get_firewall_start_json(self):
    req = ApplyRulesRequest("")
    return req.get_json()

  def get_firewall_stop_json(self):
    req = RemoveRulesRequest("")
    return req.get_json()
