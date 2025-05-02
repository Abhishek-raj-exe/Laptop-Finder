from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from .sql_connect_len import mydb

# Step 1: Set up Selenium (Chrome example)
options = Options()
options.add_argument("--log-level=3")  # Suppress logs: 0=ALL, 1=INFO, 2=WARNING, 3=ERROR
options.add_argument("--headless")            # Run in headless mode
driver = webdriver.Edge(options=options)
driver.get('https://psref.lenovo.com/')

def lenv_show_data():
    mydb.Show_data()

class Lenevo():
    def __init__(self):
        self.modls = {
            "Brand" : [],
            "Series" : [],
            "Models" : []
        }
    def __click_it(self,path):
        try:
            # Adjust the selector below
            button = WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.XPATH,path))
            )
            button.click()
            # print("\nClick succesfull\n")
        except Exception as e:
            pass
            # print("Click failed:", e)

    def find_laps(self,SQL=False):
        print("\nFinding Lenevo laptops")
        laptop_list = {}
        Brand_name = "Lenevo"
        xpath1 = "//nav/span"

        # Step 2: Wait for the clickable element to appear and click it
        self.__click_it(xpath1)
        time.sleep(0.5)
        lis = "ul_productline"
        try:
            device_list1 = WebDriverWait(driver, 0).until(
                EC.presence_of_element_located((By.ID, lis))
            )
            prod_list = device_list1.find_elements(By.TAG_NAME,"li")
            for li in prod_list:
                laptop_list[str(li.text)] = []
        except Exception as e:
            print("Error:", e)

        inxx = len(list(laptop_list.keys()))

        for inx in range(1,inxx):
            xpath = f"//div/div/div[2]/div/ul[{inx}]"
            try:
                parent_ul = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                # Find all <li> children inside the parent
                li_list = parent_ul.find_elements(By.TAG_NAME, 'li')
                for li in li_list:
                    link = li.find_element(By.TAG_NAME, 'a')
                    link = str(link.get_attribute("href")).strip()
                    link = link.replace("_"," ")
                    key_n = list(laptop_list.keys())[inx-1]
                    laptop_list[key_n].append(link)
            except Exception as e:
                print("Error:", e)

        if SQL:mydb.Del_Data()
        else:pass
 
        for key in list(laptop_list.keys()):
            for ind in range(len(laptop_list[key])):
                xx = laptop_list[key][ind]
                if (y:="https://psref.lenovo.com/Product/"+key+"/") in xx:
                    xx = xx[len(y):]
                try:
                    xx = list(xx.split("?"))[0]
                except:
                    pass
                xx = xx.split(" ")

                if len(xx)>3:
                    xx2 = xx[2:]
                    xx2 = '-'.join(xx2)
                else: xx2 = xx[2]
                xx = [xx[0],xx[1]+"-"+xx2]
                # xx = f"{xx[0]},{xx[1]},{xx[2]}"
                # print(Brand_name,xx)
                if SQL:mydb.New_Data(Brand_n=Brand_name,Series_n=xx[0],Model_n=xx[1])
                else:pass
                
                self.modls["Brand"].append(Brand_name)
                self.modls["Series"].append(xx[0])
                self.modls["Models"].append(xx[1])

        driver.quit()
        print("\nSearch complete")
        return laptop_list

find_lenv = Lenevo()