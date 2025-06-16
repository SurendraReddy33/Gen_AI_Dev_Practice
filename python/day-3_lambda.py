#Lambda creates a small anonymous function (no name) in one line. Used for short, Throwaway functions.

square = lambda x:x**2
print(square(2))
print(square(5))

#map
numbers = [1,2,3,9,5]
squared = list(map(lambda x: x**2, numbers))
print(squared)