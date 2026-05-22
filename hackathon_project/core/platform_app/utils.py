import subprocess
import sys

def run_python_code(code, input_data="", inject_var=None):
    python_cmd = 'python' if sys.platform == 'win32' else 'python3'

    # Inject variable before user code if specified
    if inject_var:
        try:
            val = int(input_data)
            prefix = f"{inject_var} = {val}\n"
        except ValueError:
            try:
                val = float(input_data)
                prefix = f"{inject_var} = {val}\n"
            except ValueError:
                try:
                    val = eval(input_data)
                    prefix = f"{inject_var} = {repr(val)}\n"
                except:
                    prefix = f"{inject_var} = {repr(input_data)}\n"
        user_code = prefix + code
    else:
        user_code = code

    # Wrap in sandbox that blocks dangerous modules
    sandbox = """
import sys
import json
import inspect
from typing import List, Dict, Tuple, Set, Optional, Union

BLOCKED = {
    'os', 'sys', 'subprocess', 'shutil', 'pathlib', 'socket',
    'requests', 'urllib', 'http', 'ftplib', 'smtplib',
    'importlib', 'builtins', 'ctypes', 'multiprocessing',
    'threading', 'signal', 'pty', 'tty', 'termios',
    'pwd', 'grp', 'resource', 'syslog', 'platform',
    'winreg', 'winsound', 'msvcrt',
}

original_import = __builtins__.__import__ if hasattr(__builtins__, '__import__') else __import__

def blocked_import(name, *args, **kwargs):
    try:
        frame = sys._getframe(1)
        filename = frame.f_code.co_filename
        if filename != '<string>':
            return original_import(name, *args, **kwargs)
    except Exception:
        pass
    base = name.split('.')[0]
    if base in BLOCKED:
        raise ImportError(f"Module '{name}' is not allowed.")
    return original_import(name, *args, **kwargs)

__builtins__.__import__ = blocked_import

def blocked_open(*args, **kwargs):
    raise PermissionError("File access is not allowed.")

__builtins__.open = blocked_open
__builtins__.exec = lambda *a, **k: (_ for _ in ()).throw(PermissionError("exec() is not allowed."))

# ── USER CODE BELOW ──
""" + user_code

    try:
        process = subprocess.run(
            [python_cmd, '-c', sandbox],
            input=input_data if not inject_var else "",
            capture_output=True,
            text=True,
            timeout=2.0
        )
        return process.stdout.strip(), process.stderr

    except subprocess.TimeoutExpired:
        return None, "TIMEOUT: Infinite loop detected"
    except Exception as e:
        return None, str(e)