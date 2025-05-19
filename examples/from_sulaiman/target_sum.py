import math

numbers_input = input("Enter a bunch of numbers separated by spaces: ")
# numbers_input = "2 7 11 15 -2"
target_sum_input = input("Now enter a target sum number: ")
# target_sum_input = 9

nums = list(map(int, numbers_input.split()))
# nums = list(map(int, user_input.split()))
# nums = [2, 7, 11, 15, -2]
target = int(target_sum_input)
# target = 9


def find_target_sum(nums, target):
    index1 = 0
    index2 = 1
    sums = []
    for i in range(math.comb(len(nums), 2)):
        if nums[index1] + nums[index2] == target:
            sums.append((nums[index1], nums[index2]))
        index2 += 1
        if index2 >= len(nums):
            index1 += 1
            index2 = index1 + 1
    return sums

print(find_target_sum(nums, target))