def shopping_list():
    x=["milk", "bread", "eggs", "apples"]
    c=[]
    u=["bananas", "cereal", "bananas", "orange juice"]
    return len(x), len(c),len(u)
    
x_count, c_count, u_count = shopping_list()

print("Total items in x:", x_count)
print("Total items in c:", c_count)
print("Total items in u:", u_count)