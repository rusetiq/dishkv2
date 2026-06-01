import json
import urllib.request as urlreq
import urllib.error

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Sum, Count
from django.db import transaction
from django.views.decorators.http import require_POST
from .models import Problem, TeamProgress, HackathonState, BonusQuestion, BonusSubmission, PointAdjustment
from .utils import run_python_code
from django.utils import timezone
from datetime import timedelta
from django.db.models import Case, When, IntegerField


def _get_total_score(user):
    problem_pts = sum(tp.points for tp in TeamProgress.objects.filter(team=user))
    bonus_pts = BonusSubmission.objects.filter(team=user, is_correct=True).aggregate(s=Sum('points_awarded'))['s'] or 0
    adj_pts = PointAdjustment.objects.filter(team=user).aggregate(s=Sum('delta'))['s'] or 0
    return problem_pts + bonus_pts + adj_pts


@require_POST
def logout_view(request):
    auth_logout(request)
    return redirect('/login/')

@login_required
def leaderboard(request):
    state = HackathonState.objects.first()

    team_scores = TeamProgress.objects.filter(
        team__is_staff=False
    ).values('team__username').annotate(
        problem_score=Sum('points')
    )

    bonus_scores = BonusSubmission.objects.filter(
        is_correct=True
    ).values('team__username').annotate(
        bonus_score=Sum('points_awarded')
    )

    adjustment_scores = PointAdjustment.objects.values('team__username').annotate(
        adj_score=Sum('delta')
    )

    team_scores_map = {t['team__username']: t['problem_score'] or 0 for t in team_scores}
    bonus_map = {b['team__username']: b['bonus_score'] or 0 for b in bonus_scores}
    adj_map = {a['team__username']: a['adj_score'] or 0 for a in adjustment_scores}

    all_teams = User.objects.filter(is_staff=False)
    teams = []
    for team in all_teams:
        username = team.username
        total = team_scores_map.get(username, 0) + bonus_map.get(username, 0) + adj_map.get(username, 0)
        teams.append({'team__username': username, 'total_score': total})

    teams = sorted(teams, key=lambda x: x['total_score'], reverse=True)

    end_time_iso = None
    if state and state.start_time:
        dur = state.duration_minutes if state.duration_minutes else 120
        end_time_iso = (state.start_time + timedelta(minutes=dur)).isoformat()

    return render(request, 'leaderboard.html', {
        'teams': teams,
        'end_time': end_time_iso
    })

@login_required
def leaderboard_data(request):
    team_scores = TeamProgress.objects.filter(
        team__is_staff=False
    ).values('team__username').annotate(
        problem_score=Sum('points')
    )
    bonus_scores = BonusSubmission.objects.filter(
        is_correct=True
    ).values('team__username').annotate(
        bonus_score=Sum('points_awarded')
    )
    adjustment_scores = PointAdjustment.objects.values('team__username').annotate(
        adj_score=Sum('delta')
    )

    team_scores_map = {t['team__username']: t['problem_score'] or 0 for t in team_scores}
    bonus_map = {b['team__username']: b['bonus_score'] or 0 for b in bonus_scores}
    adj_map = {a['team__username']: a['adj_score'] or 0 for a in adjustment_scores}

    all_teams = User.objects.filter(is_staff=False)
    teams = []
    for team in all_teams:
        username = team.username
        total = team_scores_map.get(username, 0) + bonus_map.get(username, 0) + adj_map.get(username, 0)
        teams.append({'username': username, 'score': total})
    teams = sorted(teams, key=lambda x: x['score'], reverse=True)
    return JsonResponse({'teams': teams})


