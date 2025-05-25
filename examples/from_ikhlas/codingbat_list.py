#CodingBat List1 Excercise:

#Ex1
def first_last6(nums):
  return nums[0]==6 or nums[-1]==6
first_last6([1,2,6])

############################################################
#Ex2
def same_first_last(nums):
  return len(nums)>=1 and nums[0] == nums[-1]
print(same_first_last([1,2,3]))
print(same_first_last([1, 2, 3, 1]))
print(same_first_last([1, 2, 1]))

#another solution
def same_first_last(nums):
  if len(nums)>=1:
    nums[0] == nums[-1]
  return True
print(same_first_last([1,2,3,1]))

##############################################################
#Ex3
def make_pi():
  return [3,1,4]
print(make_pi())

###############################################################
#Ex4
def common_end(a, b):
  return a[0]==b[0] or a[-1]==b[-1]
print(common_end([1,2,3],[7,3]))
print(common_end([1, 2, 3], [7, 3, 2]))
print(common_end([1, 2, 3], [1, 3]))

##############################################################
#Ex5
def sum3(nums):
  return nums[0]+nums[1]+nums[2]
print(sum3([1,2,3]))

#################################################################
#Ex6
def rotate_left3(nums):
  return nums[1:] + nums[:1]
  
print(rotate_left3([1,2,3]))
print(rotate_left3([5,11,9]))
print(rotate_left3([7,0,0]))

#######################################################################
#Ex7
def reverse3(nums):
  return nums[::-1] 
print(reverse3([1,2,3]))
print(reverse3([5,11,9]))
print(reverse3([7,0,0]))

##################################################################
#Ex8
def max_end3(nums):
  max_value = max(nums[0], nums[2])
  return [max_value, max_value, max_value]
print(max_end3([1,2,3]))
print(max_end3([11,5,9]))
print(max_end3([2,11,3]))

##################################################################
#Ex9
def sum2(nums):
  return sum(nums[:2])
print(sum2([1,2,3]))
print(sum2([1,1]))
print(sum2([1,1,1,1]))

#######################################################################
#Ex10
def middle_way(a, b):
  new_list = [a[1] , b[1]]
  return new_list
print(middle_way([1,2,3], [4,5,6]))
print(middle_way([7, 7, 7], [3, 8, 0]))
print(middle_way([5, 2, 9], [1, 4, 5]))

###########################################################################
#Ex11
def make_ends(nums):
  new_lst= [nums[0],nums[-1]]
  return new_lst
print(make_ends([1,2,3]))
print(make_ends([1,2,3,4]))
print(make_ends([7,4,6,2]))

###########################################################################
#Ex12
def has23(nums):
  return 2 in nums or 3 in nums   
print(has23([2,5]))
print(has23([4,3]))
print(has23([4,5]))

####################################################################
####################################################################
####################################################################

#List2 Codingbat Exercise

#Ex1

def count_evens(nums):
  n = 0
  for num in nums:
    if num % 2==0:
      n=n+1
  return n  
print(count_evens([2,1,2,3,4]))
print(count_evens([2, 2, 0]))
print(count_evens([1, 3, 5]))

######################################################################

#Ex2 
def big_diff(nums):
  smallest=min(nums)
  largest=max(nums)
  return largest - smallest
print(big_diff([10,3,5,6]))
print(big_diff([7,2,10,9]))
print(big_diff([2,10,7,2]))

#####################################################################33

#Ex3
def centered_average(nums):
  total=sum(nums)
  minimum=min(nums)
  maximum=max(nums)
  value=total-maximum-minimum
  avg = value//(len(nums)-2)
  return avg
print(centered_average([1, 2, 3, 4, 100]))
print(centered_average([1, 1, 5, 5, 10, 8, 7]))
print(centered_average([-10, -4, -2, -4, -2, 0]))

##########################################################################

#Ex4
##Using while loop:
def sum13(nums):
  sum = 0
  index = 0 
  while index <len(nums):
    if nums[index]==13:
      index=index+2
    else:
      sum= sum + nums[index]
      index=index+1
  return sum 
print(sum13([1,2,2,1]))
print(sum13([1,1]))
print(sum13([1,2,2,1,13]))

##using for loop:
def sum13(nums):
  sum = 0
  for index in range(len(nums)):
    if nums[index]==13:
      index=index+1
    else:
      sum= sum + nums[index]
  return sum 
print(sum13([1,2,2,1]))
print(sum13([1,1]))
print(sum13([1,2,2,1,13]))

########################################################################

#Ex5
def sum67(nums):
  sum=0
  index=0
  while index < (len(nums)):
    if nums[index]==6:
      while nums[index]!=7:
        index=index+1
      index=index+1
    else:
      sum=sum+nums[index]
      index=index+1
  return sum
print(sum67([1,2,2]))
print(sum67([1,2,2,6,99,99,7]))
print(sum67([1,1,6,7,2]))

#########################################################################

#Ex6
def has22(nums):
  for index in range(len(nums)-1): 
    if nums[index]==2 and nums[index+1]==2:
       return True
  return False
print(has22([1,2,2]))
print(has22([1,2,1,2]))
print(has22([2,1,2]))


