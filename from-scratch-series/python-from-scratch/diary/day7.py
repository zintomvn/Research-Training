# 443. String Compression


# My solution
print(str(12))

a = [1,2,3]
s = []
for num in a:
    s.append(str(num))
print(s)

def compress(chars):
    """
    :type chars: List[str]
    :rtype: int
    """
    # Solution 1
    char_list = []
    num_list = []
    char = ""
    cnt = 0
    # step 1: iterate over list to create list of chars and list of counter  
    n = len(chars)
    for i in range(n):
        if i == 0:
            char = chars[i]
            cnt = 1
        elif chars[i] != char:
            print(chars[i])
            char_list.append(char)
            num_list.append(cnt)
            char = chars[i]
            cnt = 1
        else:
            cnt += 1
        if i == n - 1:
            char_list.append(char)
            num_list.append(cnt)
    # step 2: count and return
    result = []
    length = len(char_list)
    print(char_list)
    print(num_list)
    for i in range(length):
        print(char_list[i], num_list[i])
        result.append(char_list[i])
        if num_list[i] != 1:
            if len(str(num_list[i])) > 1:
                result.extend(char for char in [x for x in str(num_list[i])])
            else:
                result.append(str(num_list[i]))
    print(f"Result: {result}")         
    return len(result)

# chars = ["a","b","b","b","b","b","b","b","b","b","b","b","b"]
chars = ["a","a","b","b","c","c","c"]
print(chars)
print(compress(chars))


# Optimal solution





# Better solution
from typing import List
class Solution:
  def compress(chars: List[str]) -> int:
    ans = 0
    i = 0

    while i < len(chars):
      letter = chars[i]
      count = 0
      while i < len(chars) and chars[i] == letter:
        count += 1
        i += 1
      chars[ans] = letter
      ans += 1
      if count > 1:
        for c in str(count):
          chars[ans] = c
          ans += 1

    return ans