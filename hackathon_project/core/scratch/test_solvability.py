import json
import ast

# Import the LEETCODE_PROBLEMS configuration
import sys
sys.path.append("/Users/rusetiq/Desktop/dishkv2/hackathon_project/core")
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
import django
django.setup()

from platform_app.leetcode_data import LEETCODE_PROBLEMS

# ----------------- SOLUTIONS FOR THE 15 NEW PROBLEMS -----------------

class Solution:
    # 7. Number of Islands
    def numIslands(self, grid: list[list[str]]) -> int:
        if not grid:
            return 0
        m, n = len(grid), len(grid[0])
        count = 0
        def dfs(r, c):
            if r < 0 or r >= m or c < 0 or c >= n or grid[r][c] == '0':
                return
            grid[r][c] = '0'
            dfs(r+1, c)
            dfs(r-1, c)
            dfs(r, c+1)
            dfs(r, c-1)
        for r in range(m):
            for c in range(n):
                if grid[r][c] == '1':
                    count += 1
                    dfs(r, c)
        return count

    # 8. Descent to the Deep
    def minimumTotal(self, triangle: list[list[int]]) -> int:
        if not triangle:
            return 0
        # Bottom-up DP
        dp = list(triangle[-1])
        for row in range(len(triangle) - 2, -1, -1):
            for col in range(len(triangle[row])):
                dp[col] = triangle[row][col] + min(dp[col], dp[col+1])
        return dp[0]

    # 9. Alternating End-Pick Game
    def predictTheWinner(self, nums: list[int]) -> bool:
        n = len(nums)
        dp = [0] * n
        for i in range(n):
            dp[i] = nums[i]
        for size in range(2, n + 1):
            next_dp = [0] * (n - size + 1)
            for i in range(n - size + 1):
                j = i + size - 1
                next_dp[i] = max(nums[i] - dp[i+1], nums[j] - dp[i])
            dp = next_dp
        return dp[0] >= 0

    # 10. Word Finder
    def findLongestWord(self, s: str, dictionary: list[str]) -> str:
        def is_subsequence(word):
            i = 0
            for char in s:
                if i < len(word) and word[i] == char:
                    i += 1
            return i == len(word)
        
        longest = ""
        for word in dictionary:
            if is_subsequence(word):
                if len(word) > len(longest) or (len(word) == len(longest) and word < longest):
                    longest = word
        return longest

    # 11. Zig-Zag Array Reordering
    def wiggleSort(self, nums: list[int]) -> list[int]:
        # To avoid side effects, copy first
        arr = sorted(nums)
        n = len(arr)
        mid = (n + 1) // 2
        left = arr[:mid][::-1]
        right = arr[mid:][::-1]
        
        res = []
        for i in range(mid):
            res.append(left[i])
            if i < len(right):
                res.append(right[i])
        return res

    # 12. 3 sums
    def threeSum(self, nums: list[int], target: int) -> list[list[int]]:
        nums.sort()
        res = []
        n = len(nums)
        for i in range(n - 2):
            if i > 0 and nums[i] == nums[i-1]:
                continue
            left, right = i + 1, n - 1
            while left < right:
                total = nums[i] + nums[left] + nums[right]
                if total == target:
                    res.append([nums[i], nums[left], nums[right]])
                    while left < right and nums[left] == nums[left+1]:
                        left += 1
                    while left < right and nums[right] == nums[right-1]:
                        right -= 1
                    left += 1
                    right -= 1
                elif total < target:
                    left += 1
                else:
                    right -= 1
        return res

    # 13. Alternating Number Elimination
    def lastRemaining(self, n: int) -> int:
        head = 1
        step = 1
        remaining = n
        left_to_right = True
        while remaining > 1:
            if left_to_right or remaining % 2 == 1:
                head += step
            remaining //= 2
            step *= 2
            left_to_right = not left_to_right
        return head

    # 14. Battleships
    def countBattleships(self, board: list[list[str]]) -> int:
        if not board:
            return 0
        m, n = len(board), len(board[0])
        count = 0
        for r in range(m):
            for c in range(n):
                if board[r][c] == 'X':
                    if (r > 0 and board[r-1][c] == 'X') or (c > 0 and board[r][c-1] == 'X'):
                        continue
                    count += 1
        return count

    # 15. Overlapping intervals
    def eraseOverlapIntervals(self, intervals: list[list[int]]) -> int:
        if not intervals:
            return 0
        intervals.sort(key=lambda x: x[1])
        count = 0
        end = intervals[0][1]
        for i in range(1, len(intervals)):
            if intervals[i][0] < end:
                count += 1
            else:
                end = intervals[i][1]
        return count

    # 16. Heaters
    def findRadius(self, houses: list[int], heaters: list[int]) -> int:
        houses.sort()
        heaters.sort()
        def bisect_left(a, x):
            lo, hi = 0, len(a)
            while lo < hi:
                mid = (lo + hi) // 2
                if a[mid] < x: lo = mid + 1
                else: hi = mid
            return lo
        ans = 0
        for house in houses:
            idx = bisect_left(heaters, house)
            dist1 = abs(heaters[idx] - house) if idx < len(heaters) else float('inf')
            dist2 = abs(heaters[idx - 1] - house) if idx > 0 else float('inf')
            ans = max(ans, min(dist1, dist2))
        return ans

    # 17. Longest Step Path
    def longestIncreasingPath(self, matrix: list[list[int]]) -> int:
        if not matrix:
            return 0
        m, n = len(matrix), len(matrix[0])
        memo = [[0] * n for _ in range(m)]
        def dfs(r, c):
            if memo[r][c] != 0:
                return memo[r][c]
            val = matrix[r][c]
            res = 1
            for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and matrix[nr][nc] > val:
                    res = max(res, 1 + dfs(nr, nc))
            memo[r][c] = res
            return res
        ans = 0
        for r in range(m):
            for c in range(n):
                ans = max(ans, dfs(r, c))
        return ans

    # 18. Dungeon Game
    def calculateMinimumHP(self, dungeon: list[list[int]]) -> int:
        m, n = len(dungeon), len(dungeon[0])
        dp = [[float('inf')] * (n + 1) for _ in range(m + 1)]
        dp[m][n-1] = dp[m-1][n] = 1
        for r in range(m - 1, -1, -1):
            for c in range(n - 1, -1, -1):
                min_hp_on_exit = min(dp[r+1][c], dp[r][c+1])
                dp[r][c] = max(1, min_hp_on_exit - dungeon[r][c])
        return int(dp[0][0])

    # 19. Efficient Task Distribution
    def minimumTimeRequired(self, jobs: list[int], k: int) -> int:
        jobs.sort(reverse=True)
        self.ans = sum(jobs)
        workloads = [0] * k
        
        def dfs(idx):
            if idx == len(jobs):
                self.ans = min(self.ans, max(workloads))
                return
            
            seen = set()
            for j in range(k):
                if workloads[j] in seen:
                    continue
                seen.add(workloads[j])
                
                if workloads[j] + jobs[idx] < self.ans:
                    workloads[j] += jobs[idx]
                    dfs(idx + 1)
                    workloads[j] -= jobs[idx]
                
                if workloads[j] == 0:
                    break
        dfs(0)
        return self.ans

    # 20. Balanced Token Distribution
    def candy(self, ratings: list[int]) -> int:
        n = len(ratings)
        candies = [1] * n
        for i in range(1, n):
            if ratings[i] > ratings[i-1]:
                candies[i] = candies[i-1] + 1
        for i in range(n - 2, -1, -1):
            if ratings[i] > ratings[i+1]:
                candies[i] = max(candies[i], candies[i+1] + 1)
        return sum(candies)

    # 21. Password checker
    def strongPasswordChecker(self, password: str) -> int:
        n = len(password)
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        
        missing_types = 3 - (has_lower + has_upper + has_digit)
        
        # Count repeats
        repeats = []
        i = 0
        while i < n:
            j = i
            while j < n and password[j] == password[i]:
                j += 1
            length = j - i
            if length >= 3:
                repeats.append(length)
            i = j
            
        if n < 6:
            return max(6 - n, missing_types)
        elif n <= 20:
            replace_count = sum(length // 3 for length in repeats)
            return max(replace_count, missing_types)
        else:
            delete_count = n - 20
            # Try to reduce repeating sections to maximize replacement efficiency
            # Priority 1: repeats with length % 3 == 0 (each deletion saves 1 replacement)
            # Priority 2: repeats with length % 3 == 1 (each 2 deletions save 1 replacement)
            # Priority 3: repeats with length % 3 == 2 (each 3 deletions save 1 replacement)
            
            # Since we can just simulate or greedy delete:
            for rem in [0, 1, 2]:
                for idx, length in enumerate(repeats):
                    if length >= 3 and length % 3 == rem:
                        needed = rem + 1
                        actual_del = min(delete_count, needed)
                        delete_count -= actual_del
                        repeats[idx] -= actual_del
                        if delete_count == 0:
                            break
                if delete_count == 0:
                    break
            
            # If we still need to delete:
            if delete_count > 0:
                for idx, length in enumerate(repeats):
                    if length >= 3:
                        actual_del = min(delete_count, length - 2)
                        delete_count -= actual_del
                        repeats[idx] -= actual_del
                        if delete_count == 0:
                            break
                            
            replace_count = sum(length // 3 for length in repeats if length >= 3)
            return (n - 20) + max(replace_count, missing_types)


# ----------------- TESTING EXECUTION -----------------

sol = Solution()
all_ok = True

for problem in LEETCODE_PROBLEMS:
    pid = problem["id"]
    if pid < 7:
        continue # skip easy ones
        
    title = problem["title"]
    func_name = problem["function_name"]
    hidden_cases = problem["hidden_test_cases"]
    
    print(f"Testing Problem {pid}: {title}...")
    func = getattr(sol, func_name, None)
    if not func:
        print(f"  FAILED: Function {func_name} not found on Solution class")
        all_ok = False
        continue
        
    for idx, case in enumerate(hidden_cases):
        inp_str = case["input"]
        exp_str = case["expected"]
        
        # Parse inputs
        try:
            parsed_input = ast.literal_eval(inp_str)
        except Exception:
            lines_split = [line.strip() for line in inp_str.split('\n') if line.strip()]
            parsed_input = []
            for line in lines_split:
                try:
                    parsed_input.append(ast.literal_eval(line))
                except Exception:
                    parsed_input.append(line)
                    
        # Call function
        try:
            # Replicate django runner parameter expansion
            # count arguments minus self
            import inspect
            sig = inspect.signature(func)
            expected_args_count = len(sig.parameters)
            
            if expected_args_count > 1:
                if isinstance(parsed_input, tuple):
                    args = parsed_input
                elif isinstance(parsed_input, list) and len(parsed_input) == expected_args_count:
                    args = tuple(parsed_input)
                else:
                    args = (parsed_input,)
            else:
                args = (parsed_input,)
                
            # If grid (Problem 7), copy it so DFS doesn't modify the test case for next runs
            if title == "Number of Islands" or title == "Battleships":
                # Deep copy of 2D list
                args = ( [list(r) for r in args[0]], )
                
            res = func(*args)
            
            # Format output as django runner does
            if res is True:
                out = "True"
            elif res is False:
                out = "False"
            elif res is None:
                out = "None"
            elif isinstance(res, (list, dict, tuple)):
                out = json.dumps(res)
            else:
                out = str(res)
                
            if out.strip() != exp_str.strip():
                print(f"  FAILED Case {idx}: Input={inp_str} Expected={exp_str} Got={out}")
                all_ok = False
            else:
                print(f"  OK Case {idx}")
        except Exception as e:
            print(f"  ERROR Case {idx}: {e}")
            all_ok = False

if all_ok:
    print("\nALL PROBLEMS ARE SOLVABLE AND TEST CASES ARE CORRECT!")
    sys.exit(0)
else:
    print("\nSOME TEST CASES OR SOLUTIONS FAILED!")
    sys.exit(1)
