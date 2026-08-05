nums = [20,100,10,12,5,13]

# My solution --> fail
def increasingTriplet(nums):
    """
    :type nums: List[int]
    :rtype: bool
    """
    # solution 1: simple solution: 3 loops -> time out
    # Solution 2: sort -> index
    # nums = [2,1,5,0,4,6]
    # sorted_indices = [3, 1, 0, 4, 2, 5]
    n = len(nums)
    sorted_indices = sorted(range(len(nums)), key=lambda i: nums[i])
    for i in range(1, n - 1):
        print(sorted_indices[i], nums[sorted_indices[i]])
        if any(x < sorted_indices[i] and nums[x] < nums[sorted_indices[i]] for x in sorted_indices[0:i]) and any(x > sorted_indices[i] and nums[x] > nums[sorted_indices[i]] for x in sorted_indices[i+1:n]):
            return True
    return False

# Better solution: My approach for this problem is actually very simple. 
# we will be first considering min1 and min2 which are the highest possible numbers in integer values.
def increasingTriplet_opt(nums):
    min1 = float('inf')
    min2 = float('inf')
    for n in nums:
        if n <= min1:
            min1 = n  # Update first minimum
            print(f'min 1: {min1}')
        elif n <= min2:
            min2 = n  # Update second minimum
            print(f"min 2: {min2}")
        else:
            return True  # Found a third number greater than both
    return False  # No triplet found

nums = [20,100,10,12,5,13]
print(increasingTriplet_opt(nums))