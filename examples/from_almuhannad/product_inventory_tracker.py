product = {}
while True:
    print("1. add new products")
    print("2. update products")
    print("3. Exit")
    u = input("choose an option:")

    if u == "1":
        name = input("Name of the product: ")
        price = input("Price: ")
        quantity_product = input("quantity: ")
        category_product = input("Category: ")

        product[name] = {'Price' : price, 'quantity' : quantity_product, 'categoryy' : category_product} 
        print("product added successfully!")
        

    if u == "2":
        if name in product:
            updated_customer = input("update the quantity: ")
            product[name]['quantity'] = updated_customer
            print(product[name])

    if u == "3":
        print("Exiting..")
        break