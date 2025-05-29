
Link =input("Enter the URL")

  
if Link.startswith("http://")or Link.startswith("https://"):
  if "."in Link:
   if "." in Link and not Link.endswith("."):
     print ("vailed Link")
     
  else:
     print("not found")
else : 
  print("not found")