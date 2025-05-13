
inventory = []

print("Inventory Management Interface\n\n")
print("Main Menu: \n1. Add Product.\n2. Update Product.\n3. Dispaly Inventory.\n4. Exit.\n")

option = input("Select an Option: ")

while option != "4":
    if option.isdigit:
        if option == "1":
            name = input("Enter Product Name: ")
            price = input("Enter Product Price: ")
            quantity = input("Enter Product Quantity: ")
            category = input("Enter Product Category: ")
            inventory.append({"Name":name, "Price": price, "Quantity":quantity, "Category": category})
            print("Product added successfuly!\n")
        elif option == "2":
            to_update = input("Enter product name to update: ")
            newQuant = input("Enter Quantity: ")
            for item in inventory:
                if item["Name"] == to_update:
                    item["Quantity"] = newQuant
        elif option == "3":
            for item in inventory:
                print(f"Name: {item["Name"]}\nQuantity: {item["Quantity"]}\nPrice: {item["Price"]}")
                print("-"*20)
        else:
            print("Invalid Input!\n")
        
    else:
        option = input("Invalid input! please enter a number: ")
        
    option = input("Select an Option: ")
    print()