Scraps any present laptops model number and series name from HP,Lenevo site

Get list of laptops:-

dict1 = find_lenv.find_laps(SQL=False)
dict2 = find_hp.find_laps(SQL=False)
set SQL = True if u want to save to database directly

Show data present in ur sql database:-

lenv_show_data()
hp_show_data()

Enter your SQL credentials:-

navigate to  HP\sql_connect_hp.py & Lenevo\sql_connect_len.py

mydb = SQL(Usernam="root",Password="root",Database_name="lenevo_database",Table_name="laptop_data")
mydb = SQL("root","root","hp_database","laptop_data")
