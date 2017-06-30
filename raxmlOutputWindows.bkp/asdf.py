# class Counter(object):
#     number = 0
#
#     def __init__(self):
#         type(self).number += 1
#
#     def __del__(self):
#         type(self).number -= 1
#
#
# class Account(Counter):
#     def __init__(self, holder, number, balance, credit_line=1500):
#         self.__Holder = holder
#         self.__Number = number
#         self.__Balance = balance
#         Counter.__init__(self)
#
# a = Account('Joe', 100, 1000)
# print a.number
# b = Account('Fred', 100, 1000)
# print b.number

class Pet(object):

    def __init__(self, name, species):
        self.name = name
        self.species = species

    def getName(self):
        return self.name

    def getSpecies(self):
        return self.species

    def __str__(self):
        return "%s is a %s" % (self.name, self.species)

class Dog(Pet):
    def __init__(self, name, chases_cats):
        Pet.__init__(self, name, "Dog")
        self.chases_cats = chases_cats

    def chasesCats(self):
        return self.chases_cats

class Cat(Pet):

    def __init__(self, name, hates_dogs):
        Pet.__init__(self, name, "Cat")
        self.hates_dogs = hates_dogs

    def hatesDogs(self):
        return self.hates_dogs

fido = Dog("Fido", True)
rover = Dog("Rover", False)
mittens = Cat("Mittens", True)
fluffy = Cat("Fluffy", False)

print fido.species

print fido