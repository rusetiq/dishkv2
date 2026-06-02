import os
import sys
import time
import re
import random
import threading
import urllib.request
import urllib.parse
from http.cookiejar import CookieJar
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from platform_app.models import HackathonState, Problem, BonusQuestion

state = HackathonState.objects.first()
if not state:
    state = HackathonState.objects.create(is_started=True, is_finished=False, is_paused=False)
else:
    state.is_started = True
    state.is_finished = False
    state.is_paused = False
    state.save()

for i in range(1, 101):
    u, created = User.objects.get_or_create(username=f"sim_team_{i}")
    if created or not u.check_password("password"):
        u.set_password("password")
        u.save()

if not Problem.objects.exists():
    Problem.objects.create(
        title="Two Sum",
        description="Find two numbers.",
        difficulty="Easy",
        function_name="twoSum",
        base_points=100,
        starter_code="class Solution:\n    def twoSum(self, nums, target):\n        pass",
        hidden_test_cases=[
            {"input": "([2,7,11,15], 9)", "expected": "[0, 1]"}
        ]
    )

problem = Problem.objects.first()
problem_id = problem.id

BASE_URL = "http://10.10.50.50"
try:
    urllib.request.urlopen(BASE_URL, timeout=1)
except Exception:
    BASE_URL = "http://10.10.50.50"

results_lock = threading.Lock()
print_lock = threading.Lock()
request_records = []
start_barrier = threading.Barrier(100)

def log_event(message):
    timestamp = time.strftime("%H:%M:%S")
    with print_lock:
        sys.stdout.write(f"[{timestamp}] {message}\n")
        sys.stdout.flush()

class Session:
    def __init__(self):
        self.cookie_jar = CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie_jar))
        self.csrf_token = None

    def request(self, path, method="GET", data=None, username=None):
        url = f"{BASE_URL}{path}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) SimulationClient/2.0"
        }
        if self.csrf_token:
            headers["X-CSRFToken"] = self.csrf_token
            headers["Referer"] = url
        
        req_data = None
        if data:
            if isinstance(data, dict):
                req_data = urllib.parse.urlencode(data).encode("utf-8")
            else:
                req_data = data
        
        req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
        t0 = time.time()
        status = 500
        duration = 0
        err_msg = None
        html = ""
        try:
            with self.opener.open(req, timeout=30) as response:
                status = response.status
                html = response.read().decode("utf-8")
                t1 = time.time()
                duration = t1 - t0
                for cookie in self.cookie_jar:
                    if cookie.name == "csrftoken":
                        self.csrf_token = cookie.value
                csrf_match = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', html)
                if csrf_match:
                    self.csrf_token = csrf_match.group(1)
        except urllib.error.HTTPError as e:
            t1 = time.time()
            duration = t1 - t0
            status = e.code
            err_msg = str(e)
            try:
                html = e.read().decode("utf-8")
            except Exception:
                html = ""
        except Exception as e:
            t1 = time.time()
            duration = t1 - t0
            status = 500
            err_msg = str(e)

        if username:
            with results_lock:
                request_records.append({
                    "username": username,
                    "method": method,
                    "path": path,
                    "status": status,
                    "duration": duration,
                    "error": err_msg
                })
        return status, duration, html, err_msg

