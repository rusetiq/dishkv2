LEETCODE_PROBLEMS = [
    {
        "id": 1,
        "title": "Median-Adjusted Mean",
        "difficulty": "Easy",
        "function_name": "median_adjusted_mean",
        "base_points": 150,
        "starter_code": "class Solution:\n    def median_adjusted_mean(self, data: list[int]) -> int:\n        pass",
        "description": "Calculate the mean of an array of integers after excluding the single minimum and single maximum values. If duplicate smallest or largest values exist, only one instance of each is removed. For example, in the array [1, 1, 3, 5, 5], the minimum value is 1 and the maximum value is 5. We remove exactly one instance of 1 and one instance of 5, leaving [1, 3, 5]. The final result must be an integer derived through floor division (rounded down to the nearest integer). You can assume the input array will always contain at least three elements.",
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
        "base_points": 150,
        "starter_code": "class Solution:\n    def verify_uniqueness(self, numbers: list[int]) -> bool:\n        pass",
        "description": "Given an array of numbers, determine if any value appears at least twice within the array. Your function should return True if duplicate elements exist, and False if every element in the array is completely distinct and unique. For example, if the input is [1, 2, 3, 1], the value 1 appears twice, so the output is True. If the input is [1, 2, 3, 4], all elements are unique, so the output is False. An empty array or an array with one element should return False.",
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
        "base_points": 150,
        "starter_code": "class Solution:\n    def threeSum(self, nums: list[int], target: int) -> list[int]:\n        pass",
        "description": "Given an array of integers named nums and a target integer target, return the indices of the three numbers in the array that add up to target. You may assume that each input has exactly one solution. You are not allowed to use the same element twice. The indices returned in the final list must be sorted in ascending order. For example, if the array is [2, 7, 11, 15] and target is 20, the elements 2, 7, and 11 add up to 20, so we return their indices [0, 1, 2].",
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
        "base_points": 150,
        "starter_code": "class Solution:\n    def find_first_defective(self, n: int) -> int:\n        pass",
        "description": "You are a quality control manager inspecting a sequence of products numbered 1 to n. All subsequent products after the first defective product are also defective. Given the total number of products n and a helper function is_defective(version) which returns True if the product at that version is defective and False otherwise, find the index of the first defective product. You should minimize the number of calls to the is_defective function using an efficient search strategy like binary search.",
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
        "base_points": 150,
        "starter_code": "class Solution:\n    def generate_pyramid(self, num_rows: int) -> list[list[int]]:\n        pass",
        "description": "Generate the first num_rows of Pascal's triangle. Pascal's triangle is a triangular array of the binomial coefficients. The triangle starts with a single number 1 at the top (row 0). Each subsequent row is constructed by placing 1 at the beginning and end, and calculating the inner numbers by adding the two adjacent numbers directly above them in the previous row. For example, row 2 is [1, 2, 1], and row 3 is [1, 3, 3, 1], where 3 is the sum of 1 and 2 from row 2.",
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
        "base_points": 150,
        "starter_code": "class Solution:\n    def is_balanced_by_removal(self, s: str) -> bool:\n        pass",
        "description": "Given a string s, determine if it is possible to make the frequency of every character in s equal by deleting exactly one character. The resulting string must not be empty. For example, the string 'abcc' is valid because deleting one 'c' yields 'abc', where all characters have a frequency of 1. The string 'aabbcd' is invalid because no single deletion can make all remaining character frequencies equal. If all characters already have the same frequency, deleting one character must still result in equal frequencies.",
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
            {"input": "'aaabbbcc'", "expected": "False"}
        ]
    },
    {
        "id": 7,
        "title": "Number of Islands",
        "difficulty": "Medium",
        "function_name": "numIslands",
        "base_points": 300,
        "starter_code": "class Solution:\n    def numIslands(self, grid: list[list[str]]) -> int:\n        pass",
        "description": "Given an m x n 2D binary grid representing a map of '1's (land) and '0's (water), return the total number of islands. An island is surrounded by water and is formed by connecting adjacent land cells horizontally or vertically. Diagonal connections do not count. You can assume that all four outer edges of the grid are surrounded by water. To count the islands, you can traverse the grid and use depth first search or breadth first search to visit and mark all connected land cells for each island.",
        "examples": "Input: grid = [\n  [\"1\",\"1\",\"1\",\"1\",\"0\"],\n  [\"1\",\"1\",\"0\",\"1\",\"0\"],\n  [\"1\",\"1\",\"0\",\"0\",\"0\"],\n  [\"0\",\"0\",\"0\",\"0\",\"0\"]\n]\nOutput: 1\nExplanation: All '1's are connected horizontally and vertically to form a single island.\n\nInput: grid = [\n  [\"1\",\"1\",\"0\",\"0\",\"0\"],\n  [\"1\",\"1\",\"0\",\"0\",\"0\"],\n  [\"0\",\"0\",\"1\",\"0\",\"0\"],\n  [\"0\",\"0\",\"0\",\"1\",\"1\"]\n]\nOutput: 3\nExplanation: The grid has 3 separate islands. One 2x2 island in the top-left, one single-cell island in the center, and one 1x2 island in the bottom-right.",
        "input_variable": "grid",
        "hidden_test_cases": [
            {"input": "[[\"1\",\"1\",\"1\",\"1\",\"0\"],[\"1\",\"1\",\"0\",\"1\",\"0\"],[\"1\",\"1\",\"0\",\"0\",\"0\"],[\"0\",\"0\",\"0\",\"0\",\"0\"]]", "expected": "1"},
            {"input": "[[\"1\",\"1\",\"0\",\"0\",\"0\"],[\"1\",\"1\",\"0\",\"0\",\"0\"],[\"0\",\"0\",\"1\",\"0\",\"0\"],[\"0\",\"0\",\"0\",\"1\",\"1\"]]", "expected": "3"},
            {"input": "[[\"0\",\"0\",\"0\"],[\"0\",\"0\",\"0\"]]", "expected": "0"},
            {"input": "[[\"1\"]]", "expected": "1"},
            {"input": "[[\"1\",\"0\",\"1\"],[\"0\",\"1\",\"0\"],[\"1\",\"0\",\"1\"]]", "expected": "5"}
        ]
    },
    {
        "id": 8,
        "title": "Descent to the Deep",
        "difficulty": "Medium",
        "function_name": "minimumTotal",
        "base_points": 300,
        "starter_code": "class Solution:\n    def minimumTotal(self, triangle: list[list[int]]) -> int:\n        pass",
        "description": "Navigate a triangular cavern represented by a 2D list of integers. Starting from the top (apex), choose a path downward to minimize the total sum of numbers along the path to the bottom. At each step, if you are at index c in the current row, you can only move to either index c or index c + 1 in the row directly below. For example, in the triangle [[2], [3, 4], [6, 5, 7]], from 2 you can move to 3 or 4, and from 3 you can move to 6 or 5.",
        "examples": "Input: triangle = [[2],[3,4],[6,5,7],[4,1,8,3]]\nOutput: 11\nExplanation: The path with the minimum sum of weights is: 2 -> 3 -> 5 -> 1. Total weight: 2 + 3 + 5 + 1 = 11.",
        "input_variable": "triangle",
        "hidden_test_cases": [
            {"input": "[[2],[3,4],[6,5,7],[4,1,8,3]]", "expected": "11"},
            {"input": "[[-10]]", "expected": "-10"},
            {"input": "[[1],[2,3]]", "expected": "3"},
            {"input": "[[2],[8,2],[1,5,3]]", "expected": "7"},
            {"input": "[[-1],[2,3],[1,-1,-3]]", "expected": "-1"}
        ]
    },
    {
        "id": 9,
        "title": "Alternating End-Pick Game",
        "difficulty": "Medium",
        "function_name": "predictTheWinner",
        "base_points": 300,
        "starter_code": "class Solution:\n    def predictTheWinner(self, nums: list[int]) -> bool:\n        pass",
        "description": "Two players are playing a turn-based strategy game using an array of integers named nums. Both players start with a score of 0, and Player 1 always takes the first turn. On each turn, a player can choose exactly one number, but only from either the very beginning or the very end of the current array. Once chosen, that number is added to the player's score and removed from the array. The game ends when no numbers are left. If Player 1's final score is greater than or equal to Player 2's final score, Player 1 wins. Assuming both players play perfectly using optimal strategies, return True if Player 1 is guaranteed to win, and False otherwise.",
        "examples": "Input: nums = [1, 5, 2]\nOutput: False\nExplanation: Player 1 can choose 1 or 2. If P1 chooses 2, remaining is [1, 5] and P2 chooses 5 to win. If P1 chooses 1, remaining is [5, 2] and P2 chooses 5 to win.\n\nInput: nums = [1, 5, 233, 7]\nOutput: True\nExplanation: Player 1 chooses 1, leaving [5, 233, 7]. Player 2 must choose 5 or 7. Whichever they choose, Player 1 can next choose 233 and win.",
        "input_variable": "nums",
        "hidden_test_cases": [
            {"input": "[1, 5, 2]", "expected": "False"},
            {"input": "[1, 5, 233, 7]", "expected": "True"},
            {"input": "[0]", "expected": "True"},
            {"input": "[1, 2, 4, 3]", "expected": "True"},
            {"input": "[10, 15, 20, 5]", "expected": "True"},
            {"input": "[1, 1, 1]", "expected": "True"}
        ]
    },
    {
        "id": 10,
        "title": "Word Finder",
        "difficulty": "Medium",
        "function_name": "findLongestWord",
        "base_points": 300,
        "starter_code": "class Solution:\n    def findLongestWord(self, s: str, dictionary: list[str]) -> str:\n        pass",
        "description": "You are given a text string s and a list of target strings called dictionary. Your goal is to find the longest word from the dictionary that can be formed using the characters of s in their original relative order. This means the word must be a subsequence of s (characters do not need to be consecutive, but their order must be preserved). If there are multiple words that tie for the longest length, return the word that comes first alphabetically (lexicographically smallest). If no words from the dictionary can be formed, return an empty string.",
        "examples": "Input: s = \"abpcplea\", dictionary = [\"ale\",\"apple\",\"monkey\",\"plea\"]\nOutput: \"apple\"\nExplanation: \"apple\" is a subsequence of \"abpcplea\" and is the longest matching word.\n\nInput: s = \"abpcplea\", dictionary = [\"a\",\"b\",\"c\"]\nOutput: \"a\"\nExplanation: \"a\", \"b\", and \"c\" all match. They all have length 1. \"a\" is lexicographically the smallest, so it is returned.",
        "input_variable": "s",
        "hidden_test_cases": [
            {"input": "(\"abpcplea\", [\"ale\",\"apple\",\"monkey\",\"plea\"])", "expected": "apple"},
            {"input": "(\"abpcplea\", [\"a\",\"b\",\"c\"])", "expected": "a"},
            {"input": "(\"aewfafwifgecaxtgr\", [\"apple\",\"ewaf\",\"awefawfwaf\",\"aefqawfbftgg\",\"abcdefa\"])", "expected": "ewaf"},
            {"input": "(\"bab\", [\"ba\",\"ab\",\"a\",\"b\"])", "expected": "ab"},
            {"input": "(\"xyz\", [\"abc\",\"def\"])", "expected": ""}
        ]
    },
    {
        "id": 11,
        "title": "Zig-Zag Array Reordering",
        "difficulty": "Medium",
        "function_name": "wiggleSort",
        "base_points": 300,
        "starter_code": "class Solution:\n    def wiggleSort(self, nums: list[int]) -> list[int]:\n        pass",
        "description": "Your task is to rearrange the numbers in the array so that they follow a strict up and down zig-zag pattern. Specifically, after rearranging, the elements must satisfy the condition: nums[0] < nums[1] > nums[2] < nums[3]... To ensure a unique and deterministic answer, you must construct the rearranged array as follows: first, sort the input array in ascending order. Second, divide it into two halves: the first half containing the smaller elements of size (n + 1) // 2, and the second half containing the remaining larger elements. Third, reverse both halves. Fourth, interleave them by taking the first element from the reversed smaller half, then the first from the reversed larger half, then the second from the reversed smaller half, and so on. Return the final rearranged array.",
        "examples": "Input: nums = [1, 5, 1, 1, 6, 4]\nOutput: [1, 6, 1, 5, 1, 4]\nExplanation: Sorted: [1,1,1,4,5,6]. Smaller half reversed: [1,1,1]. Larger half reversed: [6,5,4]. Interleaving them yields [1,6,1,5,1,4].\n\nInput: nums = [1, 3, 2, 2, 3, 1]\nOutput: [2, 3, 1, 3, 1, 2]\nExplanation: Sorted: [1,1,2,2,3,3]. Smaller half reversed: [2,1,1]. Larger half reversed: [3,3,2]. Interleaving yields [2,3,1,3,1,2].",
        "input_variable": "nums",
        "hidden_test_cases": [
            {"input": "[1, 5, 1, 1, 6, 4]", "expected": "[1, 6, 1, 5, 1, 4]"},
            {"input": "[1, 3, 2, 2, 3, 1]", "expected": "[2, 3, 1, 3, 1, 2]"},
            {"input": "[1, 2, 3]", "expected": "[2, 3, 1]"},
            {"input": "[4, 5, 5, 6]", "expected": "[5, 6, 4, 5]"}
        ]
    },
    {
        "id": 12,
        "title": "3 sums",
        "difficulty": "Medium",
        "function_name": "threeSum",
        "base_points": 300,
        "starter_code": "class Solution:\n    def threeSum(self, nums: list[int], target: int) -> list[list[int]]:\n        pass",
        "description": "Given an integer array nums and an integer target, return all unique triplets [nums[i], nums[j], nums[k]] such that their indices are distinct and their sum equals target. The solution set must not contain duplicate triplets. To ensure a unique and deterministic answer, each individual triplet must be sorted in ascending order (a <= b <= c), and the final list of triplets must be sorted lexicographically.",
        "examples": "Input: nums = [-1, 0, 1, 2, -1, -4], target = 0\nOutput: [[-1, -1, 2], [-1, 0, 1]]\nExplanation: The unique triplets that sum to 0 are [-1, -1, 2] and [-1, 0, 1]. Triplets are sorted internally, and the list of triplets is sorted lexicographically.\n\nInput: nums = [0, 1, 1], target = 0\nOutput: []\nExplanation: No three elements sum to 0.",
        "input_variable": "nums",
        "hidden_test_cases": [
            {"input": "([-1, 0, 1, 2, -1, -4], 0)", "expected": "[[-1, -1, 2], [-1, 0, 1]]"},
            {"input": "([0, 1, 1], 0)", "expected": "[]"},
            {"input": "([0, 0, 0, 0], 0)", "expected": "[[0, 0, 0]]"},
            {"input": "([1, 2, -2, -1, 3], 2)", "expected": "[[-2, 1, 3], [-1, 1, 2]]"},
            {"input": "([1, 1, -2], 0)", "expected": "[[-2, 1, 1]]"}
        ]
    },
    {
        "id": 13,
        "title": "Alternating Number Elimination",
        "difficulty": "Medium",
        "function_name": "lastRemaining",
        "base_points": 300,
        "starter_code": "class Solution:\n    def lastRemaining(self, n: int) -> int:\n        pass",
        "description": "You start with an ordered list of all integers from 1 to n, arranged in a straight line from left to right. You perform an elimination process on this list by alternating directions. In the left to right pass, starting from the left side, you delete the first number, skip the next one, delete the third one, and keep removing every second number until you reach the end of the line. In the right to left pass, looking at the remaining numbers, you start from the right side, delete the rightmost number, skip the next one, delete the third one, and keep removing every second number until you reach the beginning. You repeat these two steps, switching back and forth, until there is exactly one number left. Return that last remaining number.",
        "examples": "Input: n = 9\nOutput: 6\nExplanation:\n1 2 3 4 5 6 7 8 9 (left to right) -> 2 4 6 8 (right to left) -> 2 6 (left to right) -> 6.",
        "input_variable": "n",
        "hidden_test_cases": [
            {"input": "9", "expected": "6"},
            {"input": "1", "expected": "1"},
            {"input": "100", "expected": "54"},
            {"input": "1000", "expected": "510"},
            {"input": "6", "expected": "4"}
        ]
    },
    {
        "id": 14,
        "title": "Battleships",
        "difficulty": "Medium",
        "function_name": "countBattleships",
        "base_points": 300,
        "starter_code": "class Solution:\n    def countBattleships(self, board: list[list[str]]) -> int:\n        pass",
        "description": "Given an m x n grid board where each cell is either a battleship 'X' or empty '.', return the total number of battleships on the board. Battleships can only be placed horizontally or vertically. They are made of the shape 1 x k (1 row, k columns) or k x 1 (k rows, 1 column), where k can be of any size. At least one horizontal or vertical empty cell separates any two battleships, meaning there are no adjacent battleships sharing edges.",
        "examples": "Input: board = [[\"X\",\".\",\".\",\"X\"],[\".\",\".\",\".\",\"X\"],[\".\",\".\",\".\",\"X\"]]\nOutput: 2\nExplanation: There are 2 battleships: one single 'X' in the top-left cell, and a vertical battleship of size 3 on the rightmost column.",
        "input_variable": "board",
        "hidden_test_cases": [
            {"input": "[[\"X\",\".\",\".\",\"X\"],[\".\",\".\",\".\",\"X\"],[\".\",\".\",\".\",\"X\"]]", "expected": "2"},
            {"input": "[[\".\"]]", "expected": "0"},
            {"input": "[[\"X\",\"X\",\"X\"]]", "expected": "1"},
            {"input": "[[\"X\"],[\"X\"],[\"X\"]]", "expected": "1"},
            {"input": "[[\"X\",\".\",\"X\"],[\".\",\".\",\".\"],[\"X\",\".\",\"X\"]]", "expected": "4"}
        ]
    },
    {
        "id": 15,
        "title": "Overlapping intervals",
        "difficulty": "Medium",
        "function_name": "eraseOverlapIntervals",
        "base_points": 300,
        "starter_code": "class Solution:\n    def eraseOverlapIntervals(self, intervals: list[list[int]]) -> int:\n        pass",
        "description": "You are given a list of time slots called intervals. Each time slot is represented as a pair of numbers: [start, end]. Some of these time slots overlap with each other. Your task is to find the minimum number of intervals you need to delete so that none of the remaining intervals overlap. Note that if two intervals just touch at their endpoints, they do not count as overlapping. For example, [1, 2] and [2, 3] are non-overlapping and are allowed to remain.",
        "examples": "Input: intervals = [[1,2],[2,3],[3,4],[1,3]]\nOutput: 1\nExplanation: [1,3] can be removed and the rest of the intervals are non-overlapping.\n\nInput: intervals = [[1,2],[1,2],[1,2]]\nOutput: 2\nExplanation: You need to delete two [1,2] intervals to make the remaining interval non-overlapping.",
        "input_variable": "intervals",
        "hidden_test_cases": [
            {"input": "[[1,2],[2,3],[3,4],[1,3]]", "expected": "1"},
            {"input": "[[1,2],[1,2],[1,2]]", "expected": "2"},
            {"input": "[[1,2],[2,3]]", "expected": "0"},
            {"input": "[[1,100],[11,22],[1,11],[2,12]]", "expected": "2"}
        ]
    },
    {
        "id": 16,
        "title": "Heaters",
        "difficulty": "Medium",
        "function_name": "findRadius",
        "base_points": 300,
        "starter_code": "class Solution:\n    def findRadius(self, houses: list[int], heaters: list[int]) -> int:\n        pass",
        "description": "During the winter, your job is to design a standard heater with a fixed warm radius to heat all the houses. Every house can be warmed as long as the house is within the heater's warm radius. Given the positions of houses and heaters on a horizontal line, return the minimum radius required for the heaters so that they cover all houses. Notice that all the heaters follow the same radius, and the warm radius is identical for all heaters.",
        "examples": "Input: houses = [1,2,3], heaters = [2]\nOutput: 1\nExplanation: The only heater was placed in the position 2, and if we use the radius 1 standard, then all the houses can be warmed.\n\nInput: houses = [1,2,3,4], heaters = [1,4]\nOutput: 1\nExplanation: Heaters at position 1 and 4 can cover all houses with radius 1.",
        "input_variable": "houses",
        "hidden_test_cases": [
            {"input": "([1,2,3], [2])", "expected": "1"},
            {"input": "([1,2,3,4], [1,4])", "expected": "1"},
            {"input": "([1,5], [2])", "expected": "3"},
            {"input": "([1,5], [10])", "expected": "9"},
            {"input": "([1,2,3,4,5,6,7,8,9,10], [3,7])", "expected": "3"}
        ]
    },
    {
        "id": 17,
        "title": "Longest Step Path",
        "difficulty": "Hard",
        "function_name": "longestIncreasingPath",
        "base_points": 600,
        "starter_code": "class Solution:\n    def longestIncreasingPath(self, matrix: list[list[int]]) -> int:\n        pass",
        "description": "You are given an m x n grid of integers called matrix. You want to find a path through the grid that steps from one cell to an adjacent cell, provided the number in the next cell is strictly greater than the number in the current cell. From any cell, you can only move in four directions: up, down, left, or right. You cannot move diagonally or step outside the boundaries of the grid. Return the length of the longest path you can find. You can use dynamic programming with memoization to optimize the search and prevent redundant calculations.",
        "examples": "Input: matrix = [[9,9,4],[6,6,8],[2,1,1]]\nOutput: 4\nExplanation: The longest increasing path is [1, 2, 6, 9].\n\nInput: matrix = [[3,4,5],[3,2,6],[2,2,1]]\nOutput: 4\nExplanation: The longest increasing path is [3, 4, 5, 6] or [2, 3, 4, 5].",
        "input_variable": "matrix",
        "hidden_test_cases": [
            {"input": "[[9,9,4],[6,6,8],[2,1,1]]", "expected": "4"},
            {"input": "[[3,4,5],[3,2,6],[2,2,1]]", "expected": "4"},
            {"input": "[[1]]", "expected": "1"},
            {"input": "[[1, 2], [3, 4]]", "expected": "3"}
        ]
    },
    {
        "id": 18,
        "title": "Dungeon Game",
        "difficulty": "Hard",
        "function_name": "calculateMinimumHP",
        "base_points": 600,
        "starter_code": "class Solution:\n    def calculateMinimumHP(self, dungeon: list[list[int]]) -> int:\n        pass",
        "description": "You are given an m x n grid of integers called dungeon. You start at the top-left corner of the grid and need to reach the bottom-right corner. From any cell, you can only move in two directions: right or down. Each cell in the grid contains an integer that alters your health: negative numbers reduce your health, positive numbers increase your health, and zero leaves it unchanged. You start the journey with a positive health score. However, your health is subject to a strict survival rule: if your health drops to 0 or below at any point, you fail. Return the minimum initial health required at the start to successfully complete the journey without ever hitting 0 or below.",
        "examples": "Input: dungeon = [[-2,-3,3],[-5,-10,1],[10,30,-5]]\nOutput: 7\nExplanation: Path: right -> right -> down -> down. Health changes: 7 -> 5 -> 2 -> 5 -> 6 -> 1. Minimum initial HP is 7.",
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
        "id": 19,
        "title": "Efficient Task Distribution",
        "difficulty": "Hard",
        "function_name": "minimumTimeRequired",
        "base_points": 600,
        "starter_code": "class Solution:\n    def minimumTimeRequired(self, jobs: list[int], k: int) -> int:\n        pass",
        "description": "You are given an integer array jobs, where jobs[i] represents the amount of time it takes to complete the i-th task. There are k identical servers available to process these tasks. You must assign every task to exactly one server. The total workload of a server is the sum of the times of all tasks assigned to it. Your goal is to distribute the tasks so that the busiest server works as little as possible. Return the minimum possible maximum workload among all the servers. You can use backtracking with pruning techniques to find the optimal assignment efficiently.",
        "examples": "Input: jobs = [3,2,3], k = 3\nOutput: 3\nExplanation: Assign each job to a different server. Max workload is 3.\n\nInput: jobs = [1,2,4,7,8], k = 2\nOutput: 11\nExplanation: Assign jobs [1, 2, 8] to the first server (11) and [4, 7] to the second server (11). The maximum workload is 11.",
        "input_variable": "jobs",
        "hidden_test_cases": [
            {"input": "([3,2,3], 3)", "expected": "3"},
            {"input": "([1,2,4,7,8], 2)", "expected": "11"},
            {"input": "([5,5,4,4,4], 2)", "expected": "12"},
            {"input": "([254,256,256,254,251,256,254,253], 3)", "expected": "761"}
        ]
    },
    {
        "id": 20,
        "title": "Balanced Token Distribution",
        "difficulty": "Hard",
        "function_name": "candy",
        "base_points": 600,
        "starter_code": "class Solution:\n    def candy(self, ratings: list[int]) -> int:\n        pass",
        "description": "There are n workers standing in a line. Each worker has a performance score listed in an integer array called ratings. You need to hand out tokens to these workers based on two simple rules: first, every worker must get at least 1 token; second, a worker with a higher score than their immediate neighbor (left or right) must get more tokens than that neighbor. Return the minimum total number of tokens you need to distribute to satisfy these rules.",
        "examples": "Input: ratings = [1,0,2]\nOutput: 5\nExplanation: You can allocate to the first, second and third worker 2, 1, 2 tokens respectively.\n\nInput: ratings = [1,2,2]\nOutput: 4\nExplanation: You can allocate to the first, second and third worker 1, 2, 1 tokens respectively. The third worker gets 1 because it satisfies the rules.",
        "input_variable": "ratings",
        "hidden_test_cases": [
            {"input": "[1,0,2]", "expected": "5"},
            {"input": "[1,2,2]", "expected": "4"},
            {"input": "[1,2,3,4,5]", "expected": "15"},
            {"input": "[5,4,3,2,1]", "expected": "15"},
            {"input": "[1,3,2,1,4,3,2,1]", "expected": "17"}
        ]
    }
]

