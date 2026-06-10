# dishkv2

A real-time, interactive LeetCode-style hackathon platform built with Python and Django. This platform enables organizations to host programming competitions where teams can write Python solutions to algorithmic challenges, receive AI-powered hints, compete in fast-paced bonus rounds, and track their progress on a live, dynamic leaderboard.

---

## Features

### Live Editor & Code Execution Sandbox
- **Interactive IDE**: A fully-featured web-based code editor pre-populated with starter code templates.
- **Custom Sandbox runner**: Safely executes python submissions against pre-defined test cases using sub-processes.
- **LeetCode Style Driver**: Automatically parses inputs, injects helper utilities (such as `isBadVersion`), and runs solution methods on the fly.

### AI Hints System
- **Context-Aware Assistance**: Integrates with LLMs (e.g., Llama-3.3-70B, GPT-4o, Groq) to provide smart hints based on the user's current code draft.
- **Admin Managed Limits**: Configurable token system for hints, allowing admins to enable/disable or limit the AI assistance per team.

### Cheat Prevention (Tab Switch Tracking)
- **Tab Monitoring**: Tracks when users change tabs or leave the browser window while working on a problem.
- **Anti-Cheat Logs**: Logs tab switches in the database (`tab_switches`) to help administrators maintain competition integrity.

### Dynamic Bonus Round
- **Speed Runs**: Active timed questions launched dynamically by admins during the event.
- **Dynamic Scoring**: Score decay rewards faster submissions (e.g. earlier finishers get up to 200 points, scaling down to 0).
- **Fastest Finisher Bonus**: Tracking and bonus rewards for the first team to solve all bonus questions.

### Live Leaderboard & Admin Dashboard
- **Dynamic Standings**: Real-time ranks showing aggregated scores (Problem points + Bonus points + Adjustments).
- **Score Penalties**: Time-based scoring decays points based on time elapsed before a correct submission is made.
- **Point Adjustments**: Admin capability to grant bonuses or issue penalties to teams manually.
- **Central Control Room**: Admins can pause, resume, start, or finish the event globally.

---

## Repository Structure

```text
├── hackathon_project/
│   ├── core/
│   │   ├── core/
│   │   ├── platform_app/
│   │   ├── templates/
│   │   ├── simulate.py
│   │   └── manage.py
│   └── tutorial/
├── requirements.txt
├── users_login_status.csv
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- Django 4.x+

### Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd dishkv2
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Create a `.env` file inside `hackathon_project/core/` and `hackathon_project/tutorial/` with the following variables:
   ```env
   SECRET_KEY=your-django-secret-key
   GROQ_API_KEY=your-groq-api-key
   ```

4. **Run Migrations & Initialize Database**:
   ```bash
   cd hackathon_project/core
   python manage.py migrate
   python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword') if not User.objects.filter(username='admin').exists() else None"
   ```

5. **Start the Development Server**:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```
   Open your browser and log in at `http://localhost:8000/`.

---

## Concurrency Load Testing (`simulate.py`)

The platform contains a dedicated simulation script (`simulate.py`) to benchmark the system under heavy load. It spins up 100 concurrent threads executing realistic user sessions:
- Authenticates and logs in.
- Interacts with the home dashboard and question pages.
- Saves code drafts and triggers custom compiler test runs.
- Submits solutions and fetches leaderboard stats recursively.
- Submits active bonus round answers.

### Running the Simulator
Ensure the server is running on `http://127.0.0.1:8000` or configured appropriately in `simulate.py` (`BASE_URL`), then execute:
```bash
python simulate.py
```

It will generate a detailed **Concurrency Simulation Report** showing:
- Success rate, total runtime, and request throughput.
- Average response time, 95th percentile (P95), and Max latency per endpoint (e.g., `/api/save/`, `/api/submit/`).
- Performance bottlenecks analysis, highlighting SQLite write locking and subprocess compiler load limits.
