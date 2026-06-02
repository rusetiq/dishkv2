LEETCODE_PROBLEMS = [
    {
        "id": 1,
        "title": "Two Sum",
        "difficulty": "Easy",
        "function_name": "twoSum",
        "base_points": 150,
        "starter_code": "class Solution:\n    def twoSum(self, nums: list[int], target: int) -> list[int]:\n        pass",
        "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.\n\nReturn the indices sorted in ascending order.",
        "examples": "Input: nums = [2, 7, 11, 15], target = 9\nOutput: [0, 1]\nExplanation: Because nums[0] + nums[1] == 9, we return [0, 1].",
        "input_variable": "nums",
        "hidden_test_cases": [
            {"input": "([2, 7, 11, 15], 9)", "expected": "[0, 1]"},
            {"input": "([3, 2, 4], 6)", "expected": "[1, 2]"},
            {"input": "([3, 3], 6)", "expected": "[0, 1]"}
        ]
    }
]

BONUS_QUESTIONS = [
    {
        "title": "Bonus Challenge: Even or Odd",
        "description": "Challenge: Determine if an input integer is 'EVEN' or 'ODD'.\n\nclass Solution:\n    def even_or_odd(self, n: int) -> str:\n        return \"EVEN\" if n % 2 == 0 else \"ODD\"\n\nTarget Output: EVEN\nInput (n): ?",
        "starter_code": "try:\n    val = int(input().strip())\n    if val % 2 == 0:\n        print(\"EVEN\")\n    else:\n        print(\"ODD\")\nexcept Exception:\n    print(\"ERROR\")",
        "expected_output": "EVEN",
        "input_type_hint": "Enter an integer",
        "order": 1,
        "duration_minutes": 10
    }
]
