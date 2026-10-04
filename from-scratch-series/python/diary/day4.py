# 151. Reverse Words in a String

# Experiment 
s = "the sky is blue"
# word = ''
# word = word + s[0]
# word = word + s[1]
# print(word)
# s2 = ["123", "234", "345"]
# result = " ".join(reversed(s2))
# print(result)
# s3 = "xin    chao    toi    la"
# print(s3.split())

# My solution
def reverseWords(s):
    """
    :type s: str
    :rtype: str
    """
    if len(s) == 1:
        return s
    str_list = []
    word = ""
    for i in range(len(s)):
        if s[i] != " ":
            word = word + s[i]
        if word != "" and s[i] == " " or word != "" and i == len(s) - 1:
            str_list.append(word)
            word = ""
    result = " ".join(reversed(str_list))
    return result

s = "the sky is blue"

import time
start_time = time.perf_counter()
print(reverseWords(s))
end_time = time.perf_counter()
print(end_time - start_time)
# print(reverseWords(s))

# Better solutions
def reverseWords2(s):
    l=s.split()
    l.reverse()
    ns=""
    for i in range(0,len(l)):
        ns+=l[i]
        if i!=len(l)-1:
            ns+=" "
    return ns

import time
start_time = time.perf_counter()
print(reverseWords2(s))
end_time = time.perf_counter()
print(end_time - start_time)