def simulate_user(username):
    session = Session()
    start_barrier.wait()
    
    log_event(f"[{username}] Starting sequence")
    
    status, duration, html, err = session.request("/login/", "GET", username=username)
    log_event(f"[{username}] GET /login/ -> {status} in {duration*1000:.1f}ms")
    
    time.sleep(random.uniform(0.1, 0.3))
    
    login_data = {
        "username": username,
        "password": "password",
        "csrfmiddlewaretoken": session.csrf_token or ""
    }
    status, duration, html, err = session.request("/login/", "POST", login_data, username=username)
    log_event(f"[{username}] POST /login/ -> {status} in {duration*1000:.1f}ms")
    
    time.sleep(random.uniform(0.1, 0.3))
    
    status, duration, html, err = session.request("/home/", "GET", username=username)
    log_event(f"[{username}] GET /home/ -> {status} in {duration*1000:.1f}ms")
    
    time.sleep(random.uniform(0.1, 0.3))
    
    status, duration, html, err = session.request(f"/problem/{problem_id}/", "GET", username=username)
    log_event(f"[{username}] GET /problem/{problem_id}/ -> {status} in {duration*1000:.1f}ms")
    
    time.sleep(random.uniform(0.1, 0.3))
    
    status, duration, html, err = session.request("/api/status/", "GET", username=username)
    log_event(f"[{username}] GET /api/status/ -> {status} in {duration*1000:.1f}ms")
    
    time.sleep(random.uniform(0.1, 0.3))
    
    save_data = {
        "problem_id": problem_id,
        "code": "class Solution:\n    def twoSum(self, nums, target):\n        lookup = {}\n        for i, num in enumerate(nums):\n            if target - num in lookup:\n                return [lookup[target - num], i]\n            lookup[num] = i\n        return []",
        "csrfmiddlewaretoken": session.csrf_token or ""
    }
    status, duration, html, err = session.request("/api/save/", "POST", save_data, username=username)
    log_event(f"[{username}] POST /api/save/ -> {status} in {duration*1000:.1f}ms")
    
    time.sleep(random.uniform(0.1, 0.4))
    
    run_data = {
        "problem_id": problem_id,
        "code": "class Solution:\n    def twoSum(self, nums: list[int], target: int) -> list[int]:\n        lookup = {}\n        for i, num in enumerate(nums):\n            if target - num in lookup:\n                return [lookup[target - num], i]\n            lookup[num] = i\n        return []",
        "csrfmiddlewaretoken": session.csrf_token or ""
    }
    status, duration, html, err = session.request("/api/run-custom/", "POST", run_data, username=username)
    log_event(f"[{username}] POST /api/run-custom/ -> {status} in {duration*1000:.1f}ms")
    
    time.sleep(random.uniform(0.2, 0.5))
    
    submit_data = {
        "problem_id": problem_id,
        "code": "class Solution:\n    def twoSum(self, nums: list[int], target: int) -> list[int]:\n        lookup = {}\n        for i, num in enumerate(nums):\n            if target - num in lookup:\n                return [lookup[target - num], i]\n            lookup[num] = i\n        return []",
        "csrfmiddlewaretoken": session.csrf_token or ""
    }
    status, duration, html, err = session.request("/api/submit/", "POST", submit_data, username=username)
    log_event(f"[{username}] POST /api/submit/ -> {status} in {duration*1000:.1f}ms")
    
    for cycle in range(1, 4):
        time.sleep(random.uniform(0.3, 0.6))
        
        status, duration, html, err = session.request("/api/leaderboard-data/", "GET", username=username)
        log_event(f"[{username}] [Cycle {cycle}] GET /api/leaderboard-data/ -> {status} in {duration*1000:.1f}ms")
        
        time.sleep(random.uniform(0.2, 0.4))
        
        status, duration, html, err = session.request("/api/bonus/status/", "GET", username=username)
        log_event(f"[{username}] [Cycle {cycle}] GET /api/bonus/status/ -> {status} in {duration*1000:.1f}ms")
        
        if status == 200:
            try:
                import json
                b_data = json.loads(html)
                if b_data.get("active") and b_data.get("available"):
                    time.sleep(random.uniform(0.1, 0.3))
                    bonus_data = {
                        "user_input": "dummy_input_simulation",
                        "csrfmiddlewaretoken": session.csrf_token or ""
                    }
                    b_status, b_duration, b_html, b_err = session.request("/api/bonus/submit/", "POST", bonus_data, username=username)
                    log_event(f"[{username}] [Cycle {cycle}] POST /api/bonus/submit/ -> {b_status} in {b_duration*1000:.1f}ms")
            except Exception:
                pass
            
    log_event(f"[{username}] Completed sequence")

