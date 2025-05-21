def find_taget_sum(nums, target):
    result = []

    for num in nums:
        for other in nums:
            if num != other and num + other == target:
                pair = tuple(sorted((num, other)))
                if pair not in result:
                    result.append(pair)
    return result
   
print(find_taget_sum([1, 2, 3, 4, 5, 6], 9))