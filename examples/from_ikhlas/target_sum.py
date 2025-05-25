def target_sum(nums,target):
    n_set=set()
    result_set=set()
    for i in nums:
        total = target - i
        if total in n_set:
            result_set.add((total,i))
        n_set.add(i)
    return list(result_set)
print(target_sum([2,7,11,15,-2],9))
print(target_sum([3,2,4,3],6))
print(target_sum([1,5,3,8],12))