def main():
    try:
        urllib.request.urlopen(BASE_URL, timeout=3)
    except Exception:
        print(f"Error: The server is not running at {BASE_URL}.")
        print("Please start it in another terminal: python manage.py runserver")
        sys.exit(1)
        
    print(f"Starting intensive simulation of 100 concurrent users on {BASE_URL}...")
    t_start = time.time()
    threads = []
    for i in range(1, 101):
        t = threading.Thread(target=simulate_user, args=(f"sim_team_{i}",))
        threads.append(t)
        t.start()
        
    for t in threads:
        t.join()
    t_end = time.time()
    
    total_reqs = len(request_records)
    if total_reqs == 0:
        print("No requests completed.")
        return
        
    success_reqs = sum(1 for r in request_records if r["status"] in (200, 302))
    failed_reqs = total_reqs - success_reqs
    success_rate = (success_reqs / total_reqs) * 100
    
    total_duration = sum(r["duration"] for r in request_records)
    avg_latency = total_duration / total_reqs
    
    by_endpoint = {}
    for r in request_records:
        key = f"{r['method']} {r['path']}"
        if key not in by_endpoint:
            by_endpoint[key] = []
        by_endpoint[key].append(r)
        
    print("\n" + "="*80)
    print("                      CONCURRENCY SIMULATION REPORT")
    print("="*80)
    print(f"Total Simulated Teams:  100")
    print(f"Total Requests Made:    {total_reqs}")
    print(f"Successful Requests:    {success_reqs}")
    print(f"Failed Requests:        {failed_reqs}")
    print(f"Overall Success Rate:   {success_rate:.2f}%")
    print(f"Total Simulation Time:  {t_end - t_start:.2f} seconds")
    print(f"Average Request Time:   {avg_latency * 1000:.1f} ms")
    print(f"Throughput:             {total_reqs / (t_end - t_start):.2f} req/sec")
    print("-"*80)
    print(f"{'Endpoint':<35} | {'Count':<6} | {'Success%':<8} | {'Avg (ms)':<10} | {'P95 (ms)':<10} | {'Max (ms)':<10}")
    print("-"*80)
    
    for key, records in sorted(by_endpoint.items()):
        cnt = len(records)
        succ = sum(1 for r in records if r["status"] in (200, 302))
        pct = (succ / cnt) * 100
        durs = sorted([r["duration"] for r in records])
        avg = (sum(durs) / cnt) * 1000
        p95 = durs[int(cnt * 0.95)] * 1000 if cnt > 0 else 0
        mx = durs[-1] * 1000 if cnt > 0 else 0
        print(f"{key:<35} | {cnt:<6} | {pct:<7.1f}% | {avg:<8.1f} | {p95:<8.1f} | {mx:<8.1f}")
        
    print("="*80)
    
    print("\nDetailed Analysis:")
    print("1. Database & Session Performance:")
    print("   Concurrency is heavily affected by SQLite write locking.")
    print("   Simultaneous POST /login/ and POST /api/save/ requests write to django_session and platform_app_teamprogress.")
    print("   Average response times for POST /api/save/ show if SQLite database contention occurred.")
    print("\n2. Subprocess Execution Load:")
    print("   Requests to /api/run-custom/ and /api/submit/ spin up Python compiler subprocesses.")
    print("   If the execution server is single-core or has high CPU contention, these run/submit calls")
    print("   show significantly higher latencies (Avg and P95) compared to static page views.")
    print("\n3. Network and HTTP Throughput:")
    print("   The simulation clients achieved a concurrent surge of requests.")
    print("   Any failed requests indicate server timeouts, subprocess limits, or rate limits.")

if __name__ == "__main__":
    main()
