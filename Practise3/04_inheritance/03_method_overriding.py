class Vehicle:
    def move(self):
        print("The vehicle is moving")


class Car(Vehicle):
    def move(self):
        print("The car is driving on the road")


class Boat(Vehicle):
    def move(self):
        print("The boat is sailing on water")

v = Vehicle()
c = Car()
b = Boat()

v.move()  
c.move()  
b.move()  



