# Testing 
s = "IceCreAm"
s_list = list(s)
print(len(s_list))
print(s[0].lower())
s_list[0] = 'a'

print(s_list)
print("".join(s_list))

## 345. Reverse Vowels of a String
# My solution
def reverseVowels(s):
    """
    :type s: str
    :rtype: str
    """
    if len(s) == 1:
        return s
    vowel_list = ['a', 'e', 'i', 'o', 'u']
    start_idx = 0
    end_idx = len(s) - 1
    s_list = list(s)
    while start_idx < end_idx:
        if s_list[start_idx].lower() not in vowel_list:
            start_idx += 1
        if s_list[end_idx].lower() not in vowel_list:
            end_idx -= 1
        if s_list[start_idx].lower() in vowel_list and s_list[end_idx].lower() in vowel_list:
            s_list[start_idx], s_list[end_idx] = s_list[end_idx], s_list[start_idx]
            start_idx += 1
            end_idx -= 1
    return "".join(s_list)


# Optimized solution
def reverseVowels(s):
    vowels = set("aeiouAEIOU")
    chars = list(s)

    left, right = 0, len(chars) - 1

    while left < right:
        while left < right and chars[left] not in vowels:
            left += 1
        while left < right and chars[right] not in vowels:
            right -= 1

        chars[left], chars[right] = chars[right], chars[left]
        left += 1
        right -= 1

    return "".join(chars)