import subprocess
import sys
import ast

def run_python_code(code, input_data="", inject_var=None):
    python_cmd = 'python' if sys.platform == 'win32' else 'python3'

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
                    val = ast.literal_eval(input_data)
                    prefix = f"{inject_var} = {repr(val)}\n"
                except Exception:
                    prefix = f"{inject_var} = {repr(input_data)}\n"
        user_code = prefix + code
    else:
        user_code = code

    sandbox = """
import json
from typing import List, Dict, Tuple, Set, Optional, Union

BLOCKED = {
    'os', 'subprocess', 'shutil', 'pathlib', 'socket',
    'requests', 'urllib', 'http', 'ftplib', 'smtplib',
    'importlib', 'builtins', 'ctypes', 'multiprocessing',
    'threading', 'signal', 'pty', 'tty', 'termios',
    'pwd', 'grp', 'resource', 'syslog', 'platform',
    'winreg', 'winsound', 'msvcrt', 'concurrent',
    'asyncio', 'code', 'codeop', 'compileall', 'inspect',
}

def _setup_sandbox():
    import sys as _sys
    import inspect as _inspect

    _original_import = __builtins__.__import__ if hasattr(__builtins__, '__import__') else __import__
    _original_compile = __builtins__.compile if hasattr(__builtins__, 'compile') else compile
    _currentframe = _inspect.currentframe

    def _blocked_import(name, *args, **kwargs):
        base = name.split('.')[0]
        if base in BLOCKED:
            raise ImportError(f"Module '{name}' is not allowed.")
        if base == 'sys':
            raise ImportError(f"Module 'sys' is not allowed.")
        return _original_import(name, *args, **kwargs)

    def _blocked_compile(*args, **kwargs):
        try:
            frame = _currentframe()
            while frame:
                if frame.f_code.co_name == 'literal_eval' and frame.f_code.co_filename.endswith('ast.py'):
                    return _original_compile(*args, **kwargs)
                frame = frame.f_back
        except Exception:
            pass
        raise PermissionError("compile() is not allowed.")

    __builtins__.__import__ = _blocked_import
    __builtins__.compile = _blocked_compile
    __builtins__.open = lambda *a, **k: (_ for _ in ()).throw(PermissionError("File access is not allowed."))
    __builtins__.exec = lambda *a, **k: (_ for _ in ()).throw(PermissionError("exec() is not allowed."))

    # clean up sys modules
    _sys.modules.pop('os', None)
    _sys.modules.pop('subprocess', None)
    _sys.modules.pop('shutil', None)
    _sys.modules.pop('socket', None)
    _sys.modules.pop('signal', None)
    _sys.modules.pop('inspect', None)

    for _mod_name in list(_sys.modules.keys()):
        _base = _mod_name.split('.')[0]
        if _base in BLOCKED:
            del _sys.modules[_mod_name]

_setup_sandbox()
del _setup_sandbox
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