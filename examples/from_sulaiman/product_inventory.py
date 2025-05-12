inventory = []

while True:

    print("Product Inventory Manegment:\n"
        "1. Add inventory\n"
        "2. Update inventory quality\n"
        "3. Print\n"
        "4. Exit\n")
    
    option = input("Choose option: ")

    if option == "1":
        inname = input("Enter inventory name: ")
        inprice = input("Enter price: ")
        while not inprice.isnumeric():
            inprice = input("Enter a price NUMBER:")
        inquantity = input("Enter quantity: ")
        while not inquantity.isnumeric():
            inquantity = input("Enter a quantity NUMBER:")
        incategory = input("Enter category: ")

        inventory.append(dict(name = inname, 
                              price = inprice, 
                              quantity = inquantity, 
                              category = incategory))
    if option == "2":
        name = input("Enter product name: ")
        found = False
        for item in inventory:
            if item["name"] == name:
                quantity = input("Enter the updated quantity for the inventory " + name + ": ")
                item["quantity"] = quantity
                print(item)
                found = True
                break
        if not found:
            print("\nInventory not found\n")
    if option == "3":
        print(inventory)
    if option == "4":
        break