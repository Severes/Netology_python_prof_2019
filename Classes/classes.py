from pprint import pprint


class Car:
    fuel = 0
    position = 0
    speed = 0
    color = 'black'

    def __init__(self, position, speed, fuel, color):
        self.position = position
        self.speed = speed
        self.fuel = fuel
        self.color = color
        self.some_list = []

    def start(self):
        print('self is:', self )
        print('started')

    def accelerate(self, value):
        self.speed += value

    def move(self, hours):
        self.position += hours * self.speed
        self.fuel -= hours * 10

    def brake(self):
        self.speed = 0

    def stop(self):
        print('stopped')


class Cabrio(Car):
    roof_status = 'folded'

    def unfold(self):
        self.roof_status = 'unfolded'

    def fold(self):
        self.roof_status = 'folded'


cabrio = Cabrio(100, 10, 40, 'red')

cabrio.start()
cabrio.unfold()
print(cabrio.roof_status)

car = Car(100, 120, 40, 'red')
car1 = Car(10, 100, 50, 'green')
print(car.__dict__)
print(car1.__dict__)
print(id(car.some_list))
print(id(car1.some_list))

print(Cabrio.mro())


