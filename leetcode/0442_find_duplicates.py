# Given an integer array nums of length n where all the integers of nums are in the range [1, n] and each integer appears once or twice, return an array of all the integers that appears twice.
# You must write an algorithm that runs in O(n) time and uses only constant extra space.

# Example 1:
# Input: nums = [4,3,2,7,8,2,3,1]
# Output: [2,3]

# Example 2:
# Input: nums = [1,1,2]
# Output: [1]

# Example 3:
# Input: nums = [1]
# Output: []

class Solution:
    def findDuplicates(self, nums: list[int]) -> list[int]:
        nums_dictionary = {}
        duplicates = []

        for num in nums:
            if num not in nums_dictionary:
                nums_dictionary[num] = 1
            else:
                if nums_dictionary[num] == 2:
                    pass
                else:
                    nums_dictionary[num] += 1
                    duplicates.append(num)
        
        return duplicates