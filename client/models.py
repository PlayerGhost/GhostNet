import json

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
        self.ip = ip
        self.action = action

    def map(self):
        map = {'ip': self.ip, 'action': self.action}
        return map


class Request:

    def __init__(self, action, data):
        self.action = action
        self.data = data

    def get_json(self):
        req = {'action': self.action, 'data': self.data}
        return json.dumps(req)

class LoginRequest(Request):

    def __init__(self, data):
        super().__init__('login', data)

class CreateUserRequest(Request):

    def __init__(self, data):
        super().__init__('create_user', data)


class RemoveUserRequest(Request):

    def __init__(self, data):
        super().__init__('remove_user', data)


class GetAllUsersRequest(Request):

    def __init__(self, data):
        super().__init__('listAll_users', data)


class AddRuleRequest(Request):

    def __init__(self, data):
        super().__init__('add_rule', data)


class GetAllRulesRequest(Request):

    def __init__(self, data):
        super().__init__('listAll_rules', data)


class RemoveRuleRequest(Request):

    def __init__(self, data):
        super().__init__('remove_rule', data)

class ApplyRulesRequest(Request):

    def __init__(self, data):
        super().__init__('apply_rules', data)

class RemoveRulesRequest(Request):

    def __init__(self, data):
        super().__init__('remove_rules', data)
