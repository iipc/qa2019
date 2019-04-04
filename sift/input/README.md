# Purpose of this Directory

This is a stub directory for plugins which will take a url input and generate an output to be compared by the comparison plugin

each module is expected to have a function called "fetch" that takes a "url" parameter and returns a file-like object (which supports .read())

as an example:

`local_file.py`
```
fetch(url, **kwargs):
   return open(url, 'r')
```