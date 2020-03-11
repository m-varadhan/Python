class User:
    def __init__(self,username):
        self.username = username
        self.get = self.__dict__.get

    def __getitem__(self,attr):
        return self.__dict__[attr]


user = User('Varadhan')


print(user.username)
print(user.name)
print(user['username'])
print(user.get('username','NULL'))
print(user.get('name','NULL'))
print(user['name'])
