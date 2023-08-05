# Rename-Sequential-Files

A small rename function I created to handle documents that have the same file name during automated copy jobs. This function will allow the files to be copied by just appending a (#) to the end of the file name similar to how file systems do so. You need to pass the new directory, current file name, and the files extension and the function will return the new name with (#) if no file with the same name already exists.

For example:
```
from sequential_rename.sequential_rename import seq_rename

new_doc_name = seq_rename(r'C:\Users\[USERNAME]\Documents', 'test', '.csv')
```
