import os
import sys
import csv
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from platform_app.models import TeamProgress, BonusSubmission, PointAdjustment, BonusQuestion, HackathonState, Problem
from django.db.models import Sum

def empty_database():
    TeamProgress.objects.all().delete()
    BonusSubmission.objects.all().delete()
    PointAdjustment.objects.all().delete()
    User.objects.exclude(username="aarush").delete()
    print("Database cleared (all users except aarush and all submissions removed).")

def add_superuser():
    username = input("Enter superuser username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return
    if User.objects.filter(username=username).exists():
        print("User already exists.")
        return
    email = input("Enter email (optional): ").strip()
    password = input("Enter password: ").strip()
    if not password:
        print("Password cannot be empty.")
        return
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' created successfully.")

def add_normal_user():
    username = input("Enter username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return
    if User.objects.filter(username=username).exists():
        print("User already exists.")
        return
    password = input("Enter password: ").strip()
    if not password:
        print("Password cannot be empty.")
        return
    User.objects.create_user(username=username, password=password)
    print(f"User '{username}' created successfully.")

def add_users_from_csv():
    path = input("Enter CSV file path: ").strip()
    if not os.path.exists(path):
        print("File does not exist.")
        return
    try:
        with open(path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
        if not rows:
            print("CSV file is empty.")
            return
        
        first_row = [col.lower().strip() for col in rows[0]]
        user_idx = 0
        pass_idx = 1
        
        has_header = False
        if any(h in first_row for h in ['user', 'username', 'login', 'name', 'password', 'pass']):
            has_header = True
            for idx, col in enumerate(first_row):
                if col in ['user', 'username', 'login', 'name']:
                    user_idx = idx
                elif col in ['password', 'pass']:
                    pass_idx = idx
        
        start_row = 1 if has_header else 0
        created_count = 0
        already_exists_count = 0
        
        for row in rows[start_row:]:
            if len(row) <= max(user_idx, pass_idx):
                continue
            username = row[user_idx].strip()
            password = row[pass_idx].strip()
            if not username or not password:
                continue
            if User.objects.filter(username=username).exists():
                already_exists_count += 1
                continue
            User.objects.create_user(username=username, password=password)
            created_count += 1
            
        print(f"Successfully added {created_count} users. ({already_exists_count} users already existed).")
    except Exception as e:
        print(f"Error reading CSV: {e}")

def list_all_users():
    users = User.objects.all().order_by('username')
    if not users.exists():
        print("No users found.")
        return
    print(f"\n{'Username':<25} {'Staff':<8} {'Superuser':<12}")
    print("-" * 45)
    for u in users:
        staff = "Yes" if u.is_staff else "No"
        superuser = "Yes" if u.is_superuser else "No"
        print(f"{u.username:<25} {staff:<8} {superuser:<12}")
    print(f"\nTotal: {users.count()} users ({users.filter(is_staff=False).count()} teams, {users.filter(is_staff=True).count()} staff)")

def delete_user():
    username = input("Enter username to delete: ").strip()
    if not username:
        print("Username cannot be empty.")
        return
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        print(f"User '{username}' not found.")
        return
    if user.is_superuser:
        confirm = input(f"WARNING: '{username}' is a superuser. Are you sure? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("Cancelled.")
            return
    user.delete()
    print(f"User '{username}' deleted successfully.")

def view_leaderboard():
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
    adj_scores = PointAdjustment.objects.values('team__username').annotate(
        adj_score=Sum('delta')
    )
    team_scores_map = {t['team__username']: t['problem_score'] or 0 for t in team_scores}
    bonus_map = {b['team__username']: b['bonus_score'] or 0 for b in bonus_scores}
    adj_map = {a['team__username']: a['adj_score'] or 0 for a in adj_scores}

    all_teams = User.objects.filter(is_staff=False)
    teams = []
    for team in all_teams:
        username = team.username
        prob = team_scores_map.get(username, 0)
        bon = bonus_map.get(username, 0)
        adj = adj_map.get(username, 0)
        total = prob + bon + adj
        teams.append({'username': username, 'problem': prob, 'bonus': bon, 'adj': adj, 'total': total})

    teams = sorted(teams, key=lambda x: x['total'], reverse=True)

    if not teams:
        print("No scores yet.")
        return

    print(f"\n{'Rank':<6} {'Team':<25} {'Problems':<10} {'Bonus':<8} {'Adj':<8} {'Total':<8}")
    print("-" * 65)
    for i, t in enumerate(teams, 1):
        adj_str = f"+{t['adj']}" if t['adj'] >= 0 else str(t['adj'])
        print(f"{i:<6} {t['username']:<25} {t['problem']:<10} {t['bonus']:<8} {adj_str:<8} {t['total']:<8}")

def reset_all_progress():
    confirm = input("This will delete all TeamProgress and BonusSubmission records (users kept). Continue? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Cancelled.")
        return
    tp_count = TeamProgress.objects.count()
    bs_count = BonusSubmission.objects.count()
    pa_count = PointAdjustment.objects.count()
    TeamProgress.objects.all().delete()
    BonusSubmission.objects.all().delete()
    PointAdjustment.objects.all().delete()
    # Reset bonus first finisher
    state = HackathonState.objects.first()
    if state:
        state.bonus_first_finisher = None
        state.save()
    print(f"Deleted {tp_count} progress entries, {bs_count} bonus submissions, {pa_count} point adjustments.")

def change_user_password():
    username = input("Enter username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        print(f"User '{username}' not found.")
        return
    new_password = input("Enter new password: ").strip()
    if not new_password:
        print("Password cannot be empty.")
        return
    user.set_password(new_password)
    user.save()
    print(f"Password for '{username}' changed successfully.")

def export_results_to_csv():
    path = input("Enter output CSV file path (default: results.csv): ").strip()
    if not path:
        path = "results.csv"

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
    adj_scores = PointAdjustment.objects.values('team__username').annotate(
        adj_score=Sum('delta')
    )
    bonus_map = {b['team__username']: b['bonus_score'] or 0 for b in bonus_scores}
    adj_map = {a['team__username']: a['adj_score'] or 0 for a in adj_scores}
    team_scores_map = {t['team__username']: t['problem_score'] or 0 for t in team_scores}

    all_teams = User.objects.filter(is_staff=False)
    teams = []
    for team in all_teams:
        username = team.username
        prob = team_scores_map.get(username, 0)
        bon = bonus_map.get(username, 0)
        adj = adj_map.get(username, 0)
        teams.append({'username': username, 'problem': prob, 'bonus': bon, 'adj': adj, 'total': prob + bon + adj})

    teams = sorted(teams, key=lambda x: x['total'], reverse=True)

    try:
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Rank', 'Team', 'Problem Points', 'Bonus Points', 'Adjustments', 'Total'])
            for i, t in enumerate(teams, 1):
                writer.writerow([i, t['username'], t['problem'], t['bonus'], t['adj'], t['total']])
        print(f"Results exported to '{path}' ({len(teams)} teams).")
    except Exception as e:
        print(f"Error writing CSV: {e}")

def view_bonus_status():
    questions = BonusQuestion.objects.all().order_by('order')
    if not questions.exists():
        print("No bonus questions configured.")
        return
    state = HackathonState.objects.first()
    first_finisher = state.bonus_first_finisher.username if state and state.bonus_first_finisher else "None"

    print(f"\n{'#':<4} {'Title':<30} {'Active':<8} {'Paused':<8}")
    print("-" * 50)
    for q in questions:
        active = "Yes" if q.is_active else "No"
        paused = "Yes" if q.is_paused else "No"
        print(f"{q.order:<4} {q.title:<30} {active:<8} {paused:<8}")

    # Show solve counts per question
    print(f"\nSolve counts:")
    for q in questions:
        count = BonusSubmission.objects.filter(bonus=q, is_correct=True).count()
        print(f"  Q{q.order} ({q.title}): {count} teams solved")
    
    print(f"\nFirst finisher: {first_finisher}")

def adjust_points():
    username = input("Enter team username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        print(f"User '{username}' not found.")
        return

    try:
        delta_str = input("Enter points delta (e.g. 50 or -50): ").strip()
        delta = int(delta_str)
    except ValueError:
        print("Invalid number.")
        return

    reason = input("Enter reason for adjustment: ").strip()
    
    admin_user = User.objects.filter(is_superuser=True).first()
    PointAdjustment.objects.create(
        team=user,
        delta=delta,
        reason=reason,
        adjusted_by=admin_user
    )
    print(f"Adjusted points for '{username}' by {delta:+} points.")

def put_user_solutions():
    username = input("Enter team username: ").strip()
    if not username:
        print("Username cannot be empty.")
        return
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        print(f"User '{username}' not found.")
        return

    from platform_app.models import Problem
    problems = Problem.objects.all().order_by('id')
    if not problems.exists():
        print("No problems configured in the database.")
        return

    print("\nProblems:")
    for p in problems:
        print(f"  {p.id}. {p.title} ({p.difficulty}, {p.base_points} base points)")
    
    choice = input("\nEnter problem ID to solve, or 'all' to solve all: ").strip().lower()
    
    if choice == 'all':
        for p in problems:
            progress, created = TeamProgress.objects.get_or_create(team=user, problem=p)
            if not progress.is_solved:
                progress.is_solved = True
                progress.points = p.base_points
                progress.save()
        print(f"Successfully solved all {problems.count()} problems for team '{username}'.")
    else:
        try:
            p_id = int(choice)
            p = Problem.objects.get(id=p_id)
        except (ValueError, Problem.DoesNotExist):
            print("Invalid problem ID.")
            return

        progress, created = TeamProgress.objects.get_or_create(team=user, problem=p)
        if progress.is_solved:
            print(f"Problem '{p.title}' already solved by '{username}' with {progress.points} points.")
            return
        progress.is_solved = True
        progress.points = p.base_points
        progress.save()
        print(f"Successfully solved problem '{p.title}' for team '{username}' with {p.base_points} points.")

def add_problems_from_csv():
    path = input("Enter CSV file path for standard problems: ").strip()
    if not os.path.exists(path):
        print("File does not exist.")
        return
    try:
        with open(path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        if not rows:
            print("CSV file is empty.")
            return

        created_count = 0
        updated_count = 0
        
        for idx, row in enumerate(rows, 1):
            normalized_row = {k.lower().strip(): v for k, v in row.items() if k}
            
            title = normalized_row.get('title', '').strip()
            description = normalized_row.get('description', '').strip()
            if not title or not description:
                print(f"Skipping row {idx}: Title and description are required.")
                continue
                
            hidden_test_cases_str = normalized_row.get('hidden_test_cases', '[]').strip()
            import json
            try:
                hidden_test_cases = json.loads(hidden_test_cases_str) if hidden_test_cases_str else []
                if not isinstance(hidden_test_cases, list):
                    raise ValueError("Test cases must be a list of objects")
            except Exception as e:
                print(f"Skipping row {idx}: Invalid JSON format for hidden_test_cases. Error: {e}")
                continue

            problem_id = normalized_row.get('id', '').strip()
            difficulty = normalized_row.get('difficulty', 'Easy').strip()
            if difficulty not in ['Easy', 'Medium', 'Hard']:
                difficulty = 'Easy'
                
            function_name = normalized_row.get('function_name', 'solution').strip()
            input_variable = normalized_row.get('input_variable', 'n').strip()
            
            base_points_val = 100
            for points_key in ['base_points', 'points']:
                if points_key in normalized_row and normalized_row[points_key].strip():
                    try:
                        base_points_val = int(normalized_row[points_key].strip())
                        break
                    except ValueError:
                        pass
                        
            starter_code = normalized_row.get('starter_code', '').replace('\\n', '\n')
            examples = normalized_row.get('examples', '').replace('\\n', '\n')
            
            defaults = {
                "title": title,
                "description": description,
                "difficulty": difficulty,
                "function_name": function_name,
                "input_variable": input_variable,
                "base_points": base_points_val,
                "points": base_points_val,
                "starter_code": starter_code,
                "examples": examples,
                "hidden_test_cases": hidden_test_cases,
            }
            
            if problem_id:
                try:
                    prob, created = Problem.objects.update_or_create(id=int(problem_id), defaults=defaults)
                except ValueError:
                    prob, created = Problem.objects.update_or_create(title=title, defaults=defaults)
            else:
                prob, created = Problem.objects.update_or_create(title=title, defaults=defaults)
                
            if created:
                created_count += 1
            else:
                updated_count += 1
                
            TeamProgress.objects.filter(problem=prob, is_solved=False).update(current_code=prob.starter_code)

        print(f"Successfully processed CSV. Created {created_count} new problems, updated {updated_count} existing problems.")
    except Exception as e:
        print(f"Error reading CSV: {e}")

def add_bonus_questions_from_csv():
    path = input("Enter CSV file path for bonus questions: ").strip()
    if not os.path.exists(path):
        print("File does not exist.")
        return
    try:
        with open(path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        if not rows:
            print("CSV file is empty.")
            return

        created_count = 0
        updated_count = 0
        
        from django.db.models import Max
        max_order_query = BonusQuestion.objects.aggregate(Max('order'))
        next_order = (max_order_query['order__max'] or 0) + 1

        for idx, row in enumerate(rows, 1):
            normalized_row = {k.lower().strip(): v for k, v in row.items() if k}
            
            title = normalized_row.get('title', '').strip()
            description = normalized_row.get('description', '').strip()
            starter_code = normalized_row.get('starter_code', '').strip().replace('\\n', '\n')
            expected_output = normalized_row.get('expected_output', '').strip()
            
            if not title or not description or not starter_code or not expected_output:
                print(f"Skipping row {idx}: Title, description, starter_code, and expected_output are required.")
                continue

            order_str = normalized_row.get('order', '').strip()
            if order_str:
                try:
                    order_val = int(order_str)
                except ValueError:
                    order_val = next_order
                    next_order += 1
            else:
                order_val = next_order
                next_order += 1

            input_type_hint = normalized_row.get('input_type_hint', '').strip()
            
            duration_minutes_val = 10
            if 'duration_minutes' in normalized_row and normalized_row['duration_minutes'].strip():
                try:
                    duration_minutes_val = int(normalized_row['duration_minutes'].strip())
                except ValueError:
                    pass
            
            defaults = {
                "title": title,
                "description": description,
                "starter_code": starter_code,
                "expected_output": expected_output,
                "input_type_hint": input_type_hint,
                "duration_minutes": duration_minutes_val,
            }
            
            bq, created = BonusQuestion.objects.update_or_create(order=order_val, defaults=defaults)
            if created:
                created_count += 1
            else:
                updated_count += 1

        print(f"Successfully processed CSV. Created {created_count} new bonus questions, updated {updated_count} existing bonus questions.")
    except Exception as e:
        print(f"Error reading CSV: {e}")

def list_all_questions():
    problems = Problem.objects.all().order_by('id')
    print("\nStandard Problems:")
    print("-" * 75)
    if not problems.exists():
        print("No standard problems configured.")
    else:
        print(f"{'ID':<6} {'Title':<30} {'Difficulty':<12} {'Base Points':<12}")
        print("-" * 75)
        for p in problems:
            print(f"{p.id:<6} {p.title[:28]:<30} {p.difficulty:<12} {p.base_points:<12}")
            
    bonus = BonusQuestion.objects.all().order_by('order')
    print("\nBonus Questions:")
    print("-" * 75)
    if not bonus.exists():
        print("No bonus questions configured.")
    else:
        print(f"{'Order':<6} {'Title':<30} {'Duration':<12} {'Active':<8}")
        print("-" * 75)
        for b in bonus:
            active_str = "Yes" if b.is_active else "No"
            print(f"{b.order:<6} {b.title[:28]:<30} {f'{b.duration_minutes} min':<12} {active_str:<8}")

def delete_question():
    print("\nWhich type of question would you like to delete?")
    print("1. Standard Problem")
    print("2. Bonus Question")
    choice = input("Enter choice (1 or 2): ").strip()
    if choice == '1':
        p_id = input("Enter Standard Problem ID to delete: ").strip()
        if not p_id:
            print("ID cannot be empty.")
            return
        try:
            prob = Problem.objects.get(id=int(p_id))
        except (ValueError, Problem.DoesNotExist):
            print(f"Problem with ID {p_id} not found.")
            return
        
        confirm = input(f"Are you sure you want to delete problem '{prob.title}'? This will delete all associated TeamProgress. (yes/no): ").strip().lower()
        if confirm == 'yes':
            prob.delete()
            print("Problem deleted successfully.")
        else:
            print("Cancelled.")
    elif choice == '2':
        order_str = input("Enter Bonus Question Order to delete: ").strip()
        if not order_str:
            print("Order cannot be empty.")
            return
        try:
            bq = BonusQuestion.objects.get(order=int(order_str))
        except (ValueError, BonusQuestion.DoesNotExist):
            print(f"Bonus question with order {order_str} not found.")
            return
            
        confirm = input(f"Are you sure you want to delete bonus question '{bq.title}'? This will delete all associated submissions. (yes/no): ").strip().lower()
        if confirm == 'yes':
            bq.delete()
            print("Bonus question deleted successfully.")
        else:
            print("Cancelled.")
    else:
        print("Invalid choice.")

def delete_all_questions():
    print("\nWARNING: This will delete ALL standard problems, ALL bonus questions, and ALL team progress and submissions.")
    confirm = input("Are you absolutely sure you want to proceed? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("Cancelled.")
        return
    confirm_double = input("Type 'DELETE ALL' to confirm: ").strip()
    if confirm_double != 'DELETE ALL':
        print("Cancelled.")
        return
        
    p_count = Problem.objects.count()
    bq_count = BonusQuestion.objects.count()
    tp_count = TeamProgress.objects.count()
    bs_count = BonusSubmission.objects.count()
    
    Problem.objects.all().delete()
    BonusQuestion.objects.all().delete()
    TeamProgress.objects.all().delete()
    BonusSubmission.objects.all().delete()
    
    state = HackathonState.objects.first()
    if state:
        state.bonus_first_finisher = None
        state.save()
        
    print(f"Deleted {p_count} problems, {bq_count} bonus questions, {tp_count} progress entries, and {bs_count} bonus submissions.")

def main():
    while True:
        print("\nDIS Database Administrator Panel")
        print("─" * 38)
        print("  Users")
        print("  1.  Empty database (except aarush)")
        print("  2.  Add superuser")
        print("  3.  Add normal user")
        print("  4.  Add multiple users via CSV")
        print("  5.  List all users")
        print("  6.  Delete a user")
        print("  7.  Change user password")
        print("")
        print("  Scores & Data")
        print("  8.  View leaderboard")
        print("  9.  Reset all progress (keep users)")
        print("  10. Export results to CSV")
        print("  11. View bonus status")
        print("  12. Adjust points (add/remove)")
        print("  13. Put solutions for a specific user")
        print("")
        print("  Questions & Problems")
        print("  14. Add problems/questions via CSV")
        print("  15. Add bonus questions via CSV")
        print("  16. List all questions")
        print("  17. Delete a specific question")
        print("  18. Delete all questions")
        print("")
        print("  0.  Exit")
        print("─" * 38)
        
        choice = input("Select an option: ").strip()
        if choice == '1':
            empty_database()
        elif choice == '2':
            add_superuser()
        elif choice == '3':
            add_normal_user()
        elif choice == '4':
            add_users_from_csv()
        elif choice == '5':
            list_all_users()
        elif choice == '6':
            delete_user()
        elif choice == '7':
            change_user_password()
        elif choice == '8':
            view_leaderboard()
        elif choice == '9':
            reset_all_progress()
        elif choice == '10':
            export_results_to_csv()
        elif choice == '11':
            view_bonus_status()
        elif choice == '12':
            adjust_points()
        elif choice == '13':
            put_user_solutions()
        elif choice == '14':
            add_problems_from_csv()
        elif choice == '15':
            add_bonus_questions_from_csv()
        elif choice == '16':
            list_all_questions()
        elif choice == '17':
            delete_question()
        elif choice == '18':
            delete_all_questions()
        elif choice == '0':
            print("Exiting.")
            break
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    main()
