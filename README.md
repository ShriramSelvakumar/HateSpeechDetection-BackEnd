# Tweet Moderator Backend

## Requirements

[Install python version 3](https://www.python.org/downloads/)

Afetr installing python, use below command to install required packages

_In project directory_

```
pip install -r requirements.txt
```

If above command not working try

```
python -m pip install -r requirements.txt
```

## Running server
_In project directory_

Run below commands to _update changes_ in project
```
python .\manage.py makemigrations
python .\manage.py migrate
```

Finally, use below command to run the server
```
python .\manage.py runserver
```
