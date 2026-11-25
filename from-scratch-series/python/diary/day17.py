def equalPairs(grid: list[list[int]]) -> int:
    # solution 1: list row ri and col cj -> same elements = 1 element appear > 2 times
    rows = []
    cols = []
    n = len(grid)
    mp1: dict[list, int] = {}
    mp2: dict[list, int] = {}
    for i in range(n):
        cols.append(grid[i])
        mp1[tuple(grid[i])] = mp1.get(tuple(grid[i]), 0) + 1
    for j in range(len(grid)):
        tmp = []
        for i in range(n):
            tmp.append(grid[i][j])
        rows.append(tmp)
        mp2[tuple(tmp)] = mp2.get(tuple(tmp), 0) + 1
        
    print(set(mp1))
    print(set(mp2))
    equals = set(mp1).intersection(set(mp2))
    count = 0
    for ele in equals:
        count += mp1[ele] * mp2[ele]
    return count 

grid = [[3,2,1],[1,7,6],[2,7,7]]
print(equalPairs(grid))

# Trick chuyển ma trận 
grid_T = list(zip(*grid))
print(grid_T)

# Optimized solution
from collections import Counter

def equalPairs(self, grid: list[list[int]]) -> int:
    grid_T = zip(*grid)
    grid = [tuple(n) for n in grid]
    dict_grid = Counter(grid)
    dict_grid_T = Counter(grid_T)
    N = len(dict_grid.keys())
    pair = 0
    for key,value in dict_grid.items():
        if key in dict_grid_T:
            pair = pair + value * dict_grid_T[key]
    return pair