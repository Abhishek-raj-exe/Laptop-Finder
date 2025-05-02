import requests
from bs4 import BeautifulSoup
from .Info_finder import search_in_catalogue
from .sql_connect_hp import mydb



Brand_name = "HP"
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
q_url1 = "https://www.hp.com/in-en/shop/laptops-tablets.html"
q_url2 = q_url1+"?product_list_limit=30&subbrand="

def hp_show_data():
    mydb.Show_data()

class Laptop_finder():

    def __init__(self):
        self.sr_lst = {
            "Series" : [],
            "Models" : []
        }
        self.modls = {
            "Brand" : [],
            "Series" : [],
            "Models" : []
        }
    
    def get_series_list(self):
        """Get List of available laptop series
        
        :Return: Dict of series & model qty per series
        """
        response = requests.get(url=q_url1,headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        x = soup.find("div",{"data-code":"hp_facet_subbrand"})
        x = x.find("ol",class_="items")
        x = x.find_all("li",class_="item")

        jj = 0
        
        for ii in x:
            xx = ii.find("h4",class_="attribute-value stellar-body__medium")
            xx2 = ii.find("span",class_="count stellar-body__extra-small")
            if xx.get_text().strip().upper() in ["HP ESSENTIALS"]:
                continue
            else:
                self.sr_lst["Series"].append(xx.get_text().strip())
                self.sr_lst["Models"].append(int(xx2.get_text().strip()))
                jj+=1

        # self.sr_lst["Series"] = ["OMNIBOOK X"]
        # self.sr_lst["Models"] = [5]
        
        # return self.sr_lst
    
    def find_laps(self,SQL=False):
        print("\nFinding HP laptops")
        self.get_series_list()
        if SQL:
            mydb.Del_Data()
        for index in range(len(self.sr_lst["Series"])):
            # lf.find_series(mx)
            Query = self.sr_lst["Series"][index].replace(" ","-")

            # print(f"\nSeries: {self.sr_lst["Series"][index]}  \nModels Available: {self.sr_lst["Models"][index]}")
            response = requests.get(url=q_url2+Query,headers=headers)

            soup = BeautifulSoup(response.content, "html.parser")

            """Total amount of products on page"""
            bs = soup.find("p",class_="toolbar-amount")
            bs = bs.find_all("span")
            tot_prods = max([int(x.get_text()) for x in bs])
            # print("\nTotal products found in catalogue: ",tot_prods)

            """Find product"""
            ss = soup.find("ol",class_="products list items product-items grid")
            ss = ss.find_all("li",class_="item product product-item g-col-4 g-col-xl-4 g-col-lg-6")

            res_tot = tot_prods

            searc_dic = search_in_catalogue(headers,Query,Brand_name,res_tot)
            tot_prods = len(searc_dic['m1'])

            for mm in range(0,tot_prods):
                # print(searc_dic["m2"][mm],mm,tot_prods)
                
                if SQL:mydb.New_Data(Brand_n=Brand_name,Series_n=searc_dic['m1'][mm],Model_n=searc_dic['m2'][mm])
                else:pass
                
                self.modls["Brand"].append(Brand_name)
                self.modls["Series"].append(searc_dic['m1'][mm])
                self.modls["Models"].append(searc_dic['m2'][mm])

        print("\nSearch complete")
        return self.modls
find_hp = Laptop_finder()
# for mx in range(len(lf.sr_lst["Series"])):
# lf.find_series() 