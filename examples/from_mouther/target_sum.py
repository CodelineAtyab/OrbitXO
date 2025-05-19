def find_target_sum(nums, target):
    seen = set()
    output = set()

    for num in nums:
        complement = target - num
        if complement in seen:
            output.add((min(num, complement), max(num, complement)))
        seen.add(num)

    return list(output)

number_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
target = 10
result = find_target_sum(number_list, target)
print(f"Pairs that sum to {target}: {result}")
