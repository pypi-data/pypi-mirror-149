from ctypes import *

class ConsoleScreenBufferInfo(Structure):
    _fields_ = [("_unused_1", c_uint),
                ("_unused_2", c_uint),
                ("default_attributes", c_ushort),
                ("_unused_3", c_uint),
                ("_unused_4", c_uint),
                ("_unused_5", c_uint)]

csbi = ConsoleScreenBufferInfo(0, 0, 0, 0, 0, 0)

# the irony
stdout = c_void_p(windll.kernel32.GetStdHandle(-11))
stderr = c_void_p(windll.kernel32.GetStdHandle(-12))

windll.kernel32.GetConsoleScreenBufferInfo(stdout, pointer(csbi))

red = c_ushort(12)

set_console_text_attribute = windll.kernel32.SetConsoleTextAttribute
write_console = windll.kernel32.WriteConsoleW

print_normal = lambda text: write_console(stderr, c_wchar_p(text + "\n"), c_uint(len(text) + 1), None, None)

def print_error(text: str) -> None:
    set_console_text_attribute(stderr, red)
    write_console(stderr, c_wchar_p(text + "\n"), c_uint(len(text) + 1), None, None)
    set_console_text_attribute(stderr, csbi.default_attributes)