import requests
from math import ceil
from bs4 import BeautifulSoup

def search_in_catalogue(Headers,Query,Brand,tot_res):
    """Catalogue lookup
    
    :Headers -- device info for requests
    :Page_no -- WebPage number 
    :Query -- Series name

    
    Return : Dictionary to store info
    """

    Dict = {
    "m1":[],
    "m2":[],
    }
    limitt = 0

    for xi in range(1,ceil(tot_res/30)+1):
        # print('ZBOO K',xi,ceil(tot_res/30)+1)
        q_url = f"https://www.hp.com/in-en/shop/laptops-tablets.html/?p={xi}&product_list_limit=30&subbrand={Query}"
        response = requests.get(url=q_url,headers=Headers)
        soup_p = BeautifulSoup(response.content, "html.parser")
        ss2 = soup_p.find("div",class_="products wrapper grid products-grid")
        ss2 = ss2.find_all("li",class_="item product product-item g-col-4 g-col-xl-4 g-col-lg-6")
        limitt = len(ss2)
        ii = 0
        
        for mod in ss2:
            ii+=1
            
            # Series name

            m1 = mod.find("div",class_="product details product-item-details")
            m1 = m1.find("a",class_="product-item-link")
            m1 = str(m1.get("href")).split("/")[-1].split(".html")[0].split("-")
            if m1[0].upper() != Brand:
                m1.insert(0,Brand)
            if m1[1].upper() == "ZBOOK":
                Dict["m1"].append("ZBOOK")
            elif m1[1].upper() == "DRAGONFLY":
                continue
            elif len(m1[1])<len(Query):
                if m1[1].upper() in Query.upper():
                    Dict["m1"].append(Query)
                else: print("Error",m1[1] , Query); continue
            else:
                if Query.upper() in m1[1].upper():
                    Dict["m1"].append(Query)
                else: print("Error",m1[1] , Query); continue
            

            # Model no. 

            q_var = Query.upper().split("-")[0] 

            if q_var in ["ELITEBOOK","ELITE","PRO","Z","OMNIBOOK"]:
                m2 = mod.find("div",class_="product details product-item-details")
                m2 = m2.find("a",class_="product-item-link" )
                m2 = m2.get_text().strip().split(" ")
                m2 = [str(item).replace("(", "").replace(")", "") for item in m2]

                if m2[0].upper() != Brand:
                    m2.insert(0,Brand)

                if q_var == "PRO":
                    # print(m2)
                    if m2[2].lower() == "x360":
                        m2 = (m2[6]+"-"+m2[5])
                    elif m2[7].lower() == "notebook":                
                        m2 = (m2[2]+"-"+m2[6]+"-"+m2[3])
                    elif m2[5].lower() == "cm":
                        m2 = (m2[2]+"-"+m2[6]+"-"+m2[3])
                    else: 
                        m2 = (m2[2]+"-"+m2[6]+"-"+m2[5])

                elif q_var == "ELITEBOOK":
                    if m2[2].lower() == "ultra":
                        if m2[7].lower() == "business":
                            m2 = (m2[6]+"-"+m2[5])
                        else:  m2 = (m2[6]+"-"+m2[3])
                        
                    if m2[2].lower() == "x":
                        if m2[3].lower() == "flip":
                            m2 = (m2[4]+"-"+m2[7])
                        else:m2 = (m2[3]+"-"+m2[6])

                    
                elif q_var == "ELITE":
                    if m2[2].lower() == "x360":
                        m2 = (m2[3]+"-"+m2[7]+"-"+m2[6])
                    elif m2[6].lower() == "business":
                        m2 = (m2[2]+"-"+m2[6]+"-"+m2[5])
                    elif m2[3].lower() == "flip":
                        m2 = (m2[2]+"-"+m2[4]+"-"+m2[7])
                    elif len(m2) >= 10:
                        if m2[9].lower() == "ai":
                            m2 = (m2[2]+"-"+m2[4]+"-"+m2[7])
                        else: m2 = (m2[2]+"-"+m2[6]+"-"+m2[3])
                    else: m2 = (m2[2]+"-"+m2[6]+"-"+m2[3])

                elif q_var == "OMNIBOOK":
                    if m2[2].lower() == "5":
                        if m2[3].lower() == "next":
                            m2 = m2[6]
                        else: m2 = m2[4]
                    elif m2[2].lower() == "7":
                        if m2[3].lower() == "aero":
                            m2 = m2[7]
                        else: m2 = m2[4]
                    elif m2[2].lower() == "x":
                        if m2[3].lower() == "flip":
                            m2 = m2[4]
                        else: m2 = m2[7]
                    elif m2[2].lower() == "ultra":
                        if m2[3].lower() == "flip":
                            m2 = m2[5]
                        else: m2 = m2[3]
                    else: m2 = m2[4]

                elif q_var == "Z":
                    if m2[2].lower() == "x360":
                        if m2[6].lower() == "notebook":
                            m2 = (m2[3]+"-"+m2[5]+"-"+m2[4])
                    elif m2[3].lower() == "flip":
                        m2 = (m2[2]+"-"+m2[7]+"-"+m2[4])
                    elif m2[4].lower() == "cm":
                        m2 = (m2[2]+"-"+m2[6]+"-"+m2[5])
                    elif m2[6].lower() == "mobile":
                        m2 = (m2[2]+"-"+m2[5]+"-"+m2[4])
                    else :m2 = (m2[2]+"-"+m2[6]+"-"+m2[5])
            
            else:    
                # print("Wass here")
                m2 = mod.find("div",class_="product details product-item-details")
                m2 = m2.find("a",class_="product-item-link")
                m2 = str(m2.get("href")).split("/")[-1].split(".html")[0].split("-")[-2]

            Dict["m2"].append(m2)
            
            # Dict["m2"].append(m2)
        
            if ii == limitt:
                break
    return Dict

def find_model_number(Dict,Headers,Index):
    """Model finder
    
    :Dict: Dictionary to find info from
    :Headers: device info for requests
    :Index: Position of model in Dict
    """

    q_url = "https://www.hp.com/in-en/shop/catalogsearch/result/?q="+Dict["m2"][Index]
    
    response = requests.get(url=q_url,headers=Headers)
    soup = BeautifulSoup(response.content, "html.parser")
    
    soup = soup.find("strong","product name product-item-name")
    soup = soup.find("a", class_="product-item-link")
    
    q_url = "https://www.hp.com/in-en/shop/"+str(soup.get("href")).strip()+".html"

    response = requests.get(url=q_url,headers=Headers)
    soup = BeautifulSoup(response.content, "html.parser")
    # print(soup)
    """Find product_name"""
    soup1 = soup.find("div", class_="product-info-tabs-name stellar-title__small")
    try:
        n1,n2 = (soup1.get_text().strip()).split(",")
    except ValueError as e:
        n1 = soup1.get_text().strip()
    # print(Dict['m1'])
    return(Dict['m1'][1],n1[-11::])

