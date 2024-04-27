# Given a 0-indexed n x n integer matrix grid, return the number of pairs (ri, cj) such that row ri and column cj are equal.
# A row and column pair is considered equal if they contain the same elements in the same order (i.e., an equal array).

# Example 1:
# Input: grid = [[3,2,1],
#                [1,7,6],
#                [2,7,7]]
# Output: 1
# Explanation: There is 1 equal row and column pair:
#             - (Row 2, Column 1): [2,7,7]

# Example 2:
# Input: grid = [[3,1,2,2],
#                [1,4,4,5],
#                [2,4,2,2],
#                [2,4,2,2]]
# Output: 3
# Explanation: There are 3 equal row and column pairs:
#             - (Row 0, Column 0): [3,1,2,2]
#             - (Row 2, Column 2): [2,4,2,2]
#             - (Row 3, Column 2): [2,4,2,2]


#   383ms - Beats 74.65%
#   21.21MB - Beats 89.28%

class Solution:
    def equalPairs(self, grid: list[list[int]]) -> int:
        columns = [[grid[i][g] if i == 0 else grid[i][g] for i in range(len(grid))] for g in range(len(grid[0]))]
        my_dict = {}

        for sublist in columns:
            a = tuple(sublist)
            if a not in my_dict:
                my_dict[a] = 1
            else:
                my_dict[a] += 1
        
        count = 0
        
        for x in grid:
            x = tuple(x)
            if x in my_dict:
                count += my_dict[x]
        
        return count