import math


class Towers:
    damage : int
    recharge_time : int
    time: int
    cost : int
    upgrade_cost: int
    range : int
    level: int

    def __init__(self):
        self.level = 1

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
        return int(0.9 * self.cost)

    def upgrade(self):
        self.level += 1
        self.damage *= int((1.50) ** self.level)
        self.recharge_time *= int((0.95) ** self.level)
        self.random *= int((1.15) ** self.level)
        self.upgrade_cost *= int((1.60) ** self.level)
