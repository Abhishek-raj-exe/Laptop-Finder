A scrapper to get any present laptops model numbers and series name from HP,Lenevo website

### Get list of laptops:-
```
dict1 = find_lenv.find_laps(SQL=False)
dict2 = find_hp.find_laps(SQL=False)
```
set SQL = True if u want to save to database directly

### Show data present in ur sql database:-
```
lenv_show_data()
hp_show_data()
```
## SQL usage

Create a database in mysql with table consisting of three columns
Brand_name varchar(15) 
Series_name varchar(30) 
Model_num varchar(40)

### Enter your SQL credentials:-
navigate to  HP\sql_connect_hp.py & Lenevo\sql_connect_len.py

```
SQL(Username,Passworde,Database_name,Table_name) --> Parameters
mydb = SQL("root","root","hp_database","laptop_data") --> Example
```
