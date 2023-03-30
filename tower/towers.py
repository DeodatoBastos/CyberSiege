class Towers:
    damage : int
    recharge_time : int
    imageStr : str
    cost : int
    range : int 

class antivirus(Towers):
    def __init__(self):
        super().__init__()
        self.imageStr = 'antivirus'
        self.damage = 30
        self.recharge_time = 1
        self.cost = 20
        self.range = 100

class firewall(Towers):
    def __init__(self):
        super().__init__()
        self.imageStr = 'firewall'
        self.damage = 10
        self.recharge_time = 1
        self.cost = 25
        self.range = 30

class twoFactorAuth(Towers):
    def __init__(self):
        super().__init__()
        self.imageStr = '2FA'
        self.damage = 5
        self.recharge_time = 2
        self.cost = 20
        self.range = 300
