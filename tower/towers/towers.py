import math


class Towers:
    damage : int
    recharge_time : int
    time: int
    cost : int
    range : int 
    #Tem que ter um script pro ataque tbm

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
