

def find_target_sum(nums, target):
    
    seen = set()
    results = []

    for num in nums:
        complement = target - num
        if complement in seen:
            results.append((complement,num))
        seen.add(num)
    print(f"nums={nums} Target={target} \n Target sum = {results}")

find_target_sum([2, 7, 11, 15, -2] , 9 )
find_target_sum([3, 2, 4, 3] , 6)
find_target_sum([1, 5, 3, 8] , 12)
















"""sums = {}
    for i in range(len(nums)):
        if i != len(nums)-1:
            sums[nums[i]] = nums[i+1:]
    result = [(k, v) for k, lst in sums.items() for v in lst if k + v == target]
    print(result)"""