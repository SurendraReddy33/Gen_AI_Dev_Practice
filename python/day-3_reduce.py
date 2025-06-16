# from functools import reduce

# #List
# numbers = [1,2,3,4,5]

# even_numbers = list(filter(lambda x: x % 2==0, numbers))
# print(even_numbers)

# total = reduce(lambda x,y: x + y, numbers)
# print(total)


from functools import reduce

def add(x,y):
    return x + y

numbers = [1,2,3,4,5]
total = reduce(add, numbers)
print("Total:" , total)

total =  reduce(lambda x,y: x+y, numbers)