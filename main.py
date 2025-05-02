from Lenovo.lenevo_scrapper import find_lenv,lenv_show_data
from HP.hp_scrapper import find_hp,hp_show_data

dict1 = find_lenv.find_laps()
lenv_show_data()
dict2 = find_hp.find_laps()
hp_show_data()