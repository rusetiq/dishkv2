from django.contrib import admin
from .models import Problem, TeamProgress, HackathonState, BonusQuestion, BonusSubmission

@admin.register(HackathonState)
class StateAdmin(admin.ModelAdmin):
    list_display = ('is_started', 'is_finished')
    def has_add_permission(self, request):
        return not HackathonState.objects.exists()

admin.site.register(Problem)

@admin.register(TeamProgress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('team', 'problem', 'points', 'is_solved')
    list_editable = ('points',)

@admin.register(BonusQuestion)
class BonusAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'appear_after_minutes', 'max_points', 'max_winners', 'duration_minutes')
    list_editable = ('is_active',)
    readonly_fields = ()
    def has_add_permission(self, request):
        return not BonusQuestion.objects.exists()

@admin.register(BonusSubmission)
class BonusSubmissionAdmin(admin.ModelAdmin):
    list_display = ('team', 'bonus', 'is_correct', 'points_awarded', 'submitted_at')
    readonly_fields = ('team', 'bonus', 'submitted_input', 'is_correct', 'points_awarded', 'submitted_at')