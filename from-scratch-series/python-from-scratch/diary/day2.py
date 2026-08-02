## 605. Can Place Flowers
## 1431. Kids with The Greatest Number of Candies

## 605. Can Place Flowers
# My solution
def canPlaceFlowers1(flowerbed, n):
    """
    :type flowerbed: List[int]
    :type n: int
    :rtype: bool
    """
    # 1. Iterate each element in flowerbed
    # 2. if a[i-1] and a[i+1] and a[i] == 0
    if n == 0 or len(flowerbed) == 1 and flowerbed[0] == 0 and n == 1:
        return True
    if len(flowerbed) in [0, 1]:
        return False 
    count = n
    i = 0
    while True:
        if count == 0:
            return True
        if i >= len(flowerbed):
            break
        if i == 0:
            if flowerbed[i] == 0 and flowerbed[i + 1] == 0:
                count -= 1
                i = i + 2
                continue
        elif i == len(flowerbed) - 1:
            if flowerbed[i] == 0 and flowerbed[i - 1] == 0:
                count -= 1
                i = i + 2
                continue
        elif flowerbed[i] == 0 and flowerbed[i + 1] == 0 and flowerbed[i - 1] == 0:
            count -= 1
            i = i + 2
            continue
        i = i + 1
    return False

# Optimized solutions - smart
def canPlaceFlowers2(flowerbed, n):
    zeros, ans = 1, 0  # Easier handling of prefixes, just initialize zeros to 1
    for f in flowerbed:
        if f == 0: 
            zeros += 1
        else:
            ans += (zeros - 1) // 2
            zeros = 0
        print(f, zeros, ans)
    return ans + zeros // 2 >= n  # Note that suffix zeros need not -1

flowerbed = [1,0,0,0,1]
n = 1
print(canPlaceFlowers2(flowerbed, n))


## 1431. Kids with The Greatest Number of Candies
# My solution
def kidsWithCandies(candies, extraCandies):
    """
    :type candies: List[int]
    :type extraCandies: int
    :rtype: List[bool]
    """
    # solu 1: 
    # 1. find max among all kids
    # 2. compare max ~ element + extra
    result = []
    max_candies = 0
    for i in range(len(candies)):
        if max_candies < candies[i]:
            max_candies = candies[i]
    
    for i in range(len(candies)):
        if candies[i] + extraCandies >= max_candies:
            result.append(True)
        else:
            result.append(False)
    return result