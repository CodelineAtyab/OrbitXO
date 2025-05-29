def count_shopping_items(shopping_list):
    return len(shopping_list)

# Example test cases
print(count_shopping_items(["milk", "bread", "eggs", "apples"]))         # Output: 4
print(count_shopping_items([]))                                          # Output: 0
print(count_shopping_items(["bananas", "cereal", "bananas", "juice"]))  # Output: 4
