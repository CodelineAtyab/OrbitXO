# DRY Principle (D)on't (R)epeat (Y)ourself and use functions
def greet_vips(*args):
  greeting_msg = "Greetings! "
  mulitple_names_str = ""
  for name in args:
    mulitple_names_str = mulitple_names_str + " " + name

  print(greeting_msg + mulitple_names_str)
  print("Welcome to Technopark")
  print("Its so good to see all of you here")
  print("***********************************\n")

def greet_the_ceo(name, citation_count, recent_publication, company_name, *args, **kwargs):
  print("Really nice to have you here: " + name)
  print("Its impressive that you have " + str(citation_count) + " number of citations on your research paper")
  print("We know about your recent " + recent_publication)
  print("We would like to know more about " + company_name + "!")
  print(args)
  print("CEO's Profile:")

  type(kwargs)
  print(kwargs)

  for curr_key in kwargs.keys():
    print(curr_key + " | " + kwargs[curr_key])

  print("\n")
  
greet_the_ceo("Mr.C", 
              18,
              "IoT Agentic Framework",
              "Yet Another Meta",
              "12637123abc",
              "ASW-456",
              comes_in_top_5_companies="Comes in Top 5 Companies",
              other_startup_count="5",
              net_worth="5 Billion")


name_of_vip_guest_1 = "Mr.Ahmed"
name_of_vip_guest_2 = "Mr.Muhannad"
name_of_vip_guest_3 = "Ms.Sohaila"

# Greetings message
greet_vips(
  name_of_vip_guest_1, 
  name_of_vip_guest_2, 
  name_of_vip_guest_3,
  "Ms. Fatma",
  "Ms.Ikhlaas",
  "Mouther"
)

name_of_vip_guest_1 = "Ms.Aya"
name_of_vip_guest_2 = "Ms.Maria"
name_of_vip_guest_3 = "Ms.Hanan"

greet_vips(name_of_vip_guest_1, name_of_vip_guest_2, name_of_vip_guest_3, "Atyab", "Tufool", "Aya", "Ahmed")

name_of_vip_guest_1 = "Ms.Arooba"
name_of_vip_guest_2 = "Ms.Sundus"
name_of_vip_guest_3 = "Ms.Ghadeer"

greet_vips(name_of_vip_guest_1, name_of_vip_guest_2, name_of_vip_guest_3)
