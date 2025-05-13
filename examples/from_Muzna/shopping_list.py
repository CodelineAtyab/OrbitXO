items = input("Enter items in shopping list: ")
items_list=items.split()

items_count=len(items_list)
if len(items_list) == 0:
    print("Shopping list is empty.")
    print("The number of items = 0")
else:
    print("Your shopping list:", items_list)
    print(f"The number of items = {items_count}")