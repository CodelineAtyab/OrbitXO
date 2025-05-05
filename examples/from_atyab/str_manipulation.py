team_name: str = "Code Orbit"
paragraph: str = "A quick brown fox jumps over a lazy dog"

# Accessing a specific character from a "collection of characters" -> (String)
print(team_name)
print(team_name[0])
print(team_name[1])
print(team_name[len(team_name)-1])
print(team_name[-1])
print("-----------------------------\n\n")

index = 0

while index < len(team_name):
  print(team_name[index])

  # if team_name[index] == "a" or team_name[index] == "e" or team_name[index] == "i" or team_name[index] == "o" or team_name[index] == "u":
  #     print("Vowel Found: " + team_name[index])

  if team_name[index] in ["a", "e", "i", "o", "u"]:
    print("Vowel Found: " + team_name[index])

  index = index + 1  # Increment by 1 every time this is called

print("-----------------------------\n\n")
print(team_name[0:3:1] + team_name[3:7:1] + team_name[7:10:1])

customer_info = "Mr.A; 920123456  ;mra@gmail.com; 1003442020309949485    "
data_chunks = customer_info.split(";")

name = data_chunks[0].strip()
contact_no = data_chunks[1].strip()
email = data_chunks[2].strip()
bank_account_no = data_chunks[3].strip()  # Leading and Trailing Spaces are stripped

print(f"Name: {name} | Contact: {contact_no} | email: {email}")
# ""
# f""
# r""
# b""
# print(customer_info)
# print(name)
# print(contact_no)
# print(email)
# print(bank_account_no)

print("END OF SCRIPT ....")
