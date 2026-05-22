from django.db import models
from django.contrib.auth.models import User

class HackathonState(models.Model):
    AI_MODEL_CHOICES = [
        ('llama-3.3-70b-versatile', 'Llama 3.3 70B Versatile'),
        ('openai/gpt-oss-120b', 'GPT OSS 120B'),
        ('groq/compound', 'Groq Compound'),
    ]
    is_started = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    is_paused = models.BooleanField(default=False)
    paused_at = models.DateTimeField(null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    hints_enabled = models.BooleanField(default=True, help_text='Allow teams to request AI hints on problem pages')
    onboarding_tour_enabled = models.BooleanField(default=True, help_text='Show the guided UI tour to teams on their first visit to a problem')
    ai_model = models.CharField(max_length=100, choices=AI_MODEL_CHOICES, default='llama-3.3-70b-versatile', help_text='Groq model used for AI hints — change takes effect immediately')

    class Meta:
        verbose_name_plural = "Hackathon State"
class Problem(models.Model):
    DIFFICULTY_CHOICES = [('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')]
    input_variable = models.CharField(max_length=100, default="n", help_text="Variable name injected into student code e.g. 'n', 'data', 'nums'")
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='Easy')
    hidden_test_cases = models.JSONField(default=list) 
    points = models.IntegerField(default=100)
    function_name = models.CharField(max_length=100, default="solution")
    base_points = models.IntegerField(default=100)
    starter_code = models.TextField(blank=True, default="")
    examples = models.TextField(blank=True, default="")

    def __str__(self):
        return self.title



class TeamProgress(models.Model):
    team = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    current_code = models.TextField(default="# Write Python code here\n# Use print() for output\n")
    points = models.IntegerField(default=0)
    is_solved = models.BooleanField(default=False)
    start_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        unique_together = ('team', 'problem')
class BonusQuestion(models.Model):
    APPEAR_CHOICES = [
        (60,  'After 1 hour'),
        (90,  'After 1.5 hours'),
        (120, 'After 2 hours'),
    ]
    title = models.CharField(max_length=200, default="Bonus Round")
    description = models.TextField()
    starter_code = models.TextField()
    expected_output = models.CharField(max_length=500)
    input_type_hint = models.CharField(max_length=200, blank=True, default="")
    max_points = models.IntegerField(default=200)
    points_step = models.IntegerField(default=15)
    max_winners = models.IntegerField(default=4)
    duration_minutes = models.IntegerField(default=7)
    appear_after_minutes = models.IntegerField(default=120, choices=APPEAR_CHOICES)
    is_active = models.BooleanField(default=False)
    is_paused = models.BooleanField(default=False)
    paused_at = models.DateTimeField(null=True, blank=True)
    activated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Bonus Question"
        verbose_name_plural = "Bonus Question"

    def __str__(self):
        return self.title


class BonusSubmission(models.Model):
    team = models.ForeignKey(User, on_delete=models.CASCADE)
    bonus = models.ForeignKey(BonusQuestion, on_delete=models.CASCADE)
    submitted_input = models.TextField()
    is_correct = models.BooleanField(default=False)
    points_awarded = models.IntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('team', 'bonus')