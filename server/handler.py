import json
import os

from models import User, Rule
from threading import Thread


class Handler(Thread):

    def __init__(self, conn, addr):
        Thread.__init__(self)
        self.conn = conn
        self.addr = addr

    def run(self):
        isLogged = False

        with self.conn:
            while True:
                print(f'Aguardando comando de {self.addr[0]}:{self.addr[1]}')
                data = self.conn.recv(1024)
                if not data: break

                request = json.loads(data.decode('utf8'))

                if not isLogged:
                    if request['action'] == 'login':
                        file = open("database.json", "r")
                        content = file.read()
                        file.close()
                        db = json.loads(content)

                        user = User('', request['data']['email'], request['data']['password'])

                        wrongPassword = False

                        for i in db['users']:
                            if i['email'] == request['data']['email']:
                                if user.verifyPassword(i['password']):
                                    isLogged = True
                                    self.conn.sendall("Login concluído com sucesso!".encode('utf8'))
                                else:
                                    wrongPassword = True
                                    self.conn.sendall("Usuário ou senha inválidos.".encode('utf8'))

                                break

                        if not isLogged and not wrongPassword:
                            self.conn.sendall("Usuário não cadastrado.".encode('utf8'))

                        continue
                    else:
                        self.conn.sendall("Comando inválido ou sem permissão para executar.".encode('utf8'))

                        continue

                if isLogged:
                    if request['action'] == 'create_user':
                        file = open("database.json", "r")
                        content = file.read()
                        file.close()
                        db = json.loads(content)

                        user = User(request['data']['name'], request['data']['email'], request['data']['password'])

                        db['users'].append(user.map())

                        content = json.dumps(db)
                        file = open("database.json", "w")
                        file.write(content)
                        file.close()

                        self.conn.sendall("Usuário criado com sucesso!".encode('utf8'))

                    elif request['action'] == 'remove_user':
                        file = open("database.json", "r")
                        content = file.read()
                        file.close()
                        db = json.loads(content)

                        for i in db['users']:
                            if i['email'] == request['data']:
                                db['users'].remove(i)

                        content = json.dumps(db)
                        file = open("database.json", "w")
                        file.write(content)
                        file.close()

                        self.conn.sendall("Usuário removido com sucesso!".encode('utf8'))

                    elif request['action'] == 'listAll_users':
                        file = open("database.json", "r")
                        content = file.read()
                        file.close()
                        db = json.loads(content)
                        response = json.dumps(db['users'])

                        self.conn.sendall(response.encode('utf8'))

                    elif request['action'] == 'add_rule':
                        file = open("database.json", "r")
                        content = file.read()
                        file.close()
                        db = json.loads(content)

                        rule = Rule(request['data']['ip'], request['data']['action'])

                        db['rules'].append(rule.map())

                        content = json.dumps(db)
                        file = open("database.json", "w")
                        file.write(content)
                        file.close()

                        self.conn.sendall("Regra adicionada com sucesso!".encode('utf8'))

                    elif request['action'] == 'listAll_rules':
                        file = open("database.json", "r")
                        content = file.read()
                        file.close()
                        db = json.loads(content)
                        response = json.dumps(db['rules'])

                        self.conn.sendall(response.encode('utf8'))

                    elif request['action'] == 'remove_rule':
                        file = open("database.json", "r")
                        content = file.read()
                        file.close()
                        db = json.loads(content)

                        for i in db['rules']:
                            if i['id'] == request['data']:
                                db['rules'].remove(i)

                        content = json.dumps(db)
                        file = open("database.json", "w")
                        file.write(content)
                        file.close()

                        self.conn.sendall("Regra removida com sucesso!".encode('utf8'))

                    elif request['action'] == 'apply_rules':
                        file = open("database.json", "r")
                        content = file.read()
                        file.close()
                        db = json.loads(content)

                        try:
                            commandReset = "iptables -F"
                            os.system(commandReset)

                            for i in db['rules']:
                                if i['action'] == 'ACCEPT':
                                    commandApplyAccept = f"iptables -t filter -A FORWARD -i enp0s8 -o enp0s3 -s {i['ip']} -j ACCEPT"
                                    commandApplyAccept1 = f"iptables -t filter -A FORWARD -i enp0s3 -o enp0s8 -d {i['ip']} -j ACCEPT"
                                    os.system(commandApplyAccept)
                                    os.system(commandApplyAccept1)

                                if i['action'] == 'DENY':
                                    commandApplyDeny = f"iptables -t filter -A FORWARD -i enp0s8 -o enp0s3 -s {i['ip']} -j DROP"
                                    commandApplyDeny1 = f"iptables -t filter -A FORWARD -i enp0s3 -o enp0s8 -d {i['ip']} -j DROP"
                                    os.system(commandApplyDeny)
                                    os.system(commandApplyDeny1)

                            self.conn.sendall("Regras aplicadas com sucesso!".encode('utf8'))
                        except ValueError as e:
                            self.conn.sendall("Não foi possível aplicar as regras.".encode('utf8'))

                    elif request['action'] == 'remove_rules':
                        try:
                            commandRemoveRules = "iptables -F"
                            os.system(commandRemoveRules)

                            self.conn.sendall("Regras removidas do firewall com sucesso!".encode('utf8'))
                        except ValueError as e:
                            self.conn.sendall("Não foi remover as regras do firewall.".encode('utf8'))
                    else:
                        self.conn.sendall("Comando inválido.".encode('utf8'))
