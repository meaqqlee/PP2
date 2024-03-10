x = lambda a : a + 10
print(x(5))
#it will print 15, because lambda takes anonymus variable

x = lambda a, b : a * b
print(x(a,b))
#print the multiplication of this numbers, so lambda can take multiple variables

def myfunc(n):
  return lambda a : a * n
mydoubler = myfunc(2)
print(mydoubler(11))