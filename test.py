class Pet:
    pass


class Cat(Pet):
    pass


print(issubclass(Cat, Pet))
print(isinstance(Cat(), Pet))
