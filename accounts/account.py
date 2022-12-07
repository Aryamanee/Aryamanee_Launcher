class account_class():
    def __init__(self, uuid: str, username: str, cracked: bool, email: str, password: str):
        self.uuid = uuid
        self.username = username
        self.cracked = cracked
        self.email = email
        self.password = password
    def __str__(self):
        if self.cracked:
            self.accounttype = "Cracked"
        else:
            self.accounttype = "Premium"
        return self.username + "[" + self.accounttype + "]"