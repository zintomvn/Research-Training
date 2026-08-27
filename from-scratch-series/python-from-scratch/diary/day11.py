# 1456. Maximum Number of Vowels in a Substring of Given Length

# My solution
def maxVowels(s, k):
    """
    :type s: str
    :type k: int
    :rtype: int
    """
    # Solution 1: start with max_count = 0 and count = 0
    max_count = 0
    count = 0
    vowel_list = ['a', 'e', 'i', 'o', 'u']
    n = len(s)
    # Step 1: 0-k
    for i in range(0, k):
        if s[i] in vowel_list:
            count += 1
    max_count = count
    # Step 2: k-n -> calculate if is vowel +1
    for i in range(k, n):
        if s[i - k] in vowel_list:
            count -= 1
        if s[i] in vowel_list:
            count += 1
        if count > max_count:
            max_count = count
    return max_count

s = "abciiidef"
k = 3
print(maxVowels(s, k))