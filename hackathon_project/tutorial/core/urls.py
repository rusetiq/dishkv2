from django.contrib import admin
from django.urls import path, include
from platform_app import views 
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.waiting_room, name='waiting_room'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('home/', views.home, name='home'),
    path('problem/<int:problem_id>/', views.problem_detail, name='problem_detail'),
    path('api/save/', views.save_code),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('api/leaderboard-data/', views.leaderboard_data, name='leaderboard_data'),
    path('api/load/<int:problem_id>/', views.load_code),
    path('api/run-custom/', views.run_code_custom, name='run_custom'),
    path('api/submit/', views.submit_code, name='submit_code'),
    path('check-status/', views.check_hackathon_status, name='check_status_page'),
    path('logout/', views.logout_view, name='logout'),
    path('accounts/logout/', views.logout_view),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/status/', views.check_hackathon_status, name='check_status'),
    path('finished/', views.finished, name='finished'),
    path('bonus/', views.bonus_page, name='bonus'),
    path('api/bonus/status/', views.bonus_status, name='bonus_status'),
    path('api/bonus/submit/', views.bonus_submit, name='bonus_submit'),
    path('api/hint/', views.ai_hint, name='ai_hint'),
    path('api/features/', views.features, name='features'),
    path('api/hint-tokens/', views.get_hint_tokens, name='get_hint_tokens'),
    path('api/earn-hint/', views.earn_hint_token, name='earn_hint_token'),
    path('admin-api/start-hackathon/', views.admin_start_hackathon, name='admin_start_hackathon'),
    path('admin-api/pause-hackathon/', views.admin_pause_hackathon, name='admin_pause_hackathon'),
    path('admin-api/resume-hackathon/', views.admin_resume_hackathon, name='admin_resume_hackathon'),
    path('admin-api/end-hackathon/', views.admin_end_hackathon, name='admin_end_hackathon'),
    path('admin-api/start-bonus/', views.admin_start_bonus, name='admin_start_bonus'),
    path('admin-api/pause-bonus/', views.admin_pause_bonus, name='admin_pause_bonus'),
    path('admin-api/resume-bonus/', views.admin_resume_bonus, name='admin_resume_bonus'),
    path('admin-api/end-bonus/', views.admin_end_bonus, name='admin_end_bonus'),
    path('admin-api/toggle-hints/', views.admin_toggle_hints, name='admin_toggle_hints'),
    path('admin-api/reset-hackathon/', views.admin_reset_hackathon, name='admin_reset_hackathon'),
    path('admin-api/toggle-tour/', views.admin_toggle_tour, name='admin_toggle_tour'),
    path('admin-api/adjust-points/', views.admin_adjust_points, name='admin_adjust_points'),
    path('admin-answers/', views.admin_answers, name='admin_answers'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)