word1 = "cabbba"
word2 = "abbccc"

# My solution 1
def closeStrings(word1: str, word2: str) -> bool:
    mp1: dict[str, int] = {}
    mp2: dict[str, int] = {}
    # condition 1: num of distinct letters of word1 = word2 
    # condition 2: len of word1 = len of word2
    # condition 3: values of word 1 = values of word 2
    for i in range(len(word1)):
        mp1[word1[i]] = mp1.get(word1[i], 0) + 1
    for i in range(len(word2)):
        mp2[word2[i]] = mp2.get(word2[i], 0) + 1
    condition1 = (sorted(mp1.keys()) == sorted(mp2.keys()))
    condition2 = len(word1) == len(word2)
    condition3 = sorted(mp1.values()) == sorted(mp2.values())
    result = condition1 and condition2 and condition3
    return result

print(closeStrings(word1, word2))

# optimized solution
from collections import Counter
def closeStrings2(word1: str, word2: str) -> bool:
    frequency_word1 = Counter(word1)
    frequency_word2 = Counter(word2)

    sorted_values_word1 = sorted(frequency_word1.values())
    sorted_values_word2 = sorted(frequency_word2.values())
    
    keys_match = set(frequency_word1.keys()) == set(frequency_word2.keys())

    return sorted_values_word1 == sorted_values_word2 and keys_match

print(closeStrings2(word1, word2))