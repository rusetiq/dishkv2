LEETCODE_PROBLEMS = [
    {
        "id": 1,
        "title": "Contains Duplicate",
        "difficulty": "Easy",
        "function_name": "containsDuplicate",
        "base_points": 100,
        "starter_code": "class Solution:\n    def containsDuplicate(self, nums: List[int]) -> bool:\n        pass",
        "description": "Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.",
        "examples": "Input: nums = [1,2,3,1]\nOutput: true\n\nInput: nums = [1,2,3,4]\nOutput: false",
        "input_variable": "nums",
        "hidden_test_cases": [
            {"input": "[1,2,3,1]", "expected": "True"},
            {"input": "[1,2,3,4]", "expected": "False"},
            {"input": "[1,1,1,3,3,4,3,2,4,2]", "expected": "True"},
            {"input": "[1]", "expected": "False"},
            {"input": "[0,0]", "expected": "True"},
            {"input": "[1,2,3,4,5,6,7,8,9,10]", "expected": "False"},
            {"input": "[-5,-3,-1,-3,0]", "expected": "True"}
        ]
    },
    {
        "id": 2,
        "title": "Invert Binary Tree",
        "difficulty": "Easy",
        "function_name": "invertTree",
        "base_points": 100,
        "starter_code": "class Solution:\n    def invertTree(self, root: List[int]) -> List[int]:\n        pass",
        "description": "Given the root of a binary tree, invert the tree, and return its root as a list representation of level-order traversal.",
        "examples": "Input: root = [4,2,7,1,3,6,9]\nOutput: [4,7,2,9,6,3,1]\n\nInput: root = [2,1,3]\nOutput: [2,3,1]",
        "input_variable": "root",
        "hidden_test_cases": [
            {"input": "[4, 2, 7, 1, 3, 6, 9]", "expected": "[4, 7, 2, 9, 6, 3, 1]"},
            {"input": "[2, 1, 3]", "expected": "[2, 3, 1]"},
            {"input": "[]", "expected": "[]"},
            {"input": "[5]", "expected": "[5]"},
            {"input": "[1, 2, 2]", "expected": "[1, 2, 2]"},
            {"input": "[1, 2, 3, 4, 5, 6, 7]", "expected": "[1, 3, 2, 7, 6, 5, 4]"},
            {"input": "[1, None, 2]", "expected": "[1, 2]"}
        ]
    },
    {
        "id": 3,
        "title": "First Bad Version",
        "difficulty": "Easy",
        "function_name": "firstBadVersion",
        "base_points": 100,
        "starter_code": "class Solution:\n    def firstBadVersion(self, n: int) -> int:\n        pass",
        "description": "You are a product manager and currently leading a team to develop a new product. Unfortunately, the latest version of your product fails the quality check. Since each version is developed based on the previous version, all the versions after a bad version are also bad.\n\nSuppose you have n versions [1, 2, ..., n] and you want to find out the first bad one, which causes all the following ones to be bad.\n\nYou are given an API bool isBadVersion(version) which returns whether version is bad. Implement a function to find the first bad version. You should minimize the number of calls to the API.",
        "examples": "Input: n = 5, bad = 4\nOutput: 4",
        "input_variable": "n",
        "hidden_test_cases": [
            {"input": "5\n4", "expected": "4"},
            {"input": "1\n1", "expected": "1"},
            {"input": "10\n7", "expected": "7"},
            {"input": "2\n2", "expected": "2"},
            {"input": "100\n1", "expected": "1"},
            {"input": "100\n100", "expected": "100"},
            {"input": "20\n13", "expected": "13"}
        ]
    },
    {
        "id": 4,
        "title": "Product of Array Except Self",
        "difficulty": "Medium",
        "function_name": "productExceptSelf",
        "base_points": 100,
        "starter_code": "class Solution:\n    def productExceptSelf(self, nums: List[int]) -> List[int]:\n        pass",
        "description": "Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i].\n\nThe product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer.\n\nYou must write an algorithm that runs in O(n) time and without using the division operation.",
        "examples": "Input: nums = [1,2,3,4]\nOutput: [24,12,8,6]\n\nInput: nums = [-1,1,0,-3,3]\nOutput: [0,0,9,0,0]",
        "input_variable": "nums",
        "hidden_test_cases": [
            {"input": "[1,2,3,4]", "expected": "[24, 12, 8, 6]"},
            {"input": "[-1,1,0,-3,3]", "expected": "[0, 0, 9, 0, 0]"},
            {"input": "[1,1]", "expected": "[1, 1]"},
            {"input": "[2,3,4,5]", "expected": "[60, 40, 30, 24]"},
            {"input": "[-2,3,-4]", "expected": "[-12, 8, -6]"}
        ]
    },
    {
        "id": 5,
        "title": "Two Sum",
        "difficulty": "Easy",
        "function_name": "twoSum",
        "base_points": 100,
        "starter_code": "class Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\n        pass",
        "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.\n\nYou can return the answer in any order.",
        "examples": "Input: nums = [2,7,11,15], target = 9\nOutput: [0,1]\n\nInput: nums = [3,2,4], target = 6\nOutput: [1,2]",
        "input_variable": "nums",
        "hidden_test_cases": [
            {"input": "([2, 7, 11, 15], 9)", "expected": "[0, 1]"},
            {"input": "([3, 2, 4], 6)", "expected": "[1, 2]"},
            {"input": "([3, 3], 6)", "expected": "[0, 1]"},
            {"input": "([1, 5, 8, 3], 11)", "expected": "[2, 3]"}
        ]
    },
    {
        "id": 6,
        "title": "Valid Parentheses",
        "difficulty": "Easy",
        "function_name": "isValid",
        "base_points": 100,
        "starter_code": "class Solution:\n    def isValid(self, s: str) -> bool:\n        pass",
        "description": "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.\n\nAn input string is valid if:\n1. Open brackets must be closed by the same type of brackets.\n2. Open brackets must be closed in the correct order.\n3. Every close bracket has a corresponding open bracket of the same type.",
        "examples": "Input: s = \"()\"\nOutput: true\n\nInput: s = \"()[]{}\"\nOutput: true\n\nInput: s = \"(]\"\nOutput: false",
        "input_variable": "s",
        "hidden_test_cases": [
            {"input": "'()'", "expected": "True"},
            {"input": "'()[]{}'", "expected": "True"},
            {"input": "'(]'", "expected": "False"},
            {"input": "'([])'", "expected": "True"},
            {"input": "']'", "expected": "False"}
        ]
    },
    {
        "id": 7,
        "title": "Best Time to Buy and Sell Stock",
        "difficulty": "Easy",
        "function_name": "maxProfit",
        "base_points": 100,
        "starter_code": "class Solution:\n    def maxProfit(self, prices: List[int]) -> int:\n        pass",
        "description": "You are given an array prices where prices[i] is the price of a given stock on the ith day.\n\nYou want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.\n\nReturn the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.",
        "examples": "Input: prices = [7,1,5,3,6,4]\nOutput: 5\n\nInput: prices = [7,6,4,3,1]\nOutput: 0",
        "input_variable": "prices",
        "hidden_test_cases": [
            {"input": "[7,1,5,3,6,4]", "expected": "5"},
            {"input": "[7,6,4,3,1]", "expected": "0"},
            {"input": "[1,2]", "expected": "1"},
            {"input": "[2,4,1]", "expected": "2"}
        ]
    },
    {
        "id": 8,
        "title": "Valid Palindrome",
        "difficulty": "Easy",
        "function_name": "isPalindrome",
        "base_points": 100,
        "starter_code": "class Solution:\n    def isPalindrome(self, s: str) -> bool:\n        pass",
        "description": "A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.\n\nGiven a string s, return true if it is a palindrome, or false otherwise.",
        "examples": "Input: s = \"A man, a plan, a canal: Panama\"\nOutput: true\n\nInput: s = \"race a car\"\nOutput: false",
        "input_variable": "s",
        "hidden_test_cases": [
            {"input": "'A man, a plan, a canal: Panama'", "expected": "True"},
            {"input": "'race a car'", "expected": "False"},
            {"input": "' '", "expected": "True"},
            {"input": "'ab_a'", "expected": "True"}
        ]
    },
    {
        "id": 9,
        "title": "Valid Anagram",
        "difficulty": "Easy",
        "function_name": "isAnagram",
        "base_points": 100,
        "starter_code": "class Solution:\n    def isAnagram(self, s: str, t: str) -> bool:\n        pass",
        "description": "Given two strings s and t, return true if t is an anagram of s, and false otherwise.\n\nAn Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.",
        "examples": "Input: s = \"anagram\", t = \"nagaram\"\nOutput: true\n\nInput: s = \"rat\", t = \"car\"\nOutput: false",
        "input_variable": "s",
        "hidden_test_cases": [
            {"input": "('anagram', 'nagaram')", "expected": "True"},
            {"input": "('rat', 'car')", "expected": "False"},
            {"input": "('a', 'ab')", "expected": "False"}
        ]
    },
    {
        "id": 10,
        "title": "Binary Search",
        "difficulty": "Easy",
        "function_name": "search",
        "base_points": 100,
        "starter_code": "class Solution:\n    def search(self, nums: List[int], target: int) -> int:\n        pass",
        "description": "Given an array of integers nums which is sorted in ascending order, and an integer target, write a function to search target in nums. If target exists, then return its index. Otherwise, return -1.\n\nYou must write an algorithm with O(log n) runtime complexity.",
        "examples": "Input: nums = [-1,0,3,5,9,12], target = 9\nOutput: 4\n\nInput: nums = [-1,0,3,5,9,12], target = 2\nOutput: -1",
        "input_variable": "nums",
        "hidden_test_cases": [
            {"input": "([-1,0,3,5,9,12], 9)", "expected": "4"},
            {"input": "([-1,0,3,5,9,12], 2)", "expected": "-1"}
        ]
    },
    {
        "id": 11,
        "title": "Maximum Subarray",
        "difficulty": "Medium",
        "function_name": "maxSubArray",
        "base_points": 100,
        "starter_code": "class Solution:\n    def maxSubArray(self, nums: List[int]) -> int:\n        pass",
        "description": "Given an integer array nums, find the subarray with the largest sum, and return its sum.",
        "examples": "Input: nums = [-2,1,-3,4,-1,2,1,-5,4]\nOutput: 6\n\nInput: nums = [1]\nOutput: 1",
        "input_variable": "nums",
        "hidden_test_cases": [
            {"input": "[-2,1,-3,4,-1,2,1,-5,4]", "expected": "6"},
            {"input": "[1]", "expected": "1"},
            {"input": "[5,4,-1,7,8]", "expected": "23"}
        ]
    },
    {
        "id": 12,
        "title": "Climbing Stairs",
        "difficulty": "Easy",
        "function_name": "climbStairs",
        "base_points": 100,
        "starter_code": "class Solution:\n    def climbStairs(self, n: int) -> int:\n        pass",
        "description": "You are climbing a staircase. It takes n steps to reach the top.\n\nEach time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?",
        "examples": "Input: n = 2\nOutput: 2\n\nInput: n = 3\nOutput: 3",
        "input_variable": "n",
        "hidden_test_cases": [
            {"input": "2", "expected": "2"},
            {"input": "3", "expected": "3"},
            {"input": "5", "expected": "8"}
        ]
    },
    {
        "id": 13,
        "title": "3Sum",
        "difficulty": "Medium",
        "function_name": "threeSum",
        "base_points": 100,
        "starter_code": "class Solution:\n    def threeSum(self, nums: List[int]) -> List[List[int]]:\n        pass",
        "description": "Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.\n\nNotice that the solution set must not contain duplicate triplets.",
        "examples": "Input: nums = [-1,0,1,2,-1,-4]\nOutput: [[-1,-1,2],[-1,0,1]]",
        "input_variable": "nums",
        "hidden_test_cases": [
            {"input": "[-1,0,1,2,-1,-4]", "expected": "[[-1, -1, 2], [-1, 0, 1]]"},
            {"input": "[0,1,1]", "expected": "[]"},
            {"input": "[0,0,0]", "expected": "[[0, 0, 0]]"}
        ]
    },
    {
        "id": 14,
        "title": "Container With Most Water",
        "difficulty": "Medium",
        "function_name": "maxArea",
        "base_points": 100,
        "starter_code": "class Solution:\n    def maxArea(self, height: List[int]) -> int:\n        pass",
        "description": "You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).\n\nFind two lines that together with the x-axis form a container, such that the container contains the most water.\n\nReturn the maximum volume of water a container can store.\n\nNotice that you may not slant the container.",
        "examples": "Input: height = [1,8,6,2,5,4,8,3,7]\nOutput: 49\n\nInput: height = [1,1]\nOutput: 1",
        "input_variable": "height",
        "hidden_test_cases": [
            {"input": "[1,8,6,2,5,4,8,3,7]", "expected": "49"},
            {"input": "[1,1]", "expected": "1"}
        ]
    },
    {
        "id": 15,
        "title": "Longest Consecutive Sequence",
        "difficulty": "Medium",
        "function_name": "longestConsecutive",
        "base_points": 100,
        "starter_code": "class Solution:\n    def longestConsecutive(self, nums: List[int]) -> int:\n        pass",
        "description": "Given an unsorted array of integers nums, return the length of the longest consecutive elements sequence.\n\nYou must write an algorithm that runs in O(n) time.",
        "examples": "Input: nums = [100,4,200,1,3,2]\nOutput: 4\nExplanation: The longest consecutive elements sequence is [1, 2, 3, 4]. Therefore its length is 4.",
        "input_variable": "nums",
        "hidden_test_cases": [
            {"input": "[100,4,200,1,3,2]", "expected": "4"},
            {"input": "[0,3,7,2,5,8,4,6,0,1]", "expected": "9"},
            {"input": "[]", "expected": "0"},
            {"input": "[1,2,0,1]", "expected": "3"}
        ]
    },
    {
        "id": 16,
        "title": "Trapping Rain Water",
        "difficulty": "Hard",
        "function_name": "trap",
        "base_points": 150,
        "starter_code": "class Solution:\n    def trap(self, height: List[int]) -> int:\n        pass",
        "description": "Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.",
        "examples": "Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]\nOutput: 6",
        "input_variable": "height",
        "hidden_test_cases": [
            {"input": "[0,1,0,2,1,0,1,3,2,1,2,1]", "expected": "6"},
            {"input": "[4,2,0,3,2,5]", "expected": "9"},
            {"input": "[]", "expected": "0"},
            {"input": "[3]", "expected": "0"},
            {"input": "[2,0,2]", "expected": "2"}
        ]
    }
]

