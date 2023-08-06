__author__ = "anwenhu"
__date__ = "2022/5/4 23:00"
__version__ = "1.1.6"

from zhixuewang.account import (login, login_id, rewrite_str, login_student, login_teacher,
                            login_student_id, login_teacher_id, load_account)
from zhixuewang.session import get_session, get_session_id
VERSION = tuple(map(int, __version__.split('.')))
__all__ = [
    "login",
    "login_id",
    "rewrite_str",
    "login_student",
    "login_teacher",
    "login_student_id",
    "login_teacher_id",
    "get_session",
    "get_session_id",
    "load_account",
]
