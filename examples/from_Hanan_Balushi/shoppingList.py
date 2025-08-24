


items = input("Enter shoping items (separated by comma ,): ")
shopping_list = items.split(",")
if len(shopping_list) == 1 and shopping_list[0] == "":
    print(f"Number of items in your shopping list = 0")
else:
    print(f"Number of items in your shopping list = {len(shopping_list)}")