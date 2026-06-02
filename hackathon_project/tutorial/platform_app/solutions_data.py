SOLUTIONS = [
    {
        "id": 1,
        "title": "Two Sum",
        "method_name": "twoSum",
        "difficulty": "Easy",
        "explanation": "Use a hash table to store the value and its index. For each number, check if the complement already exists in the table.",
        "solution_code": "class Solution:\n    def twoSum(self, nums: list[int], target: int) -> list[int]:\n        lookup = {}\n        for i, num in enumerate(nums):\n            if target - num in lookup:\n                return [lookup[target - num], i]\n            lookup[num] = i\n        return []"
    },
    {
        "id": 2,
        "title": "Sum of Two Numbers",
        "method_name": "add",
        "difficulty": "Easy",
        "explanation": "Simple binary addition of two integers.",
        "solution_code": "class Solution:\n    def add(self, a: int, b: int) -> int:\n        return a + b"
    },
    {
        "id": 3,
        "title": "Is Even",
        "method_name": "isEven",
        "difficulty": "Easy",
        "explanation": "Check if the remainder of division by 2 is equal to 0.",
        "solution_code": "class Solution:\n    def isEven(self, n: int) -> bool:\n        return n % 2 == 0"
    },
    {
        "id": 4,
        "title": "Find Maximum",
        "method_name": "findMax",
        "difficulty": "Easy",
        "explanation": "Traverse the list while maintaining the maximum element seen so far.",
        "solution_code": "class Solution:\n    def findMax(self, nums: list[int]) -> int:\n        val = nums[0]\n        for num in nums:\n            if num > val:\n                val = num\n        return val"
    },
    {
        "id": 5,
        "title": "Reverse String",
        "method_name": "reverseString",
        "difficulty": "Easy",
        "explanation": "Slice the string from end to start with a negative step size of 1.",
        "solution_code": "class Solution:\n    def reverseString(self, s: str) -> str:\n        return s[::-1]"
    },
    {
        "id": 6,
        "title": "Fizz Buzz",
        "method_name": "fizzBuzz",
        "difficulty": "Easy",
        "explanation": "Loop from 1 to n. Check if divisible by both 3 and 5, or just 3, or just 5, and append the corresponding string.",
        "solution_code": "class Solution:\n    def fizzBuzz(self, n: int) -> list[str]:\n        res = []\n        for i in range(1, n + 1):\n            if i % 3 == 0 and i % 5 == 0:\n                res.append(\"FizzBuzz\")\n            elif i % 3 == 0:\n                res.append(\"Fizz\")\n            elif i % 5 == 0:\n                res.append(\"Buzz\")\n            else:\n                res.append(str(i))\n        return res"
    }
]
