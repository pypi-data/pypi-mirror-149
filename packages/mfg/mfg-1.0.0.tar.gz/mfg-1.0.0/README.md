# Message Foreground

[![License](https://img.shields.io/badge/License-MIT-blue)](#license)

This library allows you to create a message that is displayed in the foreground and above all other elements.


Simple Demo
-----------
```python
# Import the library
from mfg import foreground

# First create a instance with the following parameters
# 	Text: 'Hello World'
# 	Color: White
# 	No background
f = foreground('Hello World', '#fffffe')

# Displayed the message
f.display()
```


Requirement
---------------
- `tkinter`
- `win32api`
- `win32con`
- `threading`
- `pywintypes`


Development
-----------

This library can be improved and if you want to be part of it, contact me.
