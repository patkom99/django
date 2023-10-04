# while True:
#     try:
#         age = int(input("Enter your age: "))
#         break
#     # except ValueError:
#     #     print("Maybe you have entered wrong value in the input")

#     except Exception as e:
#         print(e)

# if age < 18:
#     print("You can't play this game")
# else:
#     print("You can play this game")

# def divide(a,b):
#     try:
#         return a/b
        
    
#     except ZeroDivisionError as e:
#         print(e)


#     except TypeError:
#         print("Number must be int or float")

#     except :
#         print("Unknown Error")

        
    
# print(divide(8,0))

class NameTooShortError(ValueError):
    pass

def validate(name):
    if len(name) < 8:
        raise NameTooShortError ('Name is Too Short')
    

username = input("Enter Name : ")
validate(username)
print(f"Hello {username}")