SOLUTIONS = [
    {
        "id": 1,
        "title": "Median-Adjusted Mean",
        "method_name": "median_adjusted_mean",
        "difficulty": "Easy",
        "explanation": "Sort the array, slice it from index 1 to -1 to exclude the single minimum and maximum, then calculate the mean using integer floor division.",
        "solution_code": "class Solution:\n    def median_adjusted_mean(self, data: list[int]) -> int:\n        data.sort()\n        return sum(data[1:-1]) // (len(data) - 2)"
    },
    {
        "id": 2,
        "title": "Unique Element Verification",
        "method_name": "verify_uniqueness",
        "difficulty": "Easy",
        "explanation": "Compare the length of the list with the length of its set. If they are different, duplicates exist.",
        "solution_code": "class Solution:\n    def verify_uniqueness(self, numbers: list[int]) -> bool:\n        return len(numbers) != len(set(numbers))"
    },
    {
        "id": 3,
        "title": "Three Sum (Single)",
        "method_name": "threeSum",
        "difficulty": "Easy",
        "explanation": "Store indices of elements in a lookup table. Use two nested loops to check pairs and find the third element in the hash map.",
        "solution_code": "class Solution:\n    def threeSum(self, nums: list[int], target: int) -> list[int]:\n        lookup = {}\n        for i, num in enumerate(nums):\n            lookup[num] = i\n        for i in range(len(nums)):\n            for j in range(i + 1, len(nums)):\n                needed = target - nums[i] - nums[j]\n                if needed in lookup and lookup[needed] > j:\n                    return [i, j, lookup[needed]]\n        return []"
    },
    {
        "id": 4,
        "title": "Defective Product Search",
        "method_name": "find_first_defective",
        "difficulty": "Easy",
        "explanation": "Perform binary search between 1 and n. If the mid product is defective, search the left half; otherwise, search the right half.",
        "solution_code": "class Solution:\n    def find_first_defective(self, n: int) -> int:\n        lo, hi = 1, n\n        ans = n\n        while lo <= hi:\n            mid = (lo + hi) // 2\n            if isBadVersion(mid):\n                ans = mid\n                hi = mid - 1\n            else:\n                lo = mid + 1\n        return ans"
    },
    {
        "id": 5,
        "title": "Arithmetic Coefficient Pyramid",
        "method_name": "generate_pyramid",
        "difficulty": "Easy",
        "explanation": "Build Pascal's triangle row by row. Each element is the sum of the two elements above it in the previous row.",
        "solution_code": "class Solution:\n    def generate_pyramid(self, num_rows: int) -> list[list[int]]:\n        if num_rows == 0:\n            return []\n        res = [[1]]\n        for i in range(1, num_rows):\n            row = [1]\n            prev = res[-1]\n            for j in range(len(prev) - 1):\n                row.append(prev[j] + prev[j+1])\n            row.append(1)\n            res.append(row)\n        return res"
    },
    {
        "id": 6,
        "title": "Balanced Character Set",
        "method_name": "is_balanced_by_removal",
        "difficulty": "Easy",
        "explanation": "Count occurrences of each character. Try removing exactly one occurrence of each character and check if all remaining frequencies are identical.",
        "solution_code": "class Solution:\n    def is_balanced_by_removal(self, s: str) -> bool:\n        if not s:\n            return False\n        counts = {}\n        for c in s:\n            counts[c] = counts.get(c, 0) + 1\n        for k in counts:\n            temp = dict(counts)\n            temp[k] -= 1\n            if temp[k] == 0:\n                del temp[k]\n            if len(set(temp.values())) <= 1:\n                return True\n        return False"
    },
    {
        "id": 7,
        "title": "Number of Islands",
        "method_name": "numIslands",
        "difficulty": "Medium",
        "explanation": "Scan grid and perform DFS traversal for every '1' encountered, marking all visited '1' cells to '0' to avoid double counting.",
        "solution_code": "class Solution:\n    def numIslands(self, grid: list[list[str]]) -> int:\n        if not grid:\n            return 0\n        m, n = len(grid), len(grid[0])\n        count = 0\n        def dfs(r, c):\n            if r < 0 or r >= m or c < 0 or c >= n or grid[r][c] == '0':\n                return\n            grid[r][c] = '0'\n            dfs(r+1, c)\n            dfs(r-1, c)\n            dfs(r, c+1)\n            dfs(r, c-1)\n        for r in range(m):\n            for c in range(n):\n                if grid[r][c] == '1':\n                    count += 1\n                    dfs(r, c)\n        return count"
    },
    {
        "id": 8,
        "title": "Descent to the Deep",
        "method_name": "minimumTotal",
        "difficulty": "Medium",
        "explanation": "Bottom-up dynamic programming. Compute path sums from bottom row upward, updating the minimal sums in-place.",
        "solution_code": "class Solution:\n    def minimumTotal(self, triangle: list[list[int]]) -> int:\n        if not triangle:\n            return 0\n        dp = list(triangle[-1])\n        for row in range(len(triangle) - 2, -1, -1):\n            for col in range(len(triangle[row])):\n                dp[col] = triangle[row][col] + min(dp[col], dp[col+1])\n        return dp[0]"
    },
    {
        "id": 9,
        "title": "Alternating End-Pick Game",
        "method_name": "predictTheWinner",
        "difficulty": "Medium",
        "explanation": "Minimax strategy with dynamic programming. Compute the maximum relative score difference the first player can achieve.",
        "solution_code": "class Solution:\n    def predictTheWinner(self, nums: list[int]) -> bool:\n        n = len(nums)\n        dp = [0] * n\n        for i in range(n):\n            dp[i] = nums[i]\n        for size in range(2, n + 1):\n            next_dp = [0] * (n - size + 1)\n            for i in range(n - size + 1):\n                j = i + size - 1\n                next_dp[i] = max(nums[i] - dp[i+1], nums[j] - dp[i])\n            dp = next_dp\n        return dp[0] >= 0"
    },
    {
        "id": 10,
        "title": "Word Finder",
        "method_name": "findLongestWord",
        "difficulty": "Medium",
        "explanation": "Filter words by checking if they are subsequences of the string using two-pointer scan. Keep the longest and lexicographically smallest match.",
        "solution_code": "class Solution:\n    def findLongestWord(self, s: str, dictionary: list[str]) -> str:\n        def is_subsequence(word):\n            i = 0\n            for char in s:\n                if i < len(word) and word[i] == char:\n                    i += 1\n            return i == len(word)\n        longest = \"\"\n        for word in dictionary:\n            if is_subsequence(word):\n                if len(word) > len(longest) or (len(word) == len(longest) and word < longest):\n                    longest = word\n        return longest"
    },
    {
        "id": 11,
        "title": "Zig-Zag Array Reordering",
        "method_name": "wiggleSort",
        "difficulty": "Medium",
        "explanation": "Sort array, partition into smaller and larger halves, reverse them to prevent adjacent equal elements from touching, and interleave.",
        "solution_code": "class Solution:\n    def wiggleSort(self, nums: list[int]) -> list[int]:\n        arr = sorted(nums)\n        n = len(arr)\n        mid = (n + 1) // 2\n        left = arr[:mid][::-1]\n        right = arr[mid:][::-1]\n        res = []\n        for i in range(mid):\n            res.append(left[i])\n            if i < len(right):\n                res.append(right[i])\n        return res"
    },
    {
        "id": 12,
        "title": "3 sums (Multiple)",
        "method_name": "threeSum",
        "difficulty": "Medium",
        "explanation": "Sort array and use fixed pointer with two-pointer scan. Skip duplicate triplets to return all unique combinations summing to target.",
        "solution_code": "class Solution:\n    def threeSum(self, nums: list[int], target: int) -> list[list[int]]:\n        nums.sort()\n        res = []\n        n = len(nums)\n        for i in range(n - 2):\n            if i > 0 and nums[i] == nums[i-1]:\n                continue\n            left, right = i + 1, n - 1\n            while left < right:\n                total = nums[i] + nums[left] + nums[right]\n                if total == target:\n                    res.append([nums[i], nums[left], nums[right]])\n                    while left < right and nums[left] == nums[left+1]:\n                        left += 1\n                    while left < right and nums[right] == nums[right-1]:\n                        right -= 1\n                    left += 1\n                    right -= 1\n                elif total < target:\n                    left += 1\n                else:                    right -= 1\n        return res"
    },
    {
        "id": 13,
        "title": "Alternating Number Elimination",
        "method_name": "lastRemaining",
        "difficulty": "Medium",
        "explanation": "Tracks the first element (head) of the remaining numbers. The step size doubles each round, and the head updates based on direction and parity.",
        "solution_code": "class Solution:\n    def lastRemaining(self, n: int) -> int:\n        head = 1\n        step = 1\n        remaining = n\n        left_to_right = True\n        while remaining > 1:\n            if left_to_right or remaining % 2 == 1:\n                head += step\n            remaining //= 2\n            step *= 2\n            left_to_right = not left_to_right\n        return head"
    },
    {
        "id": 14,
        "title": "Battleships",
        "method_name": "countBattleships",
        "difficulty": "Medium",
        "explanation": "Count the top-left cell of each battleship segment. If a cell contains 'X', check if its top or left neighbor is 'X'; if not, it represents a new battleship.",
        "solution_code": "class Solution:\n    def countBattleships(self, board: list[list[str]]) -> int:\n        if not board:\n            return 0\n        m, n = len(board), len(board[0])\n        count = 0\n        for r in range(m):\n            for c in range(n):\n                if board[r][c] == 'X':\n                    if (r > 0 and board[r-1][c] == 'X') or (c > 0 and board[r][c-1] == 'X'):\n                        continue\n                    count += 1\n        return count"
    },
    {
        "id": 15,
        "title": "Overlapping intervals",
        "method_name": "eraseOverlapIntervals",
        "difficulty": "Medium",
        "explanation": "Greedy interval scheduling. Sort intervals by end time and count overlapping intervals to remove.",
        "solution_code": "class Solution:\n    def eraseOverlapIntervals(self, intervals: list[list[int]]) -> int:\n        if not intervals:\n            return 0\n        intervals.sort(key=lambda x: x[1])\n        count = 0\n        end = intervals[0][1]\n        for i in range(1, len(intervals)):\n            if intervals[i][0] < end:\n                count += 1\n            else:\n                end = intervals[i][1]\n        return count"
    },
    {
        "id": 16,
        "title": "Heaters",
        "method_name": "findRadius",
        "difficulty": "Medium",
        "explanation": "Binary search each house's location inside the sorted heaters list, finding the minimum distance to any heater. Track the max radius required across all houses.",
        "solution_code": "class Solution:\n    def findRadius(self, houses: list[int], heaters: list[int]) -> int:\n        houses.sort()\n        heaters.sort()\n        def bisect_left(a, x):\n            lo, hi = 0, len(a)\n            while lo < hi:\n                mid = (lo + hi) // 2\n                if a[mid] < x: lo = mid + 1\n                else: hi = mid\n            return lo\n        ans = 0\n        for house in houses:\n            idx = bisect_left(heaters, house)\n            dist1 = abs(heaters[idx] - house) if idx < len(heaters) else float('inf')\n            dist2 = abs(heaters[idx - 1] - house) if idx > 0 else float('inf')\n            ans = max(ans, min(dist1, dist2))\n        return ans"
    },
    {
        "id": 17,
        "title": "Longest Step Path",
        "method_name": "longestIncreasingPath",
        "difficulty": "Hard",
        "explanation": "Depth-first search with memoization. Starting from each cell, walk in four directions to strictly greater cells and cache the longest increasing path.",
        "solution_code": "class Solution:\n    def longestIncreasingPath(self, matrix: list[list[int]]) -> int:\n        if not matrix:\n            return 0\n        m, n = len(matrix), len(matrix[0])\n        memo = [[0] * n for _ in range(m)]\n        def dfs(r, c):\n            if memo[r][c] != 0:\n                return memo[r][c]\n            val = matrix[r][c]\n            res = 1\n            for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:\n                nr, nc = r + dr, c + dc\n                if 0 <= nr < m and 0 <= nc < n and matrix[nr][nc] > val:\n                    res = max(res, 1 + dfs(nr, nc))\n            memo[r][c] = res\n            return res\n        ans = 0\n        for r in range(m):\n            for c in range(n):\n                ans = max(ans, dfs(r, c))\n        return ans"
    },
    {
        "id": 18,
        "title": "Dungeon Game",
        "method_name": "calculateMinimumHP",
        "difficulty": "Hard",
        "explanation": "Dynamic programming computed backwards from the bottom-right corner. Calculate the minimum health needed on entering each cell to ensure survival.",
        "solution_code": "class Solution:\n    def calculateMinimumHP(self, dungeon: list[list[int]]) -> int:\n        m, n = len(dungeon), len(dungeon[0])\n        dp = [[float('inf')] * (n + 1) for _ in range(m + 1)]\n        dp[m][n-1] = dp[m-1][n] = 1\n        for r in range(m - 1, -1, -1):\n            for c in range(n - 1, -1, -1):\n                min_hp_on_exit = min(dp[r+1][c], dp[r][c+1])\n                dp[r][c] = max(1, min_hp_on_exit - dungeon[r][c])\n        return int(dp[0][0])"
    },
    {
        "id": 19,
        "title": "Efficient Task Distribution",
        "method_name": "minimumTimeRequired",
        "difficulty": "Hard",
        "explanation": "Backtracking with symmetry pruning. Sort jobs in descending order, try assigning each job to each of the k servers, and prune branches exceeding the current best minimum time.",
        "solution_code": "class Solution:\n    def minimumTimeRequired(self, jobs: list[int], k: int) -> int:\n        jobs.sort(reverse=True)\n        self.ans = sum(jobs)\n        workloads = [0] * k\n        def dfs(idx):\n            if idx == len(jobs):\n                self.ans = min(self.ans, max(workloads))\n                return\n            seen = set()\n            for j in range(k):\n                if workloads[j] in seen:\n                    continue\n                seen.add(workloads[j])\n                if workloads[j] + jobs[idx] < self.ans:\n                    workloads[j] += jobs[idx]\n                    dfs(idx + 1)\n                    workloads[j] -= jobs[idx]\n                if workloads[j] == 0:\n                    break\n        dfs(0)\n        return self.ans"
    },
    {
        "id": 20,
        "title": "Balanced Token Distribution",
        "method_name": "candy",
        "difficulty": "Hard",
        "explanation": "Greedy two-pass algorithm. The left-to-right pass ensures children with higher ratings than their left neighbor get more candy. The right-to-left pass ensures the same relative to the right neighbor.",
        "solution_code": "class Solution:\n    def candy(self, ratings: list[int]) -> int:\n        n = len(ratings)\n        candies = [1] * n\n        for i in range(1, n):\n            if ratings[i] > ratings[i-1]:\n                candies[i] = candies[i-1] + 1\n        for i in range(n - 2, -1, -1):\n            if ratings[i] > ratings[i+1]:\n                candies[i] = max(candies[i], candies[i+1] + 1)\n        return sum(candies)"
    }
]
