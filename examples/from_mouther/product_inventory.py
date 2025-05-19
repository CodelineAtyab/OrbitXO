store_inventory = {}

while True:
    print("\nStore Inventory Manager")
    print("1. Add Product")
    print("2. Update Quantity")
    print("3. View All Products")
    print("4. Exit")

    choice = input("Choose an option: ")

    if choice == '1':
        name = input("Product Name: ").strip().lower()
        if name in store_inventory:
            print("Product already exists.")
        else:
            price = float(input("Price: "))
            quantity = int(input("Quantity: "))
            category = input("Category: ").strip()
            store_inventory[name] = {
                'price': price,
                'quantity': quantity,
                'category': category
            }
            print(f"Product '{name}' added successfully.")

    elif choice == '2':
        name = input("Enter product name to update quantity: ").strip().lower()
        if name in store_inventory:
            print(f"Current quantity: {store_inventory[name]['quantity']}")
            change = int(input("Enter quantity change (+ for restock, - for sold): "))
            store_inventory[name]['quantity'] += change
            print(f"Updated quantity for '{name}': {store_inventory[name]['quantity']}")

        else:
            print("Product not found.")

    elif choice == '3':
        if not store_inventory:
            print("No products in inventory.")
        else:
            print("Current Inventory:")
            for name, info in store_inventory.items():
                print(f"{name.title()}: Price= {info['price']}, Quantity= {info['quantity']}, Category= {info['category']}")

    elif choice == '4':
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")
