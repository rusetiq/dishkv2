SOLUTIONS = [
    {
        "id": 1,
        "title": "Two Sum",
        "method_name": "twoSum",
        "difficulty": "Easy",
        "explanation": "Use a hash table to store the value and its index. For each number, check if the complement already exists in the table.",
        "solution_code": "class Solution:\n    def twoSum(self, nums: list[int], target: int) -> list[int]:\n        lookup = {}\n        for i, num in enumerate(nums):\n            if target - num in lookup:\n                return [lookup[target - num], i]\n            lookup[num] = i\n        return []"
    }
]
