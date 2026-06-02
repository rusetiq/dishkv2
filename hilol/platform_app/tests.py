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

class AdminTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_superuser(username="admin", password="password", email="admin@test.com")
        self.normal_user = User.objects.create_user(username="testteam", password="password")
        self.state = HackathonState.objects.create(
            is_started=True,
            is_finished=False,
            is_paused=False,
            start_time=timezone.now(),
            hints_enabled=True
        )

    def test_admin_toggle_hints_as_staff(self):
        self.client.login(username="admin", password="password")
        response = self.client.post("/admin-api/toggle-hints/")
        self.assertEqual(response.status_code, 302)
        self.state.refresh_from_db()
        self.assertFalse(self.state.hints_enabled)

        response = self.client.post("/admin-api/toggle-hints/")
        self.assertEqual(response.status_code, 302)
        self.state.refresh_from_db()
        self.assertTrue(self.state.hints_enabled)

    def test_admin_toggle_hints_as_normal_user(self):
        self.client.login(username="testteam", password="password")
        response = self.client.post("/admin-api/toggle-hints/")
        self.assertEqual(response.status_code, 302)
        self.state.refresh_from_db()
        self.assertTrue(self.state.hints_enabled)


import os
import csv
from unittest.mock import patch
from platform_app.models import Problem, BonusQuestion, TeamProgress, BonusSubmission
import db_admin

class DBAdminTestCase(TestCase):
    def setUp(self):
        Problem.objects.all().delete()
        BonusQuestion.objects.all().delete()
        self.problems_csv_path = "test_problems.csv"
        self.bonus_csv_path = "test_bonus.csv"

    def tearDown(self):
        for p in [self.problems_csv_path, self.bonus_csv_path]:
            if os.path.exists(p):
                os.remove(p)

    def test_add_problems_from_csv(self):
        with open(self.problems_csv_path, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'title', 'description', 'difficulty', 'function_name', 'input_variable', 'base_points', 'starter_code', 'examples', 'hidden_test_cases'])
            writer.writerow([
                '99', 'Test Problem 1', 'Desc 1', 'Medium', 'testFunc', 'data', '120',
                'def testFunc(data):\\n    pass', 'Input: data = 1', '[{"input": "1", "expected": "2"}]'
            ])
            
        with patch('builtins.input', return_value=self.problems_csv_path):
            db_admin.add_problems_from_csv()
            
        prob = Problem.objects.filter(id=99).first()
        self.assertIsNotNone(prob)
        self.assertEqual(prob.title, "Test Problem 1")
        self.assertEqual(prob.difficulty, "Medium")
        self.assertEqual(prob.base_points, 120)
        self.assertEqual(prob.starter_code, "def testFunc(data):\n    pass")
        self.assertEqual(prob.hidden_test_cases, [{"input": "1", "expected": "2"}])

    def test_add_bonus_questions_from_csv(self):
        with open(self.bonus_csv_path, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['title', 'description', 'starter_code', 'expected_output', 'input_type_hint', 'order', 'duration_minutes'])
            writer.writerow([
                'Bonus 1', 'Desc Bonus', 'print("yes")', 'yes', 'none', '5', '15'
            ])
            
        with patch('builtins.input', return_value=self.bonus_csv_path):
            db_admin.add_bonus_questions_from_csv()
            
        bq = BonusQuestion.objects.filter(order=5).first()
        self.assertIsNotNone(bq)
        self.assertEqual(bq.title, "Bonus 1")
        self.assertEqual(bq.expected_output, "yes")
        self.assertEqual(bq.duration_minutes, 15)

    def test_delete_question_standard_problem(self):
        prob = Problem.objects.create(
            id=101, title="Delete Me", description="Desc", difficulty="Easy",
            function_name="sol", input_variable="n", base_points=100
        )
        
        inputs = ['1', '101', 'yes']
        with patch('builtins.input', side_effect=inputs):
            db_admin.delete_question()
            
        self.assertFalse(Problem.objects.filter(id=101).exists())

    def test_delete_question_bonus_question(self):
        bq = BonusQuestion.objects.create(
            order=10, title="Delete Me Bonus", description="Desc",
            starter_code="pass", expected_output="ok"
        )
        
        inputs = ['2', '10', 'yes']
        with patch('builtins.input', side_effect=inputs):
            db_admin.delete_question()
            
        self.assertFalse(BonusQuestion.objects.filter(order=10).exists())

    def test_delete_all_questions(self):
        Problem.objects.create(
            id=102, title="P1", description="D", difficulty="Easy",
            function_name="sol", input_variable="n", base_points=100
        )
        BonusQuestion.objects.create(
            order=11, title="B1", description="D",
            starter_code="pass", expected_output="ok"
        )
        
        inputs = ['yes', 'DELETE ALL']
        with patch('builtins.input', side_effect=inputs):
            db_admin.delete_all_questions()
            
        self.assertEqual(Problem.objects.count(), 0)
        self.assertEqual(BonusQuestion.objects.count(), 0)