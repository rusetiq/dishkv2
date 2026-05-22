from django.core.management.base import BaseCommand
from platform_app.models import Problem, TeamProgress
from platform_app.leetcode_data import LEETCODE_PROBLEMS

class Command(BaseCommand):
    def handle(self, *args, **options):
        for p in LEETCODE_PROBLEMS:
            prob, created = Problem.objects.update_or_create(
                id=p["id"],
                defaults={
                    "title": p["title"],
                    "difficulty": p["difficulty"],
                    "function_name": p["function_name"],
                    "base_points": p["base_points"],
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
