# Persistent-Reverse-Shell

A Reverse Shell written in Python 2. Made exclusively for learning purposes, and as such will be detected by almost all anti-virus programs if installed maliciously.

This Reverse Shell is written based on lectures in [Joseph Delgadillo's Python Hacking Course](https://www.udemy.com/course/ethical-hacking-python/)

To actually test the program, run the executable on the target machine, and run Server2 as a python script. However, the program must be changed to accomodate the
true target's IP address and desired port number, as those are left default for now.

If the server is running while the executable is running (most likely in the background), it will connect within 20 seconds, allowing full reverse-shell access,
including moving around the file system, and uploading and downloading files.

Next steps for this project would be a port to Python 3, anti-virus obfuscation, and User IP customization.
