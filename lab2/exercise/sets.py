fruits = {"apple", "banana", "cherry"}
if "apple" in fruits:
  print("Yes, apple is a fruit!")
#if set consist an certain element

fruits = {"apple", "banana", "cherry"}
fruits.add("orange")
#add method to add

fruits = {"apple", "banana", "cherry"}
more_fruits = ["orange", "mango", "grapes"]
fruits.update(more_fruits)
#adding more_fruits to fruits

fruits = {"apple", "banana", "cherry"}
fruits.remove("banana")
#removing

fruits = {"apple", "banana", "cherry"}
fruits.discard("banana")
#another removing method but its not message us about error if there no element



