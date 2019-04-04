# Purpose of this Directory

This is a stub directory for modules which should contain a function called "compare" that takes two file-like objects and returns a two-tuple containing a numeric score and a json-serializable metadata object

e.g.

```
"""Long Module Name
The first line of the module docstring will be considered the long module name for UI display"""

compare(file_a, file_b):
    string_a = file_a.read()
    string_b = file_b.read()
    output = perform_computation(string_a, string_b)
    return (output, [{'example': 'metadata'}])
```