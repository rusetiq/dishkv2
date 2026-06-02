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
            {"input": "([2, 7, 11, 15], 9)", "expected": "[0, 1]"}
        ]
    },
    {
        "id": 2,
        "title": "Sum of Two Numbers",
        "difficulty": "Easy",
        "function_name": "add",
        "base_points": 150,
        "starter_code": "class Solution:\n    def add(self, a: int, b: int) -> int:\n        pass",
        "description": "Write a function to return the sum of two integers a and b.",
        "examples": "Input: a = 3, b = 5\nOutput: 8",
        "input_variable": "a",
        "hidden_test_cases": [
            {"input": "(3, 5)", "expected": "8"}
        ]
    },
    {
        "id": 3,
        "title": "Is Even",
        "difficulty": "Easy",
        "function_name": "isEven",
        "base_points": 150,
        "starter_code": "class Solution:\n    def isEven(self, n: int) -> bool:\n        pass",
        "description": "Write a function to check if a given integer n is even. Return True if even, else False.",
        "examples": "Input: n = 4\nOutput: True\n\nInput: n = 7\nOutput: False",
        "input_variable": "n",
        "hidden_test_cases": [
            {"input": "4", "expected": "True"}
        ]
    },
    {
        "id": 4,
        "title": "Find Maximum",
        "difficulty": "Easy",
        "function_name": "findMax",
        "base_points": 150,
        "starter_code": "class Solution:\n    def findMax(self, nums: list[int]) -> int:\n        pass",
        "description": "Write a function to return the maximum number in a list of integers nums.",
        "examples": "Input: nums = [1, 5, 3, 9, 2]\nOutput: 9",
        "input_variable": "nums",
        "hidden_test_cases": [
            {"input": "[1, 5, 3, 9, 2]", "expected": "9"}
        ]
    },
    {
        "id": 5,
        "title": "Reverse String",
        "difficulty": "Easy",
        "function_name": "reverseString",
        "base_points": 150,
        "starter_code": "class Solution:\n    def reverseString(self, s: str) -> str:\n        pass",
        "description": "Write a function to reverse a given string s.",
        "examples": "Input: s = \"hello\"\nOutput: \"olleh\"",
        "input_variable": "s",
        "hidden_test_cases": [
            {"input": "'hello'", "expected": "olleh"}
        ]
    },
    {
        "id": 6,
        "title": "Fizz Buzz",
        "difficulty": "Easy",
        "function_name": "fizzBuzz",
        "base_points": 150,
        "starter_code": "class Solution:\n    def fizzBuzz(self, n: int) -> list[str]:\n        pass",
        "description": "Write a function that returns a list of strings representing FizzBuzz up to n (1-indexed).\nFor multiples of three, it should be 'Fizz' instead of the number, and for the multiples of five, it should be 'Buzz'. For numbers which are multiples of both three and five, it should be 'FizzBuzz'.",
        "examples": "Input: n = 5\nOutput: [\"1\", \"2\", \"Fizz\", \"4\", \"Buzz\"]",
        "input_variable": "n",
        "hidden_test_cases": [
            {"input": "5", "expected": "[\"1\", \"2\", \"Fizz\", \"4\", \"Buzz\"]"}
        ]
    }
]

BONUS_QUESTIONS = [
    {
        "title": "Bonus Challenge: Even or Odd",
        "description": "Challenge: Determine if an input integer is 'EVEN' or 'ODD'.\n\nclass Solution:\n    def even_or_odd(self, n: int) -> str:\n        return \"EVEN\" if n % 2 == 0 else \"ODD\"\n\nTarget Output: EVEN\nInput (n): ?",
        "starter_code": "try:\n    val = int(input().strip())\n    if val % 2 == 0:\n        print(\"EVEN\")\n    else:\n        print(\"ODD\")\nexcept Exception:\n    print(\"ERROR\")",
        "expected_output": "EVEN",
        "input_type_hint": "An even integer, e.g. 2",
        "order": 1,
        "duration_minutes": 10
    }
]
