# dishkv2

A Django-based project for managing user authentication and login status tracking.

## Project Overview

dishkv2 is a hackathon project built with Django that handles user login management and status tracking. The project maintains user authentication data and login history in a structured CSV format.

## Technologies

- **Django**: Web framework for building the application
- **Python**: Programming language
- **Python-dotenv**: Environment variable management

## Project Structure

```
dishkv2/
├── hackathon_project/    # Main Django project directory
├── requirements.txt      # Python dependencies
├── users_login_status.csv # User login status data
└── .gitignore           # Git ignore configuration
```

## Prerequisites

- Python 3.x
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/rusetiq/dishkv2.git
cd dishkv2
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory for your environment variables:
```
# Add your environment variables here
```

## Running the Project

To start the Django development server:
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## Features

- User login status tracking
- Environment-based configuration
- User authentication management

## Project Files

- `requirements.txt`: Contains Django and python-dotenv dependencies
- `.gitignore`: Configured to ignore environment files, cache, database, and IDE files
- `users_login_status.csv`: Stores user login status data

## Development

The project uses Django's standard development workflow. Make sure to:
- Use `.env` files for sensitive configuration
- Avoid committing environment files or cache
- Follow Django best practices for app structure

## License

This project is open source and available on GitHub.

## Author

rusetiq
