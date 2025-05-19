products = []

def add_product():
    name = input("Enter product name: ")
    price = float(input("Enter product's price: "))
    quantity = int(input("Enter product quantity: "))
    catagory = input("Enter product catagory: ")

    product = {
            "name": name,
            "price": price,
            "quantity": quantity,
            "category": catagory
        }
    
    products.append(product)
    print(f" Your product: {name} added!")

def update_quantity():
    name = input("Enter product's name to update: ")
    found = False

    for product in products:
        if product ["name"].lower() == name.lower():
            found = True
            print(f" Current quantity: {product['quantity']}")

            change = int(input("Enter quantity change (+ to restock, - to sell): "))
            product["quantity"]+= change
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

    choose = input("Choose an option from above: ")

    if choose == "1":
        add_product()
    elif choose == "2":
        update_quantity()
    elif choose == "3":
        for p in products:
            print(p)
        print()
    elif choose == "4":
        print("\nExiting .. bye bye")
        break
    else:
        print("Invalid choose, please try again!")