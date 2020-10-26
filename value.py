class Value:
    def __init__(self):
        pass

    def __get__(self, instance, owner):
        return self.amount - (self.amount * instance.commission)

    def __set__(self, instance, value):
        self.amount = value
        pass


class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission
