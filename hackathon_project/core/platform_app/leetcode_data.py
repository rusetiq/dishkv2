LEETCODE_PROBLEMS = [
    {
        "id": 1,
        "title": "Median-Adjusted Mean",
        "difficulty": "Easy",
        "function_name": "median_adjusted_mean",
        "base_points": 100,
        "starter_code": "class Solution:\n    def median_adjusted_mean(self, data: list[int]) -> int:\n        pass",
        "description": "Calculate the mean of an array of integers after excluding the single minimum and single maximum values. If duplicate smallest or largest values exist, only one instance of each is removed. The final result should be an integer derived through floor division. Assume the array contains at least three elements.",
        "examples": "Input: data = [1, 2, 3, 4, 5]\nOutput: 3\nExplanation: Min is 1, max is 5. Remaining elements: [2, 3, 4]. Mean is (2+3+4)//3 = 3.\n\nInput: data = [1, 1, 3, 5, 5]\nOutput: 3\nExplanation: Min is 1, max is 5. Removing one instance of min and one instance of max leaves: [1, 3, 5]. Mean is (1+3+5)//3 = 3.",
        "input_variable": "data",
        "hidden_test_cases": [
            {"input": "[1, 2, 3, 4, 5]", "expected": "3"},
            {"input": "[1, 1, 3, 5, 5]", "expected": "3"},
            {"input": "[10, 20, 30]", "expected": "20"},
            {"input": "[-5, 0, 5, 10]", "expected": "2"},
            {"input": "[2, 2, 2]", "expected": "2"},
            {"input": "[1, 10, 100, 1000]", "expected": "55"}
        ]
    },
    {
        "id": 2,
        "title": "Unique Element Verification",
        "difficulty": "Easy",
        "function_name": "verify_uniqueness",
        "base_points": 100,
        "starter_code": "class Solution:\n    def verify_uniqueness(self, numbers: list[int]) -> bool:\n        pass",
        "description": "Given an array of numbers, determine if any value appears at least twice within the array. Return True if duplicates exist, and False if every element is distinct.",
        "examples": "Input: numbers = [1, 2, 3, 1]\nOutput: True\n\nInput: numbers = [1, 2, 3, 4]\nOutput: False",
        "input_variable": "numbers",
        "hidden_test_cases": [
            {"input": "[1, 2, 3, 1]", "expected": "True"},
            {"input": "[1, 2, 3, 4]", "expected": "False"},
            {"input": "[]", "expected": "False"},
            {"input": "[5]", "expected": "False"},
            {"input": "[-1, -1]", "expected": "True"},
            {"input": "[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]", "expected": "False"}
        ]
    },
    {
        "id": 3,
        "title": "Three Sum",
        "difficulty": "Easy",
        "function_name": "threeSum",
        "base_points": 100,
        "starter_code": "class Solution:\n    def threeSum(self, nums: list[int], target: int) -> list[int]:\n        pass",
        "description": "Given an array of integers nums and an integer target, return indices of the three numbers such that they add up to target.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.\n\nReturn the indices sorted in ascending order.",
        "examples": "Input: nums = [2, 7, 11, 15], target = 20\nOutput: [0, 1, 2]\nExplanation: nums[0] + nums[1] + nums[2] = 2 + 7 + 11 = 20.\n\nInput: nums = [1, 2, 3, 4, 5], target = 12\nOutput: [2, 3, 4]\nExplanation: nums[2] + nums[3] + nums[4] = 3 + 4 + 5 = 12.",
        "input_variable": "nums",
        "hidden_test_cases": [
            {"input": "([2, 7, 11, 15], 20)", "expected": "[0, 1, 2]"},
            {"input": "([1, 2, 3, 4, 5], 12)", "expected": "[2, 3, 4]"},
            {"input": "([10, 20, 35, 40, 50], 85)", "expected": "[0, 2, 3]"},
            {"input": "([1, 3, 9, 27, 81], 93)", "expected": "[1, 2, 4]"},
            {"input": "([-1, 0, 1, 2], 2)", "expected": "[0, 2, 3]"}
        ]
    },
    {
        "id": 4,
        "title": "Defective Product Search",
        "difficulty": "Easy",
        "function_name": "find_first_defective",
        "base_points": 100,
        "starter_code": "class Solution:\n    def find_first_defective(self, n: int) -> int:\n        pass",
        "description": "You are a quality control manager inspecting a sequence of products. All subsequent products after the first defective one are also defective. Given a total number of products n, and a check function is_defective(version), find the number of the very first defective product. Minimize the number of calls to is_defective.",
        "examples": "Input: n = 5, defect = 4\nOutput: 4\nExplanation: is_defective(1)->False, is_defective(2)->False, is_defective(3)->False, is_defective(4)->True, is_defective(5)->True. First defective version is 4.",
        "input_variable": "n",
        "hidden_test_cases": [
            {"input": "5\n4", "expected": "4"},
            {"input": "1\n1", "expected": "1"},
            {"input": "10\n7", "expected": "7"},
            {"input": "100\n42", "expected": "42"},
            {"input": "2\n2", "expected": "2"}
        ]
    },
    {
        "id": 5,
        "title": "Arithmetic Coefficient Pyramid",
        "difficulty": "Easy",
        "function_name": "generate_pyramid",
        "base_points": 100,
        "starter_code": "class Solution:\n    def generate_pyramid(self, num_rows: int) -> list[list[int]]:\n        pass",
        "description": "Generate the first num_rows of Pascal's triangle. In Pascal's triangle, each number is the sum of the two numbers directly above it.",
        "examples": "Input: num_rows = 5\nOutput: [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]",
        "input_variable": "num_rows",
        "hidden_test_cases": [
            {"input": "1", "expected": "[[1]]"},
            {"input": "2", "expected": "[[1], [1, 1]]"},
            {"input": "5", "expected": "[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]"},
            {"input": "0", "expected": "[]"},
            {"input": "6", "expected": "[[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1], [1, 5, 10, 10, 5, 1]]"}
        ]
    },
    {
        "id": 6,
        "title": "Balanced Character Set",
        "difficulty": "Easy",
        "function_name": "is_balanced_by_removal",
        "base_points": 100,
        "starter_code": "class Solution:\n    def is_balanced_by_removal(self, s: str) -> bool:\n        pass",
        "description": "Given a string s, determine if it is possible to make the frequency of every character in s equal by deleting exactly one character. The final string must not be empty.",
        "examples": "Input: s = \"abcc\"\nOutput: True\nExplanation: Deleting one 'c' yields \"abc\", where every character appears once.\n\nInput: s = \"aabbcd\"\nOutput: False\nExplanation: We must delete exactly one character. Deleting 'a' yields \"abbcd\" (not equal), etc.",
        "input_variable": "s",
        "hidden_test_cases": [
            {"input": "'abcc'", "expected": "True"},
            {"input": "'aabbcd'", "expected": "False"},
            {"input": "'a'", "expected": "False"},
            {"input": "'ab'", "expected": "True"},
            {"input": "'abc'", "expected": "True"},
            {"input": "'aabbcc'", "expected": "False"},
            {"input": "'aaabbbcccd'", "expected": "True"},
            {"input": "'aaabbbcc'", "expected": "True"}
        ]
    },
    {
        "id": 7,
        "title": "Continental Count",
        "difficulty": "Medium",
        "function_name": "count_continents",
        "base_points": 150,
        "starter_code": "class Solution:\n    def count_continents(self, grid: list[list[str]]) -> int:\n        pass",
        "description": "Given an m x n 2D binary grid ('1' for land, '0' for water), return the total number of distinct islands. An island is formed by connected land cells horizontally or vertically. All four edges of the map are considered water.",
        "examples": "Input: grid = [\n  [\"1\",\"1\",\"1\",\"1\",\"0\"],\n  [\"1\",\"1\",\"0\",\"1\",\"0\"],\n  [\"1\",\"1\",\"0\",\"0\",\"0\"],\n  [\"0\",\"0\",\"0\",\"0\",\"0\"]\n]\nOutput: 1",
        "input_variable": "grid",
        "hidden_test_cases": [
            {"input": "[[\"1\",\"1\",\"1\",\"1\",\"0\"],[\"1\",\"1\",\"0\",\"1\",\"0\"],[\"1\",\"1\",\"0\",\"0\",\"0\"],[\"0\",\"0\",\"0\",\"0\",\"0\"]]", "expected": "1"},
            {"input": "[[\"1\",\"1\",\"0\",\"0\",\"0\"],[\"1\",\"1\",\"0\",\"0\",\"0\"],[\"0\",\"0\",\"1\",\"0\",\"0\"],[\"0\",\"0\",\"0\",\"1\",\"1\"]]", "expected": "3"},
            {"input": "[[\"0\",\"0\",\"0\"],[\"0\",\"0\",\"0\"]]", "expected": "0"},
            {"input": "[[\"1\"]]", "expected": "1"}
        ]
    },
    {
        "id": 8,
        "title": "Minimum Weight Traverse",
        "difficulty": "Medium",
        "function_name": "minimum_traverse_weight",
        "base_points": 150,
        "starter_code": "class Solution:\n    def minimum_traverse_weight(self, triangle: list[list[int]]) -> int:\n        pass",
        "description": "Navigate a triangular grid (cavern) where every step leads deeper. Starting from the apex, find the path downward to minimize the total accumulated weight (value) carried to the floor (the last row). At each level, you can only move to the adjacent numbers in the row directly below.",
        "examples": "Input: triangle = [[2],[3,4],[6,5,7],[4,1,8,3]]\nOutput: 11\nExplanation: Apex (2) -> 3 -> 5 -> 1. Total: 2 + 3 + 5 + 1 = 11.",
        "input_variable": "triangle",
        "hidden_test_cases": [
            {"input": "[[2],[3,4],[6,5,7],[4,1,8,3]]", "expected": "11"},
            {"input": "[[-10]]", "expected": "-10"},
            {"input": "[[1],[2,3]]", "expected": "3"},
            {"input": "[[2],[8,2],[1,5,3]]", "expected": "7"}
        ]
    },
    {
        "id": 9,
        "title": "Max Adjacent Difference",
        "difficulty": "Medium",
        "function_name": "find_max_difference",
        "base_points": 150,
        "starter_code": "class Solution:\n    def find_max_difference(self, nums: list[int]) -> int:\n        pass",
        "description": "Given an unsorted array of non-negative integers, find the maximum difference between successive elements in its sorted form. If the array contains less than two elements, the difference is 0.",
        "examples": "Input: nums = [3, 6, 9, 1]\nOutput: 3\nExplanation: Sorted form is [1, 3, 6, 9], maximum successive difference is between 3 and 6, which is 3.",
        "input_variable": "nums",
        "hidden_test_cases": [
            {"input": "[3, 6, 9, 1]", "expected": "3"},
            {"input": "[10]", "expected": "0"},
            {"input": "[]", "expected": "0"},
            {"input": "[1, 10]", "expected": "9"},
            {"input": "[1, 1, 1, 1]", "expected": "0"},
            {"input": "[15, 12, 2, 8, 10]", "expected": "6"}
        ]
    },
    {
        "id": 10,
        "title": "Light State Toggles",
        "difficulty": "Medium",
        "function_name": "count_on_bulbs",
        "base_points": 150,
        "starter_code": "class Solution:\n    def count_on_bulbs(self, n: int) -> int:\n        pass",
        "description": "There are n light bulbs, initially all off. You perform n rounds of switching. In round i, you toggle every i-th bulb (i, 2i, 3i, ...). After n rounds, return the number of bulbs that are on.",
        "examples": "Input: n = 3\nOutput: 1\nExplanation: Initially [off, off, off]. Round 1: [on, on, on]. Round 2: [on, off, on]. Round 3: [on, off, off]. Only the first bulb is on.",
        "input_variable": "n",
        "hidden_test_cases": [
            {"input": "3", "expected": "1"},
            {"input": "0", "expected": "0"},
            {"input": "1", "expected": "1"},
            {"input": "4", "expected": "2"},
            {"input": "10", "expected": "3"},
            {"input": "100", "expected": "10"}
        ]
    },
    {
        "id": 11,
        "title": "Jump Game: Reaching the End",
        "difficulty": "Medium",
        "function_name": "can_reach_end",
        "base_points": 150,
        "starter_code": "class Solution:\n    def can_reach_end(self, nums: list[int]) -> bool:\n        pass",
        "description": "You are given an array of non-negative integers nums. Each element nums[i] represents the maximum jump length from that position. Determine if you can reach the last index starting from the first index (index 0).",
        "examples": "Input: nums = [2, 3, 1, 1, 4]\nOutput: True\n\nInput: nums = [3, 2, 1, 0, 4]\nOutput: False",
        "input_variable": "nums",
        "hidden_test_cases": [
            {"input": "[2, 3, 1, 1, 4]", "expected": "True"},
            {"input": "[3, 2, 1, 0, 4]", "expected": "False"},
            {"input": "[0]", "expected": "True"},
            {"input": "[2, 0, 0]", "expected": "True"},
            {"input": "[1, 0, 1]", "expected": "False"}
        ]
    },
    {
        "id": 12,
        "title": "Nested Containers",
        "difficulty": "Hard",
        "function_name": "max_nested_envelopes",
        "base_points": 200,
        "starter_code": "class Solution:\n    def max_nested_envelopes(self, envelopes: list[list[int]]) -> int:\n        pass",
        "description": "You are given a set of envelopes, where envelopes[i] = [width, height] is the dimensions of the i-th envelope. An envelope can fit inside another if both its width and height are strictly smaller than the other envelope's width and height. Find the maximum number of envelopes you can nest inside one another.",
        "examples": "Input: envelopes = [[5,4],[6,4],[6,7],[2,3]]\nOutput: 3\nExplanation: [2,3] -> [5,4] -> [6,7].",
        "input_variable": "envelopes",
        "hidden_test_cases": [
            {"input": "[[5,4],[6,4],[6,7],[2,3]]", "expected": "3"},
            {"input": "[[1,1],[1,1],[1,1]]", "expected": "1"},
            {"input": "[[4,5],[4,6],[6,7],[2,3],[1,1]]", "expected": "4"},
            {"input": "[[1,3],[3,5],[5,7],[2,2],[8,9]]", "expected": "4"}
        ]
    },
    {
        "id": 13,
        "title": "Hero's Survival Path",
        "difficulty": "Hard",
        "function_name": "min_starting_health",
        "base_points": 200,
        "starter_code": "class Solution:\n    def min_starting_health(self, dungeon: list[list[int]]) -> int:\n        pass",
        "description": "A knight starts at the top-left corner of a dungeon grid and must reach the bottom-right corner. The grid cells contain positive, negative, or zero integer values representing health change. The knight must maintain a health value greater than zero at all times. Find the minimum initial health the knight must start with.",
        "examples": "Input: dungeon = [[-2,-3,3],[-5,-10,1],[10,30,-5]]\nOutput: 7\nExplanation: Path: right -> right -> down -> down. Health at each step: 7 -> 5 -> 2 -> 5 -> 6 -> 1.",
        "input_variable": "dungeon",
        "hidden_test_cases": [
            {"input": "[[-2,-3,3],[-5,-10,1],[10,30,-5]]", "expected": "7"},
            {"input": "[[0]]", "expected": "1"},
            {"input": "[[10]]", "expected": "1"},
            {"input": "[[-5]]", "expected": "6"},
            {"input": "[[1,-3,3],[0,-2,0],[-3,-3,-3]]", "expected": "3"}
        ]
    },
    {
        "id": 14,
        "title": "Optimal Balloon Popping",
        "difficulty": "Hard",
        "function_name": "max_coins_from_bursts",
        "base_points": 200,
        "starter_code": "class Solution:\n    def max_coins_from_bursts(self, nums: list[int]) -> int:\n        pass",
        "description": "Given n balloons, indexed from 0 to n-1. Each balloon has a number on it. If you burst balloon i, you get nums[i-1] * nums[i] * nums[i+1] coins. Find the maximum coins you can collect by bursting the balloons in an optimal order.",
        "examples": "Input: nums = [3, 1, 5, 8]\nOutput: 167\nExplanation: nums = [3,1,5,8] -> [3,5,8] -> [3,8] -> [8] -> []\nCoins: 3*1*5 + 3*5*8 + 1*3*8 + 1*8*1 = 15 + 120 + 24 + 8 = 167.",
        "input_variable": "nums",
        "hidden_test_cases": [
            {"input": "[3, 1, 5, 8]", "expected": "167"},
            {"input": "[1, 5]", "expected": "10"},
            {"input": "[8]", "expected": "8"},
            {"input": "[3, 5]", "expected": "20"},
            {"input": "[7, 9, 8]", "expected": "568"}
        ]
    },
    {
        "id": 15,
        "title": "Fair Distribution Score",
        "difficulty": "Hard",
        "function_name": "min_candies_required",
        "base_points": 200,
        "starter_code": "class Solution:\n    def min_candies_required(self, ratings: list[int]) -> int:\n        pass",
        "description": "There are n children standing in a line, each with a rating score. You must give each child at least one candy. Children with a higher rating must receive more candies than their adjacent neighbors. Calculate the minimum number of candies required.",
        "examples": "Input: ratings = [1, 0, 2]\nOutput: 5\nExplanation: You can allocate to the first, second and third child with 2, 1, 2 candies respectively.",
        "input_variable": "ratings",
        "hidden_test_cases": [
            {"input": "[1, 0, 2]", "expected": "5"},
            {"input": "[1, 2, 2]", "expected": "4"},
            {"input": "[1, 2, 3, 4, 5]", "expected": "15"},
            {"input": "[5, 4, 3, 2, 1]", "expected": "15"},
            {"input": "[1, 3, 2, 1, 4, 3, 2, 1]", "expected": "17"}
        ]
    }
]

