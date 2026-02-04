class Engine:
    def move(self):
        print("Engine is running")

class Wheels:
    def move(self):
        print("Wheels are rolling")

class Car(Engine, Wheels):   # ← multiple inheritance
    pass

c = Car()
c.move()
