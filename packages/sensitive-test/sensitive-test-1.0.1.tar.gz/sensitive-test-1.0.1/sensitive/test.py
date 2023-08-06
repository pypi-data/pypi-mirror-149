from time import time_ns
import traceback
import sys

error_print = None
normal_print = None
NEWLINE = '\n'

if os.name == "nt":
    from .error_win import print_error, print_normal
    error_print = print_error
    normal_print = print_normal
else:
    from .error_posix import print_error, print_normal
    error_print = print_error
    normal_print = print_normal

class Test:
    __slots__ = ("name", "start")

    def __init__(self):
        self.name = None
    
    def __repr__(self) -> str:
        return f"<Test [{self.name or '<unnamed>'}]>"
    
    def __call__(self, name: str) -> None:
        if self.name is not None:
            raise Exception("Cannot create a new test when a new test is already running.")
    
        self.name = name
        return self
    
    def __enter__(self) -> None:
        if self.name is None:
            raise Exception("Don't use this instance on the if statement without calling it with a name.")

        self.start = time_ns() / 1000000
    
    def __exit__(self, exc_type, exception, tb) -> None:
        time_amount = (time_ns() / 1000000) - self.start
        
        if exception is not None:
            try:
                raise exception # get fucked xd
            except BaseException:
                error_print(f"[FAIL] {self.name} - {time_amount}ms{NEWLINE}{traceback.format_exc()}")
            
            sys.exit(1)
        else:
            normal_print(f"[SUCCESS] {self.name} - {time_amount}ms")
        
        self.name = None
        return True