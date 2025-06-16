age = 18
print(age)
print(type(age))

age = 50
print(age)
print(type(age))

age="My age is 60"
print(age)
print(type(age))

my_str = "Hello"
new_str = my_str + "World"
print(new_str)

my_list=[1,2,3]
my_list.append(4)
print(my_list)

def modify_list(my_list):
    my_list.append(99)

my_list = [1,2,3]
modify_list(my_list)
print(my_list)

def modify_list_1(my_str):
    my_str = my_str + "Welcome"

str = "Hi"
modify_list_1(str)
print(str)

age = 25
count = 1_000_000
print(count)