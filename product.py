products = []

def add_product():
    name = input("Enter product name: ")
    price = float(input("Enter product's price: "))
    quantity = int(input("Enter product quantity: "))
    category = input("Enter product category: ")

    product = {
        "name": name,
        "price": price,
        "quantity": quantity,
        "category": category
    }

    products.append(product)
    print(f"Your product: {name} added!")

def update_quantity():
    name = input("Enter product's name to update: ")
    found = False

    for product in products:
        if product["name"].lower() == name.lower():
            found = True
            print(f"Current quantity: {product['quantity']}")
            change = int(input("Enter quantity change (+ to restock, - to sell): "))
            product["quantity"] += change
            print(f"Updated quantity for {product['name']}: {product['quantity']}\n")
            break
    if not found:
        print("Product not found!")

while True:
    print("Store inventory manager")
    print("1. Add new product")
    print("2. Update product")
    print("3. Show all products")
    print("4. Exit")

    choose = input("Please, Choose an option: ")

    if choose == "1":
        add_product()
    elif choose == "2":
        update_quantity()
    elif choose == "3":
        if not products:
            print("No products to display.\n")
        else:
            for p in products:
                print(f"Name: {p['name']}, Price: ${p['price']}, Quantity: {p['quantity']}, Category: {p['category']}")
            print()
    elif choose == "4":
        print("\nExiting, goodbye")
        break
    else:
        print("Invalid, please try again!")