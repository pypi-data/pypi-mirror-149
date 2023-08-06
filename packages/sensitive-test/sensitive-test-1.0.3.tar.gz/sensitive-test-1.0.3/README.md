# tests

```
pip install sensitive-test
```

A small, simple, and fast ordered fail-fast tests suite for Python.

```py
import sensitive

# any Exception thrown will make the test running it fail,
# and the program will immediately return exit code 1.

with sensitive.test("test name 1"):
  print("Oh yes")

with sensitive.test("test name 2"):
  raise Exception("Trolled")

with sensitive.test("test name 3"):
  print("oh no")
```