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

def main():
    nums = [0,1,0,3,12]
    print(moveZeroes(nums))


if __name__ == "__main__":
    main()