from django.core.management.base import BaseCommand
from platform_app.models import Problem, TeamProgress, BonusQuestion
from platform_app.leetcode_data import LEETCODE_PROBLEMS, BONUS_QUESTIONS

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Seed regular problems
        for p in LEETCODE_PROBLEMS:
            prob, created = Problem.objects.update_or_create(
                id=p["id"],
                defaults={
                    "title": p["title"],
                    "difficulty": p["difficulty"],
                    "function_name": p["function_name"],
                    "base_points": p["base_points"],
                    "points": p["base_points"],
                    "starter_code": p["starter_code"],
                    "description": p["description"],
                    "examples": p["examples"],
                    "input_variable": p["input_variable"],
                    "hidden_test_cases": p["hidden_test_cases"]
                }
            )
            action = "Created" if created else "Updated"
            self.stdout.write(f"{action} problem: {prob.title}")
            TeamProgress.objects.filter(problem=prob, is_solved=False).update(current_code=prob.starter_code)

        # Seed bonus questions
        for b in BONUS_QUESTIONS:
            bq, created = BonusQuestion.objects.update_or_create(
                order=b["order"],
                defaults={
                    "title": b["title"],
                    "description": b["description"],
                    "starter_code": b["starter_code"],
                    "expected_output": b["expected_output"],
                    "input_type_hint": b["input_type_hint"],
                    "duration_minutes": b["duration_minutes"]
                }
            )
            action = "Created" if created else "Updated"
            self.stdout.write(f"{action} bonus question {bq.order}: {bq.title}")