BONUS_QUESTIONS = [
    {
        "title": "Bonus Challenge 1: Reversing and Doubling",
        "description": "Challenge: Given the following Python function and the target Output, determine the list of integers Input that would produce this result.\n\nclass Solution:\n    def reverse_and_double(self, nums: list[int]) -> list[int]:\n        reversed_nums = nums[::-1]\n        doubled_nums = [x * 2 for x in reversed_nums]\n        return doubled_nums\n\nTarget Output: [4, 2]\nInput (nums): ?",
        "starter_code": "import ast\ntry:\n    nums = ast.literal_eval(input().strip())\n    if isinstance(nums, list) and all(isinstance(x, int) for x in nums):\n        reversed_nums = nums[::-1]\n        doubled_nums = [x * 2 for x in reversed_nums]\n        if doubled_nums == [4, 2]:\n            print(\"SUCCESS\")\n        else:\n            print(\"TRY AGAIN\")\n    else:\n        print(\"INVALID INPUT\")\nexcept Exception:\n    print(\"ERROR\")",
        "expected_output": "SUCCESS",
        "input_type_hint": "Enter a list",
        "order": 1,
        "duration_minutes": 15
    },
    {
        "title": "Bonus Challenge 2: Character Shift Cipher",
        "description": "Challenge: Given the following Python function and the target Output, find the string Input that generates this result. The function shifts each character's ASCII value by 1.\n\nclass Solution:\n    def character_shift(self, s: str) -> str:\n        shifted_chars = [chr(ord(c) + 1) for c in s]\n        return \"\".join(shifted_chars)\n\nTarget Output: 'bc'\nInput (s): ?",
        "starter_code": "try:\n    s = input().strip()\n    if (s.startswith(\"'\") and s.endswith(\"'\")) or (s.startswith('\"') and s.endswith('\"')):\n        import ast\n        s = ast.literal_eval(s)\n    shifted_chars = [chr(ord(c) + 1) for c in s]\n    res = \"\".join(shifted_chars)\n    if res == 'bc':\n        print(\"SUCCESS\")\n    else:\n        print(\"TRY AGAIN\")\nexcept Exception:\n    print(\"ERROR\")",
        "expected_output": "SUCCESS",
        "input_type_hint": "Enter a string",
        "order": 2,
        "duration_minutes": 15
    },
    {
        "title": "Bonus Challenge 3: Sum of Evens and Odds",
        "description": "Challenge: Given the following Python function and the target Output, find the list of integers Input that results in the given two-element list.\n\nclass Solution:\n    def sum_evens_and_odds(self, numbers: list[int]) -> list[int]:\n        even_sum = 0\n        odd_sum = 0\n        for num in numbers:\n            if num % 2 == 0:\n                even_sum += num\n            else:\n                odd_sum += num\n        return [even_sum, odd_sum]\n\nTarget Output: [6, 3]\nInput (numbers): ?",
        "starter_code": "import ast\ntry:\n    numbers = ast.literal_eval(input().strip())\n    if isinstance(numbers, list) and all(isinstance(x, int) for x in numbers):\n        even_sum = 0\n        odd_sum = 0\n        for num in numbers:\n            if num % 2 == 0:\n                even_sum += num\n            else:\n                odd_sum += num\n        res = [even_sum, odd_sum]\n        if res == [6, 3]:\n            print(\"SUCCESS\")\n        else:\n            print(\"TRY AGAIN\")\n    else:\n        print(\"INVALID INPUT\")\nexcept Exception:\n    print(\"ERROR\")",
        "expected_output": "SUCCESS",
        "input_type_hint": "A list of integers, e.g. [6, 3]",
        "order": 3,
        "duration_minutes": 15
    }
]
