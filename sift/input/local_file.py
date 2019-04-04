'''Local File Input Module
The `fetch` function returns a file handle to a local path.'''

fetch(url):
   return open(url, 'r')
