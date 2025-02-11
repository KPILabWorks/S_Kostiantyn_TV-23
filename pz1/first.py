# 21 Реалізувати клас, який веде облік створених об'єктів.

class InstanceCounter:
    count = 0

    def __init__(self):
        type(self).count += 1

    @classmethod
    def get_count(cls):
        return cls.count

    def __del__(self):
        type(self).count -= 1

obj1 = InstanceCounter()
obj2 = InstanceCounter()
obj3 = InstanceCounter()
print(InstanceCounter.get_count())

del obj1
print(InstanceCounter.get_count())
