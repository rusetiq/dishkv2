from django.test import TestCase, Client
from django.contrib.auth.models import User
from platform_app.models import Problem, TeamProgress, HackathonState
from django.utils import timezone

class CodeRunnerTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testteam", password="password")
        self.client.login(username="testteam", password="password")
        
        self.state = HackathonState.objects.create(
            is_started=True,
            is_finished=False,
            is_paused=False,
            start_time=timezone.now()
        )
        
        self.problem = Problem.objects.create(
            title="Two Sum",
            description="Find two numbers",
            difficulty="Easy",
            function_name="twoSum",
            base_points=100,
            starter_code="class Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\n        pass",
            hidden_test_cases=[
                {"input": "([2,7,11,15], 9)", "expected": "[0, 1]"},
                {"input": "([3,2,4], 6)", "expected": "[1, 2]"},
                {"input": "([3,3], 6)", "expected": "[0, 1]"}
            ]
        )
        self.progress = TeamProgress.objects.create(
            team=self.user,
            problem=self.problem,
            current_code=self.problem.starter_code
        )

    def test_run_code_custom_accepted(self):
        code = "class Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\n        lookup = {}\n        for i, num in enumerate(nums):\n            if target - num in lookup:\n                return [lookup[target - num], i]\n            lookup[num] = i\n        return []"
        response = self.client.post("/api/run-custom/", {
            "problem_id": self.problem.id,
            "code": code
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "Accepted")
        self.assertEqual(len(data["results"]), 3)
        self.assertEqual(data["results"][0]["status"], "Accepted")

    def test_run_code_custom_wrong_answer(self):
        code = "class Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\n        return [0, 0]"
        response = self.client.post("/api/run-custom/", {
            "problem_id": self.problem.id,
            "code": code
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "Wrong Answer")
        self.assertEqual(data["results"][0]["status"], "Wrong Answer")

    def test_run_code_custom_runtime_error(self):
        code = "class Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\n        raise ValueError('error')"
        response = self.client.post("/api/run-custom/", {
            "problem_id": self.problem.id,
            "code": code
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "Runtime Error")
        self.assertEqual(data["results"][0]["status"], "Runtime Error")
        self.assertIn("ValueError", data["results"][0]["error"])

    def test_submit_code_accepted(self):
        code = "class Solution:\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\n        lookup = {}\n        for i, num in enumerate(nums):\n            if target - num in lookup:\n                return [lookup[target - num], i]\n            lookup[num] = i\n        return []"
        response = self.client.post("/api/submit/", {
            "problem_id": self.problem.id,
            "code": code
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "Correct Answer!")