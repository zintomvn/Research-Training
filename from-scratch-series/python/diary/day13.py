# 1493. Longest Subarray of 1's After Deleting One Element
# My solution - hơi tèo rồi
# def longestSubarray(nums):
#     """
#     :type nums: List[int]
#     :rtype: int
#     """
#     # First solution: consider each i and save in window
#     # if k > 0: s++ 
#     # if 
#     max_sum = 0
#     s = 0
#     result_idx = 0
#     pos = 0
#     k = 1
#     n = len(nums)
#     for i in range(n):
#         if k >= 0 and nums[i] == 1:
#             s += 1
#             print("index:",i)
#         if nums[i] == 0:
#             k = k - 1 # k = -1
#             pos = i
#         if i >= s and nums[i - s] == 0:
#             k = k + 1
#         if max_sum < s:
#             max_sum = s
#             result_idx = pos
#             print(max_sum)

#     return max_sum - 1

# def longestSubarray(nums):
#     """
#     :type nums: List[int]
#     :rtype: int
#     """
#     # First solution: consider each i and save in window
#     # if k > 0: s++ 
#     # if 
#     max_sum = 0
#     s = 0
#     k = 1
#     n = len(nums)
#     for i in range(n):
#         if nums[i] == 0:
#             k = k - 1
#             print("index:",i, k)
#         if k >= 0:
#             s += 1
#         if i >= s and nums[i - s] == 0:
#             k = k + 1
#         if max_sum < s:
#             max_sum = s
#             print(i, max_sum)

#     return max_sum - 1

# Solution: Sliding window and two pointers 

def longestSubarray(nums):
    max_sum = 0
    left = 0
    zero_count = 0

    # idea: using 2 pointers (if zero_count )
    for right in range(len(nums)):
        if nums[right] == 0:
            zero_count += 1

        while zero_count > 1:
            if nums[left] == 0:
                zero_count -= 1
            left += 1
        max_sum = max(max_sum, right - left)
    return max_sum

nums = [0,1,1,1,0,1,1,0,1]
print("Result:", longestSubarray(nums))