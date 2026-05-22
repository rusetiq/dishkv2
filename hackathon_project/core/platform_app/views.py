import os
import json
import urllib.request as urlreq
import urllib.error
from urllib import request as urllib_request

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.http import JsonResponse
from django.db.models import Sum
from .models import Problem, TeamProgress, HackathonState, BonusQuestion, BonusSubmission
from .utils import run_python_code
from django.utils import timezone
from datetime import timedelta
from django.db.models import Case, When, IntegerField

def logout_view(request):
    auth_logout(request)
    return redirect('/login/')

@login_required
def leaderboard(request):
    state = HackathonState.objects.first()
    if not state:
        return redirect('waiting_room')
    if not state.is_started or state.is_paused:
        return redirect('waiting_room')

    # Regular points from problems
    team_scores = TeamProgress.objects.filter(
        team__is_staff=False
    ).values('team__username').annotate(
        problem_score=Sum('points')
    )

    # Bonus points
    bonus_scores = BonusSubmission.objects.filter(
        is_correct=True
    ).values('team__username').annotate(
        bonus_score=Sum('points_awarded')
    )

    # Merge into a dict
    bonus_map = {b['team__username']: b['bonus_score'] for b in bonus_scores}

    teams = []
    for t in team_scores:
        username = t['team__username']
        total = (t['problem_score'] or 0) + bonus_map.get(username, 0)
        teams.append({'team__username': username, 'total_score': total})

    # Sort by total
    teams = sorted(teams, key=lambda x: x['total_score'], reverse=True)

    start_time = state.start_time
    end_time = start_time + timedelta(hours=2)
    return render(request, 'leaderboard.html', {
        'teams': teams,
        'end_time': end_time.isoformat()
    })

@login_required
def waiting_room(request):
    state = HackathonState.objects.first()
    if state and state.is_started and not state.is_finished:
        return redirect('home')
    return render(request, 'waiting_room.html')


@login_required
def home(request):
    state = HackathonState.objects.first()

    if not state:
        return redirect('waiting_room')

    if state.is_finished:
        return redirect('waiting_room')

    if not state.is_started or state.is_paused:
        return redirect('waiting_room')

    problems = Problem.objects.all().order_by(
    Case(
        When(difficulty='Easy', then=0),
        When(difficulty='Medium', then=1),
        When(difficulty='Hard', then=2),
        output_field=IntegerField()
    )
)

    bonus_points = BonusSubmission.objects.filter(team=request.user, is_correct=True).aggregate(s=Sum('points_awarded'))['s'] or 0
    total_score = sum(tp.points for tp in TeamProgress.objects.filter(team=request.user)) + bonus_points
    solved_count = TeamProgress.objects.filter(team=request.user, is_solved=True).count()
    # 🔥 ADD THIS
    end_time = state.start_time + timedelta(hours=2)


    return render(request, 'home.html', {
    'problems': problems,
    'total_score': total_score,
    'solved_count': solved_count,
    'end_time': end_time.isoformat()   # 👈 THIS is what JS needs
})

@login_required
def problem_detail(request, problem_id):
    state = HackathonState.objects.first()
    if not state:
        return redirect('waiting_room')

    if not state.is_started or state.is_paused:
        return redirect('waiting_room')

    end_time = state.start_time + timedelta(hours=2)
    problem = get_object_or_404(Problem, id=problem_id)
    progress, created = TeamProgress.objects.get_or_create(
    team=request.user,
    problem=problem
)

    if created:
        progress.current_code = problem.starter_code
        progress.save()
    bonus_points = BonusSubmission.objects.filter(team=request.user, is_correct=True).aggregate(s=Sum('points_awarded'))['s'] or 0
    total_score = sum(tp.points for tp in TeamProgress.objects.filter(team=request.user)) + bonus_points
    prev_id = problem_id - 1 if problem_id > 1 else None
    next_id = problem_id + 1 if Problem.objects.filter(id=problem_id+1).exists() else None

    return render(request, 'problem.html', {
        'end_time': end_time.isoformat(),
        'problem': problem,
        'progress': progress,
        'total_score': total_score,
        'prev_id': prev_id,
        'next_id': next_id,
        'hints_enabled': state.hints_enabled,
        'onboarding_tour_enabled': state.onboarding_tour_enabled,
    })

