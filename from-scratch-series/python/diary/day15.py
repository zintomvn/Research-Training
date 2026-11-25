# 2215. Find the Difference of Two Arrays
"""
nums1 = [1,2,3]
nums2 = [2,4,6]

# Solution 1
def findDifference(self, nums1: list[int], nums2: list[int]) -> list[list[int]]:
    mp1: dict[int, int] = {}
    mp2: dict[int, int] = {}
    for i in range(len(nums1)):
        mp1[nums1[i]] = 1
    for i in range(len(nums2)):
        mp2[nums2[i]] = 1
    re1: dict[int, int] = {}
    re2: dict[int, int] = {}
    for i in range(len(nums2)):
        if mp1.get(nums2[i]) is None:
            re2[nums2[i]] = 1
    for i in range(len(nums1)):
        if mp2.get(nums1[i]) is None:
            re1[nums1[i]] = 1
    result = [list(re1.keys()), list(re2.keys())] 
    return result

# Solution 2 - Set (Bản chất cũng là hashmap)
def findDifference(self, nums1: list[int], nums2: list[int]) -> list[list[int]]:
    set1 = set(nums1)
    set2 = set(nums2)
    return [list(set1 - set2), list(set2 - set1)]


"""

# 1207. Unique Number of Occurrences
arr = [1,2,2,1,1,3]
mp: dict[int, int] = {}
for i in range(len(arr)):
    mp[arr[i]] = mp.get(arr[i], 0) + 1
print(list(mp.values()))


# My solutions
def uniqueOccurrences(self, arr: list[int]) -> bool:
    mp: dict[int, int] = {}
    for i in range(len(arr)):
        mp[arr[i]] = mp.get(arr[i], 0) + 1
    
    count_map: dict[int, int] = {}
    for num in list(mp.values()):
        count_map[num] = count_map.get(num, 0) + 1
    for num in list(count_map.values()):
        if num != 1:
            return False
    return True

# Better solution - set
def uniqueOccurrences(self, arr: list[int]) -> bool:
    freq = {}
    for x in arr:
        freq[x] = freq.get(x, 0) + 1

    return len(freq) == len(set(freq.values()))