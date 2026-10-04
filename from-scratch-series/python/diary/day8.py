# Two pointers technique:
# 283. Move Zeroes
# 392. Is Subsequence

# 283. Move Zeroes
# My solution: O(N^2) - Swap with 2 iterations
def moveZeroes(nums):
    """
    :type nums: List[int]
    :rtype: None Do not return anything, modify nums in-place instead.
    """
    length = len(nums)
    for i in range(length):
        if nums[i] == 0:
            print(i)
            for j in range(i + 1, length):
                if nums[j] != 0:
                    nums[i], nums[j] = nums[j], nums[i]
                    break
    return nums

# Solution 2: O(N) - Two pointers
def moveZeroes(nums):
    length = len(nums)
    not_zero_index = 0
    for i in range(length):
        if nums[i] != 0:
            nums[not_zero_index] = nums[i]
            not_zero_index += 1
    for i in range(not_zero_index, length):
        nums[i] = 0
    return nums

nums = [0,1,0,3,12]
print(moveZeroes(nums))

# ----------------------------------------
# 392. Is Subsequence
# My solution: Two pointers
def isSubsequence(s, t):
        """
        :type s: str
        :type t: str
        :rtype: bool
        """
        s_length = len(s)
        t_length = len(t)
        s_pointer = 0
        t_pointer = 0
        while True:
            if s_pointer >= s_length:
                return True
            if t_pointer >= t_length:
                return False
            if s[s_pointer] == t[t_pointer]:
                s_pointer += 1
                t_pointer += 1
            else:
                t_pointer += 1
            # Stupid! -> isolate t_pointer condition: t_pointer += 1
        return False

# Better solution: Shorter and check condition in return operation
def isSubsequence(s, t):
    i = 0
    j = 0
    while i < len(s) and j < len(t):
        if s[i] == t[j]:
            i += 1
        j += 1
    return i == len(s)      
