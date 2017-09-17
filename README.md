# Verbs in func names counter
This script calculate verbs count in func names in `.py` files.
Script check all folders recursively. Default folder names for search:\
_django, flask, pyramid, reddit, requests, sqlalchemy._\
You can add your folders to check list.

# How to install
1. Recomended use venv or virtualenv for better isolation.\
   Venv setup example: \
   `$ python3 -m venv myenv`\
   `$ source myenv/bin/activate`
2. Install requirements: \
   `pip3 install -r requirements.txt` (alternatively try add `sudo` before command)
3. Run on CLI for update `nltk` if it need:
    ```
    $ python3
    >> import nltk
    >> nltk.download('all')
    ```
4. Put script `dclint.py` on root folder with your projects.

# How to use
If you want check default folders:\
`$ python3 dclint.py`
If you want add your project folders, print it space-separated:
`$ python3 dclint.py myproject1 myproject2`

# Usage example:
We have some folders structure with `dclint.py`:
```
├── dclint.py
├── django
│   ├── css
│   ├── bootstrap.min.css
│   ├── my_app.py
│
├── flask
│   ├── favicon.ico
│   ├── polls.py
│   ├── garbage_files
│   │   ├──bootstrap.min.js
│   │   ├──html5shiv.min.js
│   │   ├──thrash.py
│   
├──myproject
│   ├──ie-emulation-modes-warning.js
│   ├──old_version.py
│   ├──new_file.py
```

In all folders - 5 `.py` files.\
All files have funcs like this (for example):
```python
def get_all_names(names):
    for name in names:
        print('name: {name}'.format(name=name))
```

```python
def give_money(user, money):
    print('{user} now have {money} $'.format(user=user,
     money=money))
```

```python
def check_exist(folder):
    if os.path.exist(folder):
        return True
```
And another funcs.

Folders `flask` and `django` already in check list, but we need add `myproject`.\
Run check:\
`$ python3 dclint.py myproject`
Result:\
````
dirpath: ./myproject:
total ".py" files count: 1
trees generated
functions extracted
verb "get" count: 1


dirpath: ./django:
total ".py" files count: 3
trees generated
functions extracted
verb "get" count: 3
verb "give" count: 2


dirpath: ./flask:
total ".py" files count: 1
trees generated
functions extracted
verb "get" count: 1


total 4 words, unique 2
"get" in 3 projects
"give" in 1 projects

````

# License

MIT license