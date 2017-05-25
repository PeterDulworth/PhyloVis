import os

filename = "windows/foo.txt"

if not os.path.exists(filename):
    os.makedirs("windows")

with open(filename, "w") as f:
    f.write("FOOBAR")