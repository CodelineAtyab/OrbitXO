def find_target_sum(nums, target):
    seen_nums = set()
    result_pairs = set()

    for n in nums:
        needed = target - n
        if needed in seen_nums:
            result_pairs.add(tuple(sorted((n, needed))))
        seen_nums.add(n)

    return list(result_pairs)

print(find_target_sum([2, 7, 11, 15, -2], 9))
print(find_target_sum([3, 2, 4, 3], 6))
print(find_target_sum([1, 5, 3, 8], 12))