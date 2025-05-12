inventory = {}
while True:
    print("1. Add Product")
    print("2. update quantity")
    print("3. Exit")
    choice = input("Enter your choice: ")
    if choice == '1':
        pname = input("Enter product name: ")
        price = input("Enter product price: ")
        quantity = input("Enter product quantity: ")
        category = input("Enter product category: ")
        inventory[pname] = {
            "price": price,
            "quantity": quantity,
            "category": category}
        print("Product added to inventory.")
    elif choice == '2':
        pname = input("Enter product name to update: ")
        if pname in inventory:
            quantity = input("Enter new quantity: ")
            inventory[pname]["quantity"] = quantity
            print("Product quantity updated.")
        else:
            print("Product not found in inventory.")
    elif choice == '3':
        print("Exiting...")
        break
    




