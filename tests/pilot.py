class Pilot:
    """Тестовая обёртка: пассажир управляет лодкой."""
    def __init__(self, submarine):
        self.submarine = submarine

    def dive(self, depth):
        return self.submarine.dive(depth)

    def swim(self, distance):
        return self.submarine.swim(distance)

    def recharge(self, amount):
        return self.submarine.recharge(amount)

    def damage_propeller(self):
        return self.submarine.damage_propeller()

    def repair_propeller(self):
        return self.submarine.repair_propeller()
