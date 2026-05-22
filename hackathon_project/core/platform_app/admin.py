from django.contrib import admin
from django.contrib import messages
from django.utils import timezone
from .models import Problem, TeamProgress, HackathonState, BonusQuestion, BonusSubmission

from django import forms

class HackathonStateForm(forms.ModelForm):
    ai_model = forms.CharField(
        max_length=100,
        help_text='Groq model ID — e.g. llama-3.3-70b-versatile, openai/gpt-oss-120b, groq/compound'
    )
    class Meta:
        model = HackathonState
        fields = '__all__'

@admin.register(HackathonState)
class StateAdmin(admin.ModelAdmin):
    form = HackathonStateForm
    list_display = ('is_started', 'is_finished', 'is_paused', 'hints_enabled', 'ai_model', 'start_time')
    actions = ['start_hackathon_action', 'stop_hackathon_action']
    fieldsets = (
        ('Event Control', {'fields': ('is_started', 'is_finished', 'is_paused', 'start_time', 'paused_at')}),
        ('Feature Flags', {
            'description': 'Toggle these at any time — changes take effect immediately for all teams.',
            'fields': ('hints_enabled', 'onboarding_tour_enabled', 'ai_model'),
        }),
    )
    readonly_fields = ('paused_at',)

    def has_add_permission(self, request):
        return not HackathonState.objects.exists()

    def start_hackathon_action(self, request, queryset):
        for state in queryset:
            state.is_started = True
            state.is_finished = False
            state.start_time = timezone.now()
            state.save()
        self.message_user(request, 'Hackathon started!', messages.SUCCESS)
    start_hackathon_action.short_description = '🚀 Start hackathon now'

    def stop_hackathon_action(self, request, queryset):
        for state in queryset:
            state.is_finished = True
            state.save()
        self.message_user(request, 'Hackathon stopped!', messages.WARNING)
    stop_hackathon_action.short_description = '🛑 Stop hackathon'

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'difficulty', 'points', 'function_name')
    list_filter = ('difficulty',)
    search_fields = ('title', 'description')
    list_editable = ('difficulty', 'points')
    ordering = ('id',)
    fieldsets = (
        ('Problem Info', {'fields': ('title', 'difficulty', 'description', 'examples')}),
        ('Scoring', {'fields': ('points', 'base_points')}),
        ('Code', {'fields': ('function_name', 'input_variable', 'starter_code')}),
        ('Test Cases', {'fields': ('hidden_test_cases',)}),
    )

@admin.register(TeamProgress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('team', 'problem', 'points', 'is_solved')
    list_filter = ('is_solved', 'problem')
    search_fields = ('team__username',)
    list_editable = ('points',)
    actions = ['reset_progress_action']
    
    def reset_progress_action(self, request, queryset):
        queryset.update(points=0, is_solved=False, current_code='')
        self.message_user(request, f'Reset {queryset.count()} progress entries.', messages.WARNING)
    reset_progress_action.short_description = '🔄 Reset selected progress'

@admin.register(BonusQuestion)
class BonusAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'appear_after_minutes', 'max_points', 'max_winners', 'duration_minutes')
    list_editable = ('is_active',)
    fieldsets = (
        ('Question', {'fields': ('title', 'description', 'starter_code', 'expected_output', 'input_type_hint')}),
        ('Timing', {'fields': ('appear_after_minutes', 'duration_minutes')}),
        ('Scoring', {'fields': ('max_points', 'points_step', 'max_winners')}),
        ('Status', {'fields': ('is_active', 'activated_at')}),
    )
    readonly_fields = ('activated_at',)
    
    def has_add_permission(self, request):
        return not BonusQuestion.objects.exists()

@admin.register(BonusSubmission)
class BonusSubmissionAdmin(admin.ModelAdmin):
    list_display = ('team', 'bonus', 'is_correct', 'points_awarded', 'submitted_at')
    list_filter = ('is_correct',)
    search_fields = ('team__username',)
    readonly_fields = ('team', 'bonus', 'submitted_input', 'is_correct', 'points_awarded', 'submitted_at')

admin.site.site_header = 'DIS Hackathon Admin'
admin.site.site_title = 'DIS Admin'
admin.site.index_title = 'Control Panel'

original_index = admin.site.index
def custom_index(request, extra_context=None):
    if extra_context is None:
        extra_context = {}
    extra_context['h_state'] = HackathonState.objects.first()
    extra_context['b_state'] = BonusQuestion.objects.first()
    return original_index(request, extra_context)
admin.site.index = custom_index