# API for Save/Load/Submit
@login_required
def save_code(request):
    if request.method == "POST":
        p_id = request.POST.get('problem_id')
        code = request.POST.get('code')
        TeamProgress.objects.filter(team=request.user, problem_id=p_id).update(current_code=code)
        return JsonResponse({'status': 'Saved'})

@login_required
def load_code(request, problem_id):
    progress = TeamProgress.objects.get(team=request.user, problem_id=problem_id)
    return JsonResponse({'code': progress.current_code})

def run_leetcode_code(user_code, input_data, problem):
    driver = f"""
import json
import inspect

def _run_leetcode_style():
    func_name = {repr(problem.function_name)}
    g = globals()
    func = None
    if func_name in g:
        func = g[func_name]
    elif "Solution" in g:
        sol_class = g["Solution"]
        sol_inst = sol_class()
        if hasattr(sol_inst, func_name):
            func = getattr(sol_inst, func_name)
    
    if not func:
        print(f"Error: Function '{{func_name}}' not found.", file=sys.stderr)
        sys.exit(1)
        
    input_str = sys.stdin.read().strip()
    if not input_str:
        return
        
    try:
        parsed_input = eval(input_str)
    except Exception:
        lines = [line.strip() for line in input_str.split('\\n') if line.strip()]
        parsed_input = []
        for line in lines:
            try:
                parsed_input.append(eval(line))
            except Exception:
                parsed_input.append(line)
                
    sig = inspect.signature(func)
    params = list(sig.parameters.values())
    expected_args_count = len([p for p in params if p.name != 'self' and p.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)])
    
    if expected_args_count > 1:
        if isinstance(parsed_input, tuple):
            args = parsed_input
        elif isinstance(parsed_input, list) and len(parsed_input) == expected_args_count:
            args = tuple(parsed_input)
        else:
            args = (parsed_input,)
    else:
        args = (parsed_input,)
        
    if func_name == "firstBadVersion" or "firstBadVersion" in g or "First Bad Version" in {repr(problem.title)}:
        bad_version = 0
        lines = [line.strip() for line in input_str.split('\\n') if line.strip()]
        if len(lines) >= 2:
            try:
                bad_version = int(lines[1])
            except:
                pass
        g['isBadVersion'] = lambda v: v >= bad_version
        
    try:
        res = func(*args)
        if res is True:
            print("True")
        elif res is False:
            print("False")
        elif res is None:
            print("None")
        elif isinstance(res, (list, dict, tuple)):
            print(json.dumps(res))
        else:
            print(str(res))
    except Exception as e:
        print(f"Runtime Error: {{type(e).__name__}}: {{e}}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    _run_leetcode_style()
"""
    full_code = user_code + "\n" + driver
    return run_python_code(full_code, input_data, inject_var=None)

@login_required
def submit_code(request):
    if request.method == "POST":
        p_id = request.POST.get('problem_id')
        user_code = request.POST.get('code')
        problem = get_object_or_404(Problem, id=p_id)
        progress = get_object_or_404(TeamProgress, team=request.user, problem=problem)
        state = HackathonState.objects.first()
        if not state or not state.is_started or state.is_finished or state.is_paused:
            return JsonResponse({'status': 'Hackathon is not active.'})
        
        for case in problem.hidden_test_cases:
            try:
                input_data = case['input']
                expected = case['expected']

                output, error = run_leetcode_code(user_code, input_data, problem)

                if error:
                    return JsonResponse({
                        'status': 'Runtime Error',
                        'error': error
                    })

                if output.strip() != str(expected).strip():
                    return JsonResponse({'status': 'Wrong Answer'})

            except Exception as e:
                return JsonResponse({
                    'status': 'Runtime Error',
                    'error': str(e)
                })

        if not progress.is_solved:
            elapsed = (timezone.now() - state.start_time).total_seconds()
            time_penalty = int(elapsed / 120)
            final_points = max(20, problem.base_points - time_penalty)
            
            progress.points = final_points
            progress.is_solved = True
            progress.save()

        new_total = sum(tp.points for tp in TeamProgress.objects.filter(team=request.user))
        
        return JsonResponse({
            'status': 'Correct Answer!', 
            'new_total': new_total
        })

@login_required
def bonus_status(request):
    state = HackathonState.objects.first()
    if not state or not state.start_time:
        return JsonResponse({'available': False})

    bonus = BonusQuestion.objects.first()
    if not bonus or not bonus.is_active:
        return JsonResponse({'available': False})

    elapsed_minutes = (timezone.now() - state.start_time).total_seconds() / 60
    if elapsed_minutes < bonus.appear_after_minutes:
        return JsonResponse({'available': False})

    if not bonus.activated_at:
        bonus.activated_at = timezone.now()
        bonus.save()

    if bonus.is_paused:
        open_seconds = (bonus.paused_at - bonus.activated_at).total_seconds()
    else:
        open_seconds = (timezone.now() - bonus.activated_at).total_seconds()
    duration_seconds = bonus.duration_minutes * 60

    winners_so_far = BonusSubmission.objects.filter(bonus=bonus, is_correct=True).count()
    
    time_expired = open_seconds >= duration_seconds
    spots_full = winners_so_far >= bonus.max_winners
    expired = time_expired or spots_full

    already_solved = BonusSubmission.objects.filter(
        bonus=bonus, team=request.user, is_correct=True
    ).exists()

    already_submitted = BonusSubmission.objects.filter(
        bonus=bonus, team=request.user
    ).exists()

    time_remaining_seconds = max(0, int(duration_seconds - open_seconds))

    available = not expired and not already_submitted and not bonus.is_paused

    return JsonResponse({
        'available': available,
        'expired': expired,
        'already_solved': already_solved,
        'already_submitted': already_submitted,
        'title': bonus.title,
        'description': bonus.description,
        'starter_code': bonus.starter_code,
        'input_type_hint': bonus.input_type_hint,
        'winners_so_far': winners_so_far,
        'max_winners': bonus.max_winners,
        'max_points': bonus.max_points,
        'points_step': bonus.points_step,
        'points_if_next': max(0, bonus.max_points - (winners_so_far * bonus.points_step)),
        'time_remaining_seconds': time_remaining_seconds,
        'duration_minutes': bonus.duration_minutes,
    })