BONUS_QUESTIONS = [
    {
        "title": "Bonus Challenge 1: Find the Secret Key",
        "description": "Submit an integer x such that the function outputs 'SUCCESS'. The script checks if x^2 - 12x + 35 = 0 and x > 6.",
        "starter_code": "try:\n    val = int(input().strip())\n    if val**2 - 12*val + 35 == 0 and val > 6:\n        print(\"SUCCESS\")\n    else:\n        print(\"TRY AGAIN\")\nexcept Exception:\n    print(\"INVALID INPUT\")",
        "expected_output": "SUCCESS",
        "input_type_hint": "An integer x",
        "order": 1,
        "duration_minutes": 15
    },
    {
        "title": "Bonus Challenge 2: Word Play",
        "description": "Find a word containing exactly three 'a's and of length 7 that prints 'FOUND'.",
        "starter_code": "word = input().strip().lower()\nif len(word) == 7 and word.count('a') == 3:\n    print(\"FOUND\")\nelse:\n    print(\"NOT FOUND\")",
        "expected_output": "FOUND",
        "input_type_hint": "A 7-letter word",
        "order": 2,
        "duration_minutes": 15
    },
    {
        "title": "Bonus Challenge 3: Fibonacci Puzzle",
        "description": "Provide an integer input n such that the n-th Fibonacci number is 55. The Fibonacci sequence starts with F(0)=0, F(1)=1.",
        "starter_code": "def fib(n):\n    if n <= 0: return 0\n    if n == 1: return 1\n    a, b = 0, 1\n    for _ in range(2, n + 1):\n        a, b = b, a + b\n    return b\n\ntry:\n    val = int(input().strip())\n    if fib(val) == 55:\n        print(\"MATCH\")\n    else:\n        print(\"NOMATCH\")\nexcept Exception:\n    print(\"ERROR\")",
        "expected_output": "MATCH",
        "input_type_hint": "Integer n",
        "order": 3,
        "duration_minutes": 15
    }
]