BONUS_QUESTIONS = [
    {
        "title": "Bonus Challenge 1: Reversing and Doubling",
        "description": "Challenge: Given the following Python function and the target Output, determine the list of integers Input that would produce this result.\n\nclass Solution:\n    def reverse_and_double(self, nums: list[int]) -> list[int]:\n        reversed_nums = nums[::-1]\n        doubled_nums = [x * 2 for x in reversed_nums]\n        return doubled_nums\n\nTarget Output: [10, 8, 6, 4]\nInput (nums): ?",
        "starter_code": "import ast\ntry:\n    nums = ast.literal_eval(input().strip())\n    if isinstance(nums, list) and all(isinstance(x, int) for x in nums):\n        reversed_nums = nums[::-1]\n        doubled_nums = [x * 2 for x in reversed_nums]\n        if doubled_nums == [10, 8, 6, 4]:\n            print(\"SUCCESS\")\n        else:\n            print(\"TRY AGAIN\")\n    else:\n        print(\"INVALID INPUT\")\nexcept Exception:\n    print(\"ERROR\")",
        "expected_output": "SUCCESS",
        "input_type_hint": "A list of integers, e.g. [2, 3, 4, 5]",
        "order": 1,
        "duration_minutes": 15
    },
    {
        "title": "Bonus Challenge 2: Character Shift Cipher",
        "description": "Challenge: Given the following Python function and the target Output, find the string Input that generates this result. The function shifts each character's ASCII value by 1.\n\nclass Solution:\n    def character_shift(self, s: str) -> str:\n        shifted_chars = [chr(ord(c) + 1) for c in s]\n        return \"\".join(shifted_chars)\n\nTarget Output: 'ifmmp'\nInput (s): ?",
        "starter_code": "try:\n    s = input().strip()\n    if (s.startswith(\"'\") and s.endswith(\"'\")) or (s.startswith('\"') and s.endswith('\"')):\n        import ast\n        s = ast.literal_eval(s)\n    shifted_chars = [chr(ord(c) + 1) for c in s]\n    res = \"\".join(shifted_chars)\n    if res == 'ifmmp':\n        print(\"SUCCESS\")\n    else:\n        print(\"TRY AGAIN\")\nexcept Exception:\n    print(\"ERROR\")",
        "expected_output": "SUCCESS",
        "input_type_hint": "A string, e.g. hello",
        "order": 2,
        "duration_minutes": 15
    },
    {
        "title": "Bonus Challenge 3: Sum of Evens and Odds",
        "description": "Challenge: Given the following Python function and the target Output, find the list of integers Input that results in the given two-element list.\n\nclass Solution:\n    def sum_evens_and_odds(self, numbers: list[int]) -> list[int]:\n        even_sum = 0\n        odd_sum = 0\n        for num in numbers:\n            if num % 2 == 0:\n                even_sum += num\n            else:\n                odd_sum += num\n        return [even_sum, odd_sum]\n\nTarget Output: [12, 15]\nInput (numbers): ?",
        "starter_code": "import ast\ntry:\n    numbers = ast.literal_eval(input().strip())\n    if isinstance(numbers, list) and all(isinstance(x, int) for x in numbers):\n        even_sum = 0\n        odd_sum = 0\n        for num in numbers:\n            if num % 2 == 0:\n                even_sum += num\n            else:\n                odd_sum += num\n        res = [even_sum, odd_sum]\n        if res == [12, 15]:\n            print(\"SUCCESS\")\n        else:\n            print(\"TRY AGAIN\")\n    else:\n        print(\"INVALID INPUT\")\nexcept Exception:\n    print(\"ERROR\")",
        "expected_output": "SUCCESS",
        "input_type_hint": "A list of integers, e.g. [12, 15]",
        "order": 3,
        "duration_minutes": 15
    }
]