@login_required
def bonus_submit(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error'})

    bonus = BonusQuestion.objects.first()
    if not bonus or not bonus.is_active:
        return JsonResponse({'status': 'Bonus not active'})

    if BonusSubmission.objects.filter(bonus=bonus, team=request.user, is_correct=True).exists():
        return JsonResponse({'status': 'Already submitted'})

    winners_so_far = BonusSubmission.objects.filter(bonus=bonus, is_correct=True).count()
    if winners_so_far >= bonus.max_winners:
        return JsonResponse({'status': 'Bonus closed — all spots taken'})

    if bonus.activated_at:
        open_minutes = (timezone.now() - bonus.activated_at).total_seconds() / 60
        if open_minutes >= bonus.duration_minutes:
            return JsonResponse({'status': 'Bonus round has expired'})

    user_input = request.POST.get('user_input', '').strip()
    output, error = run_python_code(bonus.starter_code, user_input)

    if error:
        return JsonResponse({'status': 'Runtime Error', 'error': error})

    is_correct = output.strip() == bonus.expected_output.strip()
    points_awarded = 0

    if is_correct:
        winners_so_far = BonusSubmission.objects.filter(bonus=bonus, is_correct=True).count()
        if winners_so_far < bonus.max_winners:
            points_awarded = max(0, bonus.max_points - (winners_so_far * bonus.points_step))

    if not is_correct:
        return JsonResponse({'status': 'Wrong Answer — check your input format.'})

    BonusSubmission.objects.create(
        team=request.user, bonus=bonus,
        submitted_input=user_input,
        is_correct=True,
        points_awarded=points_awarded,
    )

    if is_correct and points_awarded > 0:
        new_total = (
            sum(tp.points for tp in TeamProgress.objects.filter(team=request.user))
            + (BonusSubmission.objects.filter(team=request.user, is_correct=True).aggregate(s=Sum('points_awarded'))['s'] or 0)
        )
        return JsonResponse({'status': 'Correct!', 'points_awarded': points_awarded, 'new_total': new_total})
    elif is_correct:
        return JsonResponse({'status': 'Correct! But all point slots were just taken.'})
    else:
        return JsonResponse({'status': 'Wrong Answer — check your input format.'})
@login_required
def check_hackathon_status(request):
    state = HackathonState.objects.first()

    if not state or not state.start_time:
        return JsonResponse({
            'is_finished': False,
            'is_live': False
        })

    end_time = state.start_time + timedelta(hours=2)

    if timezone.now() >= end_time:
        state.is_finished = True
        state.save()

    is_finished = state.is_finished
    is_live = state.is_started and not state.is_finished and not state.is_paused

    return JsonResponse({
        'is_finished': is_finished,
        'is_live': is_live,
        'is_paused': state.is_paused
    })
@login_required
def run_code_custom(request):
    if request.method == "POST":
        p_id = request.POST.get('problem_id')
        user_code = request.POST.get('code')
        problem = get_object_or_404(Problem, id=p_id)
        cases = problem.hidden_test_cases[:3]
        results = []
        overall_status = "Accepted"
        for case in cases:
            input_data = case.get('input', '')
            expected = case.get('expected', '')
            try:
                output, error = run_leetcode_code(user_code, input_data, problem)
                if error:
                    status = "Runtime Error"
                    overall_status = "Runtime Error"
                elif output.strip() != str(expected).strip():
                    status = "Wrong Answer"
                    if overall_status == "Accepted":
                        overall_status = "Wrong Answer"
                else:
                    status = "Accepted"
            except Exception as e:
                output = ""
                error = str(e)
                status = "Runtime Error"
                overall_status = "Runtime Error"
            results.append({
                'input': input_data,
                'expected': expected,
                'output': output,
                'error': error,
                'status': status
            })
        return JsonResponse({
            'status': overall_status,
            'results': results
        })
@login_required
def ai_hint(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    state = HackathonState.objects.first()
    if state and not state.hints_enabled:
        return JsonResponse({'hint': 'AI hints have been disabled by the admin for this event.'}, status=200)

    problem_id = request.POST.get('problem_id')
    current_code = request.POST.get('code', '')

    problem = get_object_or_404(Problem, id=problem_id)

    from django.conf import settings
    api_key = getattr(settings, 'GEMINI_API_KEY', '')
    if not api_key:
        return JsonResponse({'hint': 'AI hints are not configured. Ask your admin to set GEMINI_API_KEY.'})

    console_output = request.POST.get('console_output', '').strip()
    model_name = (state.ai_model if state and state.ai_model else 'gemini-3.1-flash-lite')

    code_block = current_code.strip() if current_code.strip() else '(empty — student has not written anything yet)'

    console_section = ''
    if console_output:
        console_section = f'\n\nLatest console output / error when they ran the code:\n```\n{console_output}\n```\nIf this shows an error or wrong answer, prioritize addressing it in your hint.'

    prompt = f"""You are a helpful coding tutor for a Python hackathon. Help the student with this problem.

Problem: {problem.title}
Description: {problem.description}

Student's current code:
```python
{code_block}
```{console_section}

Give a helpful hint to guide them toward the solution WITHOUT giving away the full answer.
Be encouraging, concise (2-4 sentences max), and specific to their code and any errors shown.
Focus on the approach/algorithm, not the exact implementation."""

    payload = json.dumps({
        'contents': [{'parts': [{'text': prompt}]}],
        'generationConfig': {'maxOutputTokens': 300, 'temperature': 0.7}
    }).encode()

    req = urlreq.Request(
        f'https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}',
        data=payload,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    try:
        with urlreq.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            hint_text = data['candidates'][0]['content']['parts'][0]['text']
            return JsonResponse({'hint': hint_text})
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors='ignore')
        return JsonResponse({'hint': f'API error {e.code}: {body}'})
    except Exception as e:
        return JsonResponse({'hint': f'Could not load hint: {e}'})

@login_required
def features(request):
    state = HackathonState.objects.first()
    return JsonResponse({
        'hints_enabled': state.hints_enabled if state else True,
        'onboarding_tour_enabled': state.onboarding_tour_enabled if state else True,
    })

@login_required
def finished(request):
    state = HackathonState.objects.first()
    if not TeamProgress.objects.filter(team=request.user).exists():
        return redirect('waiting_room')
    if state and state.is_started and not state.is_finished:
        if state.is_paused:
            return redirect('waiting_room')
        return redirect('home')
    bonus_points = BonusSubmission.objects.filter(team=request.user, is_correct=True).aggregate(s=Sum('points_awarded'))['s'] or 0
    total_score = sum(tp.points for tp in TeamProgress.objects.filter(team=request.user)) + bonus_points
    return render(request, 'finished.html', {'total_score': total_score})

@login_required
def admin_start_hackathon(request):
    if not request.user.is_staff:
        return redirect('waiting_room')
    state, _ = HackathonState.objects.get_or_create(id=1)
    state.is_started = True
    state.is_finished = False
    state.is_paused = False
    state.paused_at = None
    state.start_time = timezone.now()
    state.save()
    return redirect('/admin/')

@login_required
def admin_pause_hackathon(request):
    if not request.user.is_staff:
        return redirect('waiting_room')
    state = HackathonState.objects.first()
    if state and state.is_started and not state.is_finished and not state.is_paused:
        state.is_paused = True
        state.paused_at = timezone.now()
        state.save()
    return redirect('/admin/')

@login_required
def admin_resume_hackathon(request):
    if not request.user.is_staff:
        return redirect('waiting_room')
    state = HackathonState.objects.first()
    if state and state.is_started and not state.is_finished and state.is_paused:
        if state.paused_at and state.start_time:
            duration = timezone.now() - state.paused_at
            state.start_time = state.start_time + duration
        state.is_paused = False
        state.paused_at = None
        state.save()
    return redirect('/admin/')

@login_required
def admin_end_hackathon(request):
    if not request.user.is_staff:
        return redirect('waiting_room')
    state = HackathonState.objects.first()
    if state:
        state.is_finished = True
        state.is_paused = False
        state.paused_at = None
        state.save()
    return redirect('/admin/')

@login_required
def admin_start_bonus(request):
    if not request.user.is_staff:
        return redirect('waiting_room')
    bonus = BonusQuestion.objects.first()
    if bonus:
        bonus.is_active = True
        bonus.is_paused = False
        bonus.paused_at = None
        bonus.activated_at = timezone.now()
        bonus.save()
    return redirect('/admin/')

@login_required
def admin_pause_bonus(request):
    if not request.user.is_staff:
        return redirect('waiting_room')
    bonus = BonusQuestion.objects.first()
    if bonus and bonus.is_active and not bonus.is_paused:
        bonus.is_paused = True
        bonus.paused_at = timezone.now()
        bonus.save()
    return redirect('/admin/')

@login_required
def admin_resume_bonus(request):
    if not request.user.is_staff:
        return redirect('waiting_room')
    bonus = BonusQuestion.objects.first()
    if bonus and bonus.is_active and bonus.is_paused:
        if bonus.paused_at and bonus.activated_at:
            duration = timezone.now() - bonus.paused_at
            bonus.activated_at = bonus.activated_at + duration
        bonus.is_paused = False
        bonus.paused_at = None
        bonus.save()
    return redirect('/admin/')

@login_required
def admin_end_bonus(request):
    if not request.user.is_staff:
        return redirect('waiting_room')
    bonus = BonusQuestion.objects.first()
    if bonus:
        bonus.is_active = False
        bonus.is_paused = False
        bonus.paused_at = None
        bonus.activated_at = None
        bonus.save()
    return redirect('/admin/')