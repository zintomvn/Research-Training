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
    # for i in range(len(candies)):
    #     if max_candies < candies[i]:
    #         max_candies = candies[i]
    max_candies = max(candies)
    print(f"Max:", max_candies)
    for i in range(len(candies)):
        if candies[i] + extraCandies >= max_candies:
            result.append(True)
        else:
            result.append(False)
    return result

candies = [2,3,5,1,3]
extraCandies = 3

print(kidsWithCandies(candies, extraCandies))
