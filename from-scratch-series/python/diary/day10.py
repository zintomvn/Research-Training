# 1679. Max Number of K-Sum Pairs

# Experiment
nums = [3,1,3,4,3]
k = 6
visited = {}
# visited = {x: 0 for x in range(1, k)}
for num in nums:
    if num < k:
        if num not in visited.keys():
            visited[num] = 1
        else:
            visited[num] += 1
print(visited)
a = nums.sort()
print(a)

def maxOperations(self, nums, k):
    """
    :type nums: List[int]
    :type k: int
    :rtype: int
    """
    n = len(nums)
    # Easy solution (O(n^2)) -> time out
    visited = [False] * n
    cnt = 0 
    for i in range(n):
        if visited[i] == True:
                continue 
        for j in range(i + 1, n):
            if visited[j] == False and nums[i] + nums[j] == k:
                print(j)
                cnt += 1
                visited[j] = True
                break

def maxOperations(self, nums, k):
    # Solution 2: Hash table + Two pointers
    # Mapping - Hash table
    visited = {x: 0 for x in range(1, k)}
    visited = {}
    for num in nums:
        if num < k:
            if num not in visited.keys():
                visited[num] = 1
            else:
                visited[num] += 1
    # left = 1, right = k - 1 -> iteration from left -> right
    left = 1
    right = k - 1
    count = 0 
    print(visited)
    while left <= right:
        # edge case: left == right
        if left not in visited.keys() or right not in visited.keys(): # optimize
            left = left + 1
            right = right - 1
            continue
        if left == right:
            count += (visited[left] // 2)
            break
        delta = min(visited[left], visited[right])
        count += delta
        left = left + 1
        right = right - 1
            
    return count
    
# Optimized solution 1: using mapping -> hash table
def maxOperations(self, nums, k):
    seen = {}
    y = 0 #no of pairs
    for x in nums:
        if seen.get(k-x, 0) > 0:
            seen[k-x] -= 1
            y += 1
        else:
            seen[x] = seen.get(x, 0) + 1
    return y

# Optimized solution 2: 2 pointers
def maxOperations(self, nums, k):
    nums.sort()
    count = 0
    left, right = 0, len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        print(total)
        if total == k:
            count += 1
            left += 1
            right -= 1
        elif total < k:
            left += 1
        elif total > k:
            right -= 1
    return count


# Optimized solution 3: mapping
def maxOperations(self, nums, k):
    count = 0
    seen = {}
    for num in nums:
        target = k - num
        if target in seen and seen[target] > 0:
            seen[target] -= 1
            count += 1
        elif num in seen:
            seen[num] += 1
        else:
            seen[num] = 1
    return count