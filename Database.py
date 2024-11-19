import psycopg2

#this might need to be an object. that way i only need to provide 1 connection string 
# and then can have as many as needed for testing and stuff

class Database:
    def __init__(self,connectionString):
        self.connectionString = connectionString

    def getConnection(self):
        return psycopg2.connect(self.connectionString)
    
    def insert(self,query:str,data:tuple):
        conn = self.getConnection()
        cur = conn.cursor()
        try:
            cur.execute(query,data)
            #close DB conection 
            conn.commit()
            cur.close()
            conn.close()
            return True,'success'
        except (Exception, psycopg2.Error) as error:
            return False, str(error)
        
    def execute(self,query:str):
        conn = self.getConnection()
        cur = conn.cursor()
        try:
            cur.execute(query)
            #close DB conection 
            conn.commit()
            cur.close()
            conn.close()
            return True,'success'
        except (Exception, psycopg2.Error) as error:
            return False, str(error)
            #could return a tuple with the error for clarity 



def get_db_connection(DATABASE_URL):
    conn = psycopg2.connect(DATABASE_URL)
    return conn
