def decorate_greet(inc_func):
  def decorated_func():
    print("***************")
    inc_func()
    print("***************")
  return decorated_func

@decorate_greet
def greet_you():
  print("Hello Ikhlas!!!")


@decorate_greet
def greet_your_neighbour():
  print("Hello Muzna!!!")


greet_you()
greet_your_neighbour()

print("END")