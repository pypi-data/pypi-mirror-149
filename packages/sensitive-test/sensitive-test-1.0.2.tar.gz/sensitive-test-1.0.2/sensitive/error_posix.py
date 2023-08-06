from ctypes import CDLL, c_size_t, c_int, c_char_p

libc = CDLL("libc.so.6")
write = libc.write
stderr = c_int(2)

red = c_char_p(b"\x1b[91m")
reset = c_char_p(b"\n\x1b[0m")

five = c_size_t(5)

print_normal = lambda s: libc.puts(c_char_p(bytes(s, "utf8")))

def print_error(text: str, end: str = "\n"):
    write(stderr, red, five)
    write(stderr, c_char_p(bytes(text, "utf8")), c_size_t(len(text)))
    write(stderr, reset, five)