import math


class Towers:
    damage: int
    recharge_time: int
    time: int
    cost: int
    upgrade_cost: int
    range: int
    level: int
    level_colors: "list[str]"

    def __init__(self):
        self.level = 1
        self.level_colors = ['#CCCCCCA6', '#00CED1A6', '#FF1493A6', '#FFD700A6']

    def distance(self, pos, en_x, en_y):
        return math.dist(pos, [en_x, en_y])

    def hit_enemies(self, pos, enemies: list):
        if self.time > 0:
            self.time -= 1
            return enemies, 0
        self.time = self.recharge_time
        money = 0
        for enemy in enemies:
            distance = self.distance(pos, enemy.x, enemy.y)
            if self.range >= distance:
                if enemy.hit(self.damage):
                    money = enemy.money
                    enemies.remove(enemy)
                break
        return enemies, money

    def sell(self):
        return int(0.9 * self.cost * ((1.6 ** self.level) - 1) / 0.6)

    def level_color(self):
        return self.level_colors[self.level - 1]

    def upgrade(self):
        self.level += 1
        self.damage *= int((1.50) ** self.level)
        self.recharge_time *= int((0.95) ** self.level)
        self.range *= int((1.15) ** self.level)
        self.upgrade_cost *= int((1.60) ** self.level)

    def is_upgradable(self, balance):
        return (balance >= self.upgrade_cost) and (self.level < len(self.level_colors))
