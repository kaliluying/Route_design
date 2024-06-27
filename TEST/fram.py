a = 10


class A:
    def __init__(self):
        self.b = 20

    def add(self):
        self.b += a
        return self.b


c = A()

for i in range(10):
    a += 1

print(c.add())
