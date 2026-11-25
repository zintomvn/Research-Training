# 2390. Removing Stars From a String
# solution 1: consider from right to left + stack save the start
def removeStars(s: str) -> str:
    stack = []
    result = ""
    for cha in s[::-1]:
        if cha == "*":
            stack.append(cha)
        else:
            if len(stack) == 0:
                result += cha
                continue
            stack.pop()
    return result[::-1]

# soltution 2: stack save the string + start -> pop
def removeStars(s: str) -> str:
    stack = []
    for cha in s:
        if cha == "*":
            stack.pop()
        else:
            stack.append(cha)
    return "".join(stack)





