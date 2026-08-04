# 238. Product of Array Except Self

# Experiment
# nums = [1,2,3,4]
# nums_len = len(nums)

# forward_product = 1
# backward_product = 1
# forward_list = []
# backward_list = []

# for i in range(nums_len):
#     forward_product = forward_product * nums[i]
#     print(nums_len - i - 1, nums[nums_len - i - 1])
#     backward_product = backward_product * nums[nums_len - i - 1]
#     print(backward_product)
#     forward_list.append(forward_product)
#     backward_list.append(backward_product)

# print(forward_list)
# print(backward_list)

# My solution 
def productExceptSelf(self, nums):
    """
    :type nums: List[int]
    :rtype: List[int]
    """
    nums_len = len(nums)
    # edge case
    if nums_len == 1:
        return nums
    # step 1: run forward and backward
    forward_product = 1
    backward_product = 1
    forward_list = []
    backward_list = []
    
    for i in range(nums_len):
        forward_product = forward_product * nums[i]
        backward_product = backward_product * nums[nums_len - i - 1]
        forward_list.append(forward_product)
        backward_list.append(backward_product)
    
    # step 2: save it in array answer
    answer = []
    for i in range(nums_len):
        if i == 0:
            answer.append(backward_list[nums_len - i - 2])
        elif i == nums_len - 1:
            answer.append(forward_list[i - 1])
        else:
            print(i - 1, nums_len - i - 2)
            answer.append(forward_list[i - 1] * backward_list[nums_len - i - 2]) 
    return answer


# Better solution
def productExceptSelf(nums):
    n = len(nums)
    answer = [1] * n # create pre-declared array

    # Prefix products
    prefix = 1
    for i in range(n):
        answer[i] = prefix
        prefix *= nums[i]

    # Suffix products
    suffix = 1
    for i in range(n - 1, -1, -1):
        answer[i] *= suffix
        suffix *= nums[i]

    return answer

# Note that: 
# using prefix product for saving answer => multiply by suffix 
# using pre-declared array