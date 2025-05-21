def find_target_sum(numbers, target):
    U = set()        
    R = set()       
    for num in numbers:
        need = target - num 

        if need in U:
           
            pair = tuple(sorted((num, need)))
            R.add(pair)

        U.add(num)  

    return list(R)

print(find_target_sum([2, 7, 11, 15, -2], 9))
print(find_target_sum([3, 2, 4, 3], 6))
print(find_target_sum([1, 5, 3, 8], 12))


