import sqlite3 

class database():

    #Default constructor
    def __init__(self):
        self.conn=sqlite3.connect("bank.db")
        self.cur=self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY,user TEXT, surname TEXT,account_number INTEGER UNIQUE,balance REAL,account_limit REAL)")
        self.conn.commit()
    
    #Get all users
    def get_users(self):
        self.cur.execute("SELECT * FROM users")
        rows=self.cur.fetchall()
        return rows
    
    #Add account
    def add_user(self,name,surname,acc_number,balance,limit):
        try:
            self.cur.execute("INSERT INTO users VALUES(NULL,?,?,?,?,?)",(name,surname,acc_number,balance,limit))
            self.conn.commit()
        except:
            return -1
    
    #Search account
    def search_user(self,name='',surname='',acc_number=''):
        self.cur.execute("SELECT * FROM users WHERE user=? OR surname=? OR account_number=?",(name,surname,acc_number))
        rows=self.cur.fetchall()
        return rows
    
    #Update account
    def update_user(self,name,surname,acc_number,balance,limit,id):
        self.cur.execute("UPDATE users SET user=?,surname=?,account_number=?,balance=?,account_limit=? WHERE id=?",(name,surname,acc_number,balance,limit,id))
        self.conn.commit()
    
    #Delete user
    def delete_user(self,acc_number):
        self.cur.execute("DELETE FROM users WHERE account_number=?",(acc_number,))
        self.conn.commit()
    
    #Withdraw money
    def withdrawMoney(self,name,acc_number,money):
        self.cur.execute("SELECT * FROM users WHERE user=? AND account_number=?",(name,acc_number))
        account=self.cur.fetchall()
        for el in account:
            self.act_balance=el[4]
        return self.act_balance
    
    #Delete constructor
    def __del__(self):
        self.conn.close()