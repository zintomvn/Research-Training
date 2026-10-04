# 11. Container With Most Water
# My solution -> optimized solution zayyy!
def maxArea(height):
    """
    :type height: List[int]
    :rtype: int
    """
    # index: a, b
    # area = min(height[a], height[b]) * (b - a + 1)
    # Solution 1: 
    n = len(height)
    left = 0
    right = n - 1
    max_area = 0
    while left < right:
        area = min(height[left], height[right]) * (right - left)
        if area > max_area:
            max_area = area
        if height[left] <= height[right]:
            left += 1
        else:
            right -= 1
    return max_area
