import re

print("Text Message Formatter: LOWERCASE URLs")

message = input("\nEnter your text: ")

def lowercase_url(match): #when the re.sub() finds a match it passes it to this function
    return match.group().lower() #the pased match converted to lower

replaced = re.sub(r"https?://\S+",lowercase_url,message,flags=re.IGNORECASE) #find a match & ignore case

print(f"\nConverted message: {replaced}\n")