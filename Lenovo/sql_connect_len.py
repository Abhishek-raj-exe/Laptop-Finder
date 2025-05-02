import mysql.connector as myc
from mysql.connector.errors import IntegrityError

a1 = "HP"
a2 = "PAVILION"
a3 = "14-EK1010TU"

class SQL:
    def __init__(self,User,Pass,Db_Name,Tb_Name):
        """Mysql login
        
        :User -- Username
        :Pass -- Password
        :Db_name -- Database_Name
        :Table_n -- Table name
        
        Return: None
        """

        self.User = User
        self.Pass = Pass
        self.Db_Name = Db_Name
        self.Tb_Name = Tb_Name
        
        self.db = myc.connect(
            host = "localhost",
            username = self.User,
            password = self.Pass,
            database = self.Db_Name,
        )
        self.mc = self.db.cursor()

    def New_Data(self,Brand_n,Series_n,Model_n):
        """Creates fresh new data cells
        :Brand_n -- Brand name
        :Series_n -- Series name
        :Model_n -- Model name

        Return: None
        """
        try:
            self.mc.execute(f"INSERT INTO {self.Tb_Name} (Brand_name, Series_name, Model_num) VALUES (%s, %s, %s)", (Brand_n, Series_n, Model_n))
            self.db.commit()
        except IntegrityError as e:
            e = str(e)
            x,y = e[e.find("'")::].split(" for key ")
            print(f"Entry failed.!! Duplicate entry of {x} in key {y}")
    
    def Del_Data(self):
        self.mc.execute(f"DELETE FROM {self.Tb_Name}")
        self.db.commit()

    def Show_data(self):
        self.mc.execute(f"SELECT * FROM {self.Tb_Name}")
        for x in self.mc:
            print(x)

mydb = SQL("root","root","lenevo_database","laptop_data")
