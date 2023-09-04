# Programming vacancies salary comparison

Fetch job vacancies from HeadHunter and SuperJob for several of the popular programming languages and compare their average offered salaries in the form of a table.

## How to install

Python should already be installed.

Use of virtual environment such as [venv](https://docs.python.org/3/library/venv.html) is recommended. 

Download the project files, install requirements using `pip` (or `pip3` if there is a conflict with Python2)
```commandline
pip install -r requirements.txt
```
To get data from SuperJob a secret key should be obtained from [their API webpage](https://api.superjob.ru/info/) (use has to be registered themselves and register their app)
The secret key must be put in `.env` file in root folder under `SJ_KEY`:
```
SJ_KEY = [your_key]
```
## How to use

Simply run `main.py`
```commandline
python main.py
```
**Be aware that this scripts need a lot of time to finish**  
~10 minutes (unless some of the optional arguments are selected) 

Example result:
```
(venv) d:\Users\David\PycharmProjects\API_salary>python main.py

+HeadHunter Moscow-------------+---------------------+---------------------+
| Language   | Vacancies Found | Vacancies Processed | Average Salary, RUB |
+------------+-----------------+---------------------+---------------------+
| JavaScript | 2650            | 657                 | 178363              |
| Java       | 2098            | 324                 | 224318              |
| Python     | 2579            | 440                 | 199619              |
| Ruby       | 135             | 24                  | 209937              |
| PHP        | 1213            | 511                 | 173559              |
| C++        | 1183            | 310                 | 183334              |
| C#         | 1022            | 227                 | 187039              |
| C          | 2983            | 669                 | 181425              |
| Go         | 749             | 147                 | 267607              |
| Shell      | 161             | 38                  | 197483              |
+------------+-----------------+---------------------+---------------------+

+SuperJob Moscow---------------+---------------------+---------------------+
| Language   | Vacancies Found | Vacancies Processed | Average Salary, RUB |
+------------+-----------------+---------------------+---------------------+
| JavaScript | 19              | 13                  | 150769              |
| Java       | 3               | 2                   | 171500              |
| Python     | 14              | 12                  | 103550              |
| Ruby       | 0               | 0                   | -                   |
| PHP        | 14              | 10                  | 146100              |
| C++        | 8               | 7                   | 150714              |
| C#         | 9               | 6                   | 98166               |
| C          | 9               | 7                   | 124942              |
| Go         | 4               | 3                   | 266666              |
| Shell      | 2               | 0                   | -                   |
+------------+-----------------+---------------------+---------------------+
```

### Optional settings

Scripts accept arguments:
- `-t`, `--timer` - add start and end time of script running after the results
- `-s`, `--single` - only fetch the first page of the results (the first 20 job offers)
- `--hh` - get stats only from HeadHunter
- `--sj` - get stats only from SuperJob


Programming languages used in these scripts are:

- JavaScript
- Java
- Python
- Ruby
- PHP
- C++
- C#
- C
- Go
- Shell

They are hardcoded in `handlers.py` but can be changed for whatever other languages if you wish so.

## Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).