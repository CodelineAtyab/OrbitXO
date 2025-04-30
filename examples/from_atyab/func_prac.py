import time

# DRY Principle (D)on't (R)epeat (Y)ourself and use functions
def greet_vips(vip_name_1, vip_name_2, vip_name_3):
  print("Greetings " + vip_name_1 + ", " + vip_name_2 + ", " + vip_name_3)
  print("Welcome to Technopark")
  print("Its so good to see all of you here")
  print("***********************************\n")
  time.sleep(5)


name_of_vip_guest_1 = "Mr.Ahmed"
name_of_vip_guest_2 = "Mr.Muhannad"
name_of_vip_guest_3 = "Ms.Sohaila"

# Greetings message
greet_vips(name_of_vip_guest_1, name_of_vip_guest_2, name_of_vip_guest_3)

name_of_vip_guest_1 = "Ms.Aya"
name_of_vip_guest_2 = "Ms.Maria"
name_of_vip_guest_3 = "Ms.Hanan"

greet_vips(name_of_vip_guest_1, name_of_vip_guest_2, name_of_vip_guest_3)

name_of_vip_guest_1 = "Ms.Arooba"
name_of_vip_guest_2 = "Ms.Sundus"
name_of_vip_guest_3 = "Ms.Ghadeer"

greet_vips(name_of_vip_guest_1, name_of_vip_guest_2, name_of_vip_guest_3)
