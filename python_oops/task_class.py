class Laptop:
    discount_percent = 10
    def __init__(self, brand_name, model_name, price):
        self.brand_name = brand_name
        self.model_name = model_name
        self.price = price
        self.combine = brand_name + " " + model_name + str(price)

    def discount_off(self):
        discount = self.price - (self.price * Laptop.discount_percent/100)
        return discount


hp1 = Laptop("Hp", "Hp 1101", 12000)
dell1 = Laptop("Dell", "Dell d1", 63000)

# print(dell1)
# print(dell1.__dict__.brand_name)


# class Person:
#     person_instance_count = 0

#     def __init__(self,brand_name):
#         Person.person_instance_count+=1
#         self.brand_name = brand_name

#     def instance_count():
#         return Person.person_instance_count
# p1 = Person("vishal")
# p1 = Person("vishal")
# p1 = Person("vishal")
# print(Person.person_instance_count)

# class Person:
#     instance_count = 0
#     def __init__(self, name):
#         self.name = name
#         Person.instance_count+=1

#     @classmethod
#     def inst_count(cls):
#         return f"You have created {Person.inst_count} of person class"
    
# p1 = Person("vishal")
# p1 = Person("vishal")
# print(Person.instance_count)

# class Phone:
#     def __init__(self, brand, model, price):
#         self.brand = brand
#         self.model = model
#         self.price = price

#     def phone_spec(self):
#         return f"{self.brand} {self.model}"
    
#     def __repr__(self):
#         return f"Phone(\'{self.brand}\',\'{self.model}\',{self.price})"
    
#     def __str__(self):
#         return f"{self.brand} {self.model} is of price {self.price}"
    
#     def __len__(self):
#         return len(self.phone_spec())
    
#     def __add__(self, other):
#         return self.price + other.price
    

# p1 = Phone("Nokia", 1100, 44000)
# p2 = Phone("Iphone", 500, 12000)
# print(p1 + p2)

# def add(a,b):
#     if (type (a) is int) and (type (b) is int):
#         return a+b
#     raise TypeError ("Oops you used wrong datatypes")

# print(add('4','5'))


# class Animal:
#     def __init__(self,name):
#         self.name=name

#     def sound(self):
#         raise NotImplementedError("you have to define the method in sub class")
    

# class Dog(Animal):
#     def __init__(self, name, breed):
#         super().__init__(name)
#         self.breed=breed

#     def sound(self):
#         return "Bow Bow"

# class Cat(Animal):
#     def __init__(self, name, breed):
#         super().__init__(name)
#         self.breed = breed

#     def sound(self):
#         return "Meow meow"

# dog1 = Dog("Tommy", "Golden Retriever")
# cat1 = Cat("meouu", 'abc')
# print(dog1.sound())
# print(cat1.sound())



class Mobile:
    def __init__(self, name):
        self.name = name

class Mobile_store:
    def __init__(self):
        self.mobiles=[]

    def add_mobiles(self, new_mobile):
        if isinstance(new_mobile, Mobile):
            self.mobiles.append(new_mobile)
        else:
            raise TypeError('New Mobile should be the object of mobile class.')
    
redmi = Mobile("Redmi Note 7s")
samsung = "Samsung Galaxy pro"

mob_store = Mobile_store()
mob_store.add_mobiles(redmi)
a=mob_store.mobiles
print(a[0].name)