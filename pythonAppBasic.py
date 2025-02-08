# List
a = [1, 2, 3, 4]
print(type(a), 'a =', a)
b = [1, 2, 3, 4]

print('memory a, ', id(a), 'memory b', id(b))

for num in a:
    print(num)

# while loop
counter = 4
while 5 > counter > 1:
    print(counter)
    counter -= counter
    if counter == 2:
        break
    else:
        continue
print('end of while')

# range and for loop
rangeObj = range(10)
print(rangeObj)
print(list(rangeObj))

for i in list(rangeObj):
    print(i)


# Define a Function
def loopRange(givenRange):

    print(givenRange)
    for i in list(givenRange):
        print(i)
    print('end of function')
    return i


print(loopRange(range(10)))

print(dir(__builtins__))