@login_required
def waiting_room(request):
    state = HackathonState.objects.first()
    if state and state.is_started and not state.is_finished:
        return redirect('home')
    return render(request, 'waiting_room.html', {
        'onboarding_tour_enabled': state.onboarding_tour_enabled if state else True
    })


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

    solved_problem_ids = set(TeamProgress.objects.filter(team=request.user, is_solved=True).values_list('problem_id', flat=True))
    total_score = _get_total_score(request.user)
    solved_count = TeamProgress.objects.filter(team=request.user, is_solved=True).count()
    dur = state.duration_minutes if state.duration_minutes else 120
    end_time = state.start_time + timedelta(minutes=dur)

    all_teams = User.objects.filter(is_staff=False)
    team_scores = {t['team__username']: t['problem_score'] or 0 for t in TeamProgress.objects.filter(team__is_staff=False).values('team__username').annotate(problem_score=Sum('points'))}
    bonus_scores = {b['team__username']: b['bonus_score'] or 0 for b in BonusSubmission.objects.filter(is_correct=True).values('team__username').annotate(bonus_score=Sum('points_awarded'))}
    adj_scores = {a['team__username']: a['adj_score'] or 0 for a in PointAdjustment.objects.values('team__username').annotate(adj_score=Sum('delta'))}

    teams_list = []
    for team in all_teams:
        username = team.username
        total = team_scores.get(username, 0) + bonus_scores.get(username, 0) + adj_scores.get(username, 0)
        teams_list.append({'username': username, 'score': total})

    teams_list = sorted(teams_list, key=lambda x: x['score'], reverse=True)
    my_rank = "—"
    for index, team in enumerate(teams_list):
        if team['username'] == request.user.username:
            my_rank = index + 1
            break

    return render(request, 'home.html', {
        'problems': problems,
        'solved_problem_ids': solved_problem_ids,
        'total_score': total_score,
        'solved_count': solved_count,
        'end_time': end_time.isoformat(),
        'rank': my_rank
    })

@login_required
def problem_detail(request, problem_id):
    state = HackathonState.objects.first()
    if not state:
        return redirect('waiting_room')

    if not state.is_started or state.is_paused:
        return redirect('waiting_room')

    dur = state.duration_minutes if state.duration_minutes else 120
    end_time = state.start_time + timedelta(minutes=dur)
    problem = get_object_or_404(Problem, id=problem_id)
    progress, created = TeamProgress.objects.get_or_create(
    team=request.user,
    problem=problem
)

    if created:
        progress.current_code = problem.starter_code
        progress.save()
    total_score = _get_total_score(request.user)
    all_problem_ids = list(Problem.objects.order_by(
        Case(
            When(difficulty='Easy', then=0),
            When(difficulty='Medium', then=1),
            When(difficulty='Hard', then=2),
            output_field=IntegerField()
        ), 'id'
    ).values_list('id', flat=True))
    try:
        current_idx = all_problem_ids.index(problem_id)
    except ValueError:
        current_idx = -1
    prev_id = all_problem_ids[current_idx - 1] if current_idx > 0 else None
    next_id = all_problem_ids[current_idx + 1] if current_idx >= 0 and current_idx < len(all_problem_ids) - 1 else None

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

@login_required
@require_POST
def save_code(request):
    p_id = request.POST.get('problem_id')
    code = request.POST.get('code', '')
    if len(code) > 50000:
        return JsonResponse({'error': 'Code too large'}, status=400)
    updated = TeamProgress.objects.filter(team=request.user, problem_id=p_id).update(current_code=code)
    if not updated:
        return JsonResponse({'error': 'Progress not found'}, status=404)
    return JsonResponse({'status': 'Saved'})

@login_required
def load_code(request, problem_id):
    try:
        progress = TeamProgress.objects.get(team=request.user, problem_id=problem_id)
    except TeamProgress.DoesNotExist:
        problem = get_object_or_404(Problem, id=problem_id)
        return JsonResponse({'code': problem.starter_code})
    return JsonResponse({'code': progress.current_code})

def run_leetcode_code(user_code, input_data_list, problem):
    driver = f"""
import json
import ast

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
        raise AttributeError(f"Error: Function '{{func_name}}' not found.")
        
    lines = []
    while True:
        try:
            lines.append(input())
        except EOFError:
            break
    input_str = "\\n".join(lines).strip()
    if not input_str:
        return
        
    inputs = json.loads(input_str)
    expected_args_count = func.__code__.co_argcount - (1 if hasattr(func, '__self__') else 0)
    
    res_list = []
    for inp in inputs:
        try:
            try:
                parsed_input = ast.literal_eval(inp)
            except Exception:
                lines_split = [line.strip() for line in inp.split('\\n') if line.strip()]
                parsed_input = []
                for line in lines_split:
                    try:
                        parsed_input.append(ast.literal_eval(line))
                    except Exception:
                        parsed_input.append(line)
            
            if expected_args_count > 1:
                if isinstance(parsed_input, tuple):
                    args = parsed_input
                elif isinstance(parsed_input, list) and len(parsed_input) == expected_args_count:
                    args = tuple(parsed_input)
                else:
                    args = (parsed_input,)
            else:
                args = (parsed_input,)
                
            if func_name == "firstBadVersion" or "firstBadVersion" in g or "First Bad Version" in {repr(problem.title)} or func_name == "find_first_defective" or "find_first_defective" in g or "Defective Product" in {repr(problem.title)}:
                bad_version = 0
                lines_split = [line.strip() for line in inp.split('\\n') if line.strip()]
                if len(lines_split) >= 2:
                    try:
                        bad_version = int(lines_split[1])
                    except:
                        pass
                g['isBadVersion'] = lambda v: v >= bad_version
                g['is_defective'] = lambda v: v >= bad_version
                
            res = func(*args)
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
            res_list.append({{'output': out, 'error': '', 'status': 'Accepted'}})
        except Exception as e:
            res_list.append({{'output': '', 'error': f"{{type(e).__name__}}: {{e}}", 'status': 'Runtime Error'}})
            
    print("RESULT:" + json.dumps(res_list))

if __name__ == "__main__":
    _run_leetcode_style()
"""
    full_code = user_code + "\n" + driver
    stdout, stderr = run_python_code(full_code, json.dumps(input_data_list), inject_var=None)
    if stderr:
        return None, stderr
    result_prefix = "RESULT:"
    result_line = None
    for line in stdout.split('\n'):
        if line.startswith(result_prefix):
            result_line = line[len(result_prefix):]
            break
    if result_line is None:
        return None, stdout or "Unknown error occurred"
    try:
        return json.loads(result_line), None
    except Exception as e:
        return None, f"JSON parse error of driver output: {e}"

@login_required
@require_POST
def submit_code(request):
    if request.user.is_staff:
        return JsonResponse({'status': 'Staff accounts cannot submit.'})
    p_id = request.POST.get('problem_id')
    user_code = request.POST.get('code')
    problem = get_object_or_404(Problem, id=p_id)
    progress = get_object_or_404(TeamProgress, team=request.user, problem=problem)
    state = HackathonState.objects.first()
    if not state or not state.is_started or state.is_finished or state.is_paused:
        return JsonResponse({'status': 'Hackathon is not active.'})
    
    input_list = [case['input'] for case in problem.hidden_test_cases]
    results, error = run_leetcode_code(user_code, input_list, problem)

    if error:
        return JsonResponse({
            'status': 'Runtime Error',
            'error': error
        })

    for case, res in zip(problem.hidden_test_cases, results):
        if res['status'] == 'Runtime Error':
            return JsonResponse({
                'status': 'Runtime Error',
                'error': res['error']
            })
        expected = case['expected']
        output = res['output']
        if output is None or output.strip() != str(expected).strip():
            return JsonResponse({'status': 'Wrong Answer'})

    if not progress.is_solved:
        elapsed = (timezone.now() - state.start_time).total_seconds()
        time_penalty = int(elapsed / 120)
        final_points = max(20, problem.base_points - time_penalty)
        
        progress.points = final_points
        progress.is_solved = True
        progress.save()

    new_total = _get_total_score(request.user)
    
    return JsonResponse({
        'status': 'Correct Answer!', 
        'new_total': new_total
    })

@login_required
def bonus_status(request):
    questions = BonusQuestion.objects.all().order_by('order')
    if not questions.exists():
        return JsonResponse({
            'active': False,
            'available': False,
            'expired': False,
            'questions': [],
        })

    first_q = questions.first()
    
    if not first_q.is_active:
        return JsonResponse({
            'active': False,
            'available': False,
            'expired': False,
            'questions': [],
        })

    if first_q.is_paused:
        open_seconds = (first_q.paused_at - first_q.activated_at).total_seconds()
    else:
        open_seconds = (timezone.now() - first_q.activated_at).total_seconds()
    duration_seconds = first_q.duration_minutes * 60

    time_expired = open_seconds >= duration_seconds
    time_remaining_seconds = max(0, int(duration_seconds - open_seconds))

    state = HackathonState.objects.first()
    first_finisher = state.bonus_first_finisher if state else None

    solved_question_ids = set(
        BonusSubmission.objects.filter(
            team=request.user, is_correct=True, bonus__in=questions
        ).values_list('bonus_id', flat=True)
    )

    all_solved = len(solved_question_ids) == questions.count() and questions.count() > 0

    question_list = []
    for q in questions:
        question_list.append({
            'id': q.id,
            'order': q.order,
            'title': q.title,
            'description': q.description,
            'starter_code': q.starter_code,
            'input_type_hint': q.input_type_hint,
            'solved': q.id in solved_question_ids,
        })

    active = first_q.is_active
    expired = time_expired
    available = active and not expired and not all_solved and not first_q.is_paused

    return JsonResponse({
        'active': active,
        'available': available,
        'expired': expired,
        'all_solved': all_solved,
        'is_paused': first_q.is_paused,
        'first_finisher': first_finisher.username if first_finisher else None,
        'is_first_finisher': first_finisher == request.user if first_finisher else False,
        'time_remaining_seconds': time_remaining_seconds,
        'duration_minutes': first_q.duration_minutes,
        'questions': question_list,
        'total_questions': questions.count(),
        'solved_count': len(solved_question_ids),
    })

@login_required
@require_POST
def bonus_submit(request):
    if request.user.is_staff:
        return JsonResponse({'status': 'Staff accounts cannot submit.'})

    state = HackathonState.objects.first()
    if not state or not state.is_started or state.is_finished or state.is_paused:
        return JsonResponse({'status': 'Hackathon is not active.'})

    question_id = request.POST.get('question_id')
    if not question_id:
        return JsonResponse({'status': 'Missing question_id'})

    bonus = get_object_or_404(BonusQuestion, id=question_id)
    if not bonus.is_active:
        return JsonResponse({'status': 'Bonus not active'})

    if bonus.is_paused:
        return JsonResponse({'status': 'Bonus is paused'})

    if BonusSubmission.objects.filter(bonus=bonus, team=request.user, is_correct=True).exists():
        return JsonResponse({'status': 'Already solved this question'})

    if bonus.activated_at:
        if bonus.is_paused:
            open_seconds = (bonus.paused_at - bonus.activated_at).total_seconds()
        else:
            open_seconds = (timezone.now() - bonus.activated_at).total_seconds()
        if open_seconds >= bonus.duration_minutes * 60:
            return JsonResponse({'status': 'Bonus round has expired'})

    user_input = request.POST.get('user_input', '').strip()
    if not user_input:
        return JsonResponse({'status': 'Please enter an input'})

    output, error = run_python_code(bonus.starter_code, user_input)

    if error:
        return JsonResponse({'status': 'Runtime Error', 'error': error})

    if output is None or output.strip() != bonus.expected_output.strip():
        return JsonResponse({'status': 'Wrong Answer — check your input format.'})

    points_awarded = 70
    finish_rank = None

    all_questions = BonusQuestion.objects.filter(is_active=True).order_by('order')
    already_solved_ids = set(
        BonusSubmission.objects.filter(
            team=request.user, is_correct=True, bonus__in=all_questions
        ).values_list('bonus_id', flat=True)
    )
    already_solved_ids.add(bonus.id)

    all_complete = len(already_solved_ids) == all_questions.count()

    if all_complete:
        try:
            with transaction.atomic():
                h_state = HackathonState.objects.select_for_update().first()

                finished_teams_count = BonusSubmission.objects.filter(
                    bonus__in=all_questions,
                    is_correct=True
                ).exclude(
                    team=request.user
                ).values('team').annotate(
                    solved_count=Count('bonus', distinct=True)
                ).filter(
                    solved_count=all_questions.count()
                ).count()

                if finished_teams_count == 0:
                    points_awarded += 100
                    finish_rank = 1
                    if h_state and not h_state.bonus_first_finisher:
                        h_state.bonus_first_finisher = request.user
                        h_state.save()
                elif finished_teams_count == 1:
                    points_awarded += 50
                    finish_rank = 2
                elif finished_teams_count == 2:
                    points_awarded += 25
                    finish_rank = 3
                else:
                    finish_rank = finished_teams_count + 1

                BonusSubmission.objects.create(
                    team=request.user, bonus=bonus,
                    submitted_input=user_input,
                    is_correct=True,
                    points_awarded=points_awarded,
                )
        except Exception:
            return JsonResponse({'status': 'Already solved this question'})
    else:
        try:
            BonusSubmission.objects.create(
                team=request.user, bonus=bonus,
                submitted_input=user_input,
                is_correct=True,
                points_awarded=points_awarded,
            )
        except Exception:
            return JsonResponse({'status': 'Already solved this question'})

    new_total = _get_total_score(request.user)

    solved_count = BonusSubmission.objects.filter(
        team=request.user, is_correct=True, bonus__in=all_questions
    ).count()

    response_data = {
        'status': 'Correct!',
        'new_total': new_total,
        'solved_count': solved_count,
        'total_questions': all_questions.count(),
        'all_complete': all_complete,
    }

    if all_complete:
        if finish_rank == 1:
            response_data['status'] = 'Correct! 🏆 You finished first — +100 bonus points!'
            response_data['first_finisher'] = True
        elif finish_rank == 2:
            response_data['status'] = 'Correct! 🥈 You finished second — +50 bonus points!'
            response_data['first_finisher'] = False
        elif finish_rank == 3:
            response_data['status'] = 'Correct! 🥉 You finished third — +25 bonus points!'
            response_data['first_finisher'] = False
        else:
            response_data['status'] = 'Correct! All questions complete — +70 points!'
            response_data['first_finisher'] = False
        response_data['points_awarded'] = points_awarded

    return JsonResponse(response_data)

@login_required
def bonus_page(request):
    questions = BonusQuestion.objects.filter(is_active=True).order_by('order')
    if not questions.exists():
        return redirect('home')

    first_q = questions.first()
    state = HackathonState.objects.first()
    if not state or not state.start_time:
        return redirect('home')

    if first_q.activated_at:
        if first_q.is_paused:
            open_seconds = (first_q.paused_at - first_q.activated_at).total_seconds()
        else:
            open_seconds = (timezone.now() - first_q.activated_at).total_seconds()
    else:
        open_seconds = 0
    duration_seconds = first_q.duration_minutes * 60
    time_remaining_seconds = max(0, int(duration_seconds - open_seconds))
    expired = open_seconds >= duration_seconds

    # Per-question solved status
    solved_ids = set(
        BonusSubmission.objects.filter(
            team=request.user, is_correct=True, bonus__in=questions
        ).values_list('bonus_id', flat=True)
    )

    question_data = []
    for q in questions:
        question_data.append({
            'id': q.id,
            'order': q.order,
            'title': q.title,
            'description': q.description,
            'starter_code': q.starter_code,
            'expected_output': q.expected_output,
            'input_type_hint': q.input_type_hint,
            'solved': q.id in solved_ids,
        })

    all_solved = len(solved_ids) == questions.count()
    first_finisher = state.bonus_first_finisher
    is_first_finisher = first_finisher == request.user if first_finisher else False

    return render(request, 'bonus.html', {
        'questions': question_data,
        'total_questions': questions.count(),
        'solved_count': len(solved_ids),
        'all_solved': all_solved,
        'time_remaining_seconds': time_remaining_seconds,
        'duration_minutes': first_q.duration_minutes,
        'expired': expired,
        'is_paused': first_q.is_paused,
        'first_finisher': first_finisher.username if first_finisher else None,
        'is_first_finisher': is_first_finisher,
    })


@login_required
def check_hackathon_status(request):
    state = HackathonState.objects.first()

    if not state or not state.start_time:
        return JsonResponse({
            'is_finished': False,
            'is_live': False
        })

    dur = state.duration_minutes if state.duration_minutes else 120
    end_time = state.start_time + timedelta(minutes=dur)
    is_finished = state.is_finished

    if not is_finished and timezone.now() >= end_time:
        state.is_finished = True
        state.save()
        is_finished = True

    is_live = state.is_started and not is_finished and not state.is_paused

    return JsonResponse({
        'is_finished': is_finished,
        'is_live': is_live,
        'is_paused': state.is_paused
    })
@login_required
@require_POST
def run_code_custom(request):
    p_id = request.POST.get('problem_id')
    user_code = request.POST.get('code')
    problem = get_object_or_404(Problem, id=p_id)
    cases = problem.hidden_test_cases[:3]
    
    input_list = [case.get('input', '') for case in cases]
    results, error = run_leetcode_code(user_code, input_list, problem)
    
    if error:
        results_list = []
        for case in cases:
            results_list.append({
                'input': case.get('input', ''),
                'expected': case.get('expected', ''),
                'output': '',
                'error': error,
                'status': 'Runtime Error'
            })
        return JsonResponse({
            'status': 'Runtime Error',
            'results': results_list
        })

    overall_status = "Accepted"
    results_list = []
    for case, res in zip(cases, results):
        input_data = case.get('input', '')
        expected = case.get('expected', '')
        status = res['status']
        output = res['output']
        err = res['error']
        
        if status == 'Accepted':
            if output is None or output.strip() != str(expected).strip():
                status = "Wrong Answer"
                if overall_status == "Accepted":
                    overall_status = "Wrong Answer"
            else:
                status = "Accepted"
        else:
            overall_status = "Runtime Error"
            
        results_list.append({
            'input': input_data,
            'expected': expected,
            'output': output,
            'error': err,
            'status': status
        })
        
    return JsonResponse({
        'status': overall_status,
        'results': results_list
    })
@login_required
@require_POST
def ai_hint(request):
    state = HackathonState.objects.first()
    if state and not state.hints_enabled:
        return JsonResponse({'hint': 'AI hints have been disabled by the admin for this event.'}, status=200)

    problem_id = request.POST.get('problem_id')
    current_code = request.POST.get('code', '')

    problem = get_object_or_404(Problem, id=problem_id)

    from django.conf import settings
    api_key = getattr(settings, 'GROQ_API_KEY', '')
    if not api_key:
        return JsonResponse({'hint': 'AI hints are not configured. Ask your admin to set GROQ_API_KEY.'})

    console_output = request.POST.get('console_output', '').strip()
    model_name = (state.ai_model if state and state.ai_model else 'llama-3.3-70b-versatile')

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
        'model': model_name,
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 300,
        'temperature': 0.7,
    }).encode()

    req = urlreq.Request(
        'https://api.groq.com/openai/v1/chat/completions',
        data=payload,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}',
            'User-Agent': 'Mozilla/5.0',
        },
        method='POST'
    )

    try:
        with urlreq.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            hint_text = data['choices'][0]['message']['content']
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
    total_score = _get_total_score(request.user)
    return render(request, 'finished.html', {'total_score': total_score})

@login_required
@require_POST
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
@require_POST
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
@require_POST
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
@require_POST
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
@require_POST
def admin_start_bonus(request):
    if not request.user.is_staff:
        return redirect('waiting_room')
    now = timezone.now()
    questions = BonusQuestion.objects.all()
    for q in questions:
        q.is_active = True
        q.is_paused = False
        q.paused_at = None
        q.activated_at = now
        q.save()
    return redirect('/admin/')

@login_required
@require_POST
def admin_pause_bonus(request):
    if not request.user.is_staff:
        return redirect('waiting_room')
    now = timezone.now()
    questions = BonusQuestion.objects.filter(is_active=True, is_paused=False)
    for q in questions:
        q.is_paused = True
        q.paused_at = now
        q.save()
    return redirect('/admin/')

@login_required
@require_POST
def admin_resume_bonus(request):
    if not request.user.is_staff:
        return redirect('waiting_room')
    questions = BonusQuestion.objects.filter(is_active=True, is_paused=True)
    for q in questions:
        if q.paused_at and q.activated_at:
            duration = timezone.now() - q.paused_at
            q.activated_at = q.activated_at + duration
        q.is_paused = False
        q.paused_at = None
        q.save()
    return redirect('/admin/')

@login_required
@require_POST
def admin_end_bonus(request):
    if not request.user.is_staff:
        return redirect('waiting_room')
    questions = BonusQuestion.objects.all()
    for q in questions:
        q.is_active = False
        q.is_paused = False
        q.paused_at = None
        q.activated_at = None
        q.save()
    return redirect('/admin/')

@login_required
@require_POST
def admin_toggle_hints(request):
    if not request.user.is_staff:
        return redirect('waiting_room')
    state = HackathonState.objects.first()
    if state:
        state.hints_enabled = not state.hints_enabled
        state.save()
    return redirect('/admin/')

@login_required
@require_POST
def admin_reset_hackathon(request):
    if not request.user.is_staff:
        return redirect('waiting_room')
    state = HackathonState.objects.first()
    if state:
        state.is_started = False
        state.is_finished = False
        state.is_paused = False
        state.start_time = None
        state.paused_at = None
        state.bonus_first_finisher = None
        state.save()
    questions = BonusQuestion.objects.all()
    for q in questions:
        q.is_active = False
        q.is_paused = False
        q.paused_at = None
        q.activated_at = None
        q.save()
    return redirect('/admin/')

@login_required
@require_POST
def admin_toggle_tour(request):
    if not request.user.is_staff:
        return redirect('waiting_room')
    state = HackathonState.objects.first()
    if state:
        state.onboarding_tour_enabled = not state.onboarding_tour_enabled
        state.save()
    return redirect('/admin/')

@login_required
@require_POST
def admin_adjust_points(request):
    if not request.user.is_staff:
        return JsonResponse({'error': 'Forbidden'}, status=403)
    from django.contrib.auth.models import User
    team_id = request.POST.get('team_id')
    delta_raw = request.POST.get('delta', '0')
    reason = request.POST.get('reason', '').strip()
    try:
        delta = int(delta_raw)
    except ValueError:
        return JsonResponse({'error': 'Invalid delta'}, status=400)
    team = get_object_or_404(User, id=team_id, is_staff=False)
    PointAdjustment.objects.create(team=team, delta=delta, reason=reason, adjusted_by=request.user)
    return JsonResponse({'status': 'ok', 'team': team.username, 'delta': delta})