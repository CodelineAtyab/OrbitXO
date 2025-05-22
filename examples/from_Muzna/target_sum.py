def find_target_sum(nums, target):

    seen = set()
    trgt_set=set()
    for i in nums:
        div = target - i
        if div in seen:
            trgt_set.add(tuple((i,div)))

        seen.add(i)

    return list(trgt_set)

print(find_target_sum([2, 7, 11, 15, -2], 9))
print(find_target_sum([3, 2, 4, 3], 6))
print(find_target_sum([1, 5, 3, 8], 12))
