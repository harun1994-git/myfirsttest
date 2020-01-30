from tkinter import *
from tkinter import Scrollbar
import app_backend as database
from tkinter import simpledialog
from tkinter import messagebox

class Window(object):
    #Default constructor
    def __init__(self,window):

        #Initialize database
        self.bankDb=database.database()

        #Define window and title of window
        self.window=window
        self.window.wm_title("Bank application")

        #Define label for name
        lbl1=Label(window,text="Name:")
        lbl1.grid(row=0,column=0)

        #Define label for account number
        lbl2=Label(window,text="Acc number:")
        lbl2.grid(row=0,column=2)

        #Define label for surname
        lbl3=Label(window,text="Surname:")
        lbl3.grid(row=1,column=0)

        #Define label for balance
        lbl4=Label(window,text="Balance:")
        lbl4.grid(row=1,column=2)

        #Define label for account limit
        lbl5=Label(window,text="Account limit:")
        lbl5.grid(row=2,column=2)

        #Define entry field for Name
        self.Name=StringVar()
        self.entName=Entry(window,textvariable=self.Name)
        self.entName.grid(row=0,column=1)

        #Define entry field for account number
        self.AccNum=StringVar()
        self.entAccNum=Entry(window,textvariable=self.AccNum)
        self.entAccNum.grid(row=0,column=3)

        #Define entry field for Surname
        self.Surname=StringVar()
        self.entSurname=Entry(window,textvariable=self.Surname)
        self.entSurname.grid(row=1,column=1)

        #Define entry field for Balance
        self.Balance=StringVar()
        self.entBalance=Entry(window,textvariable=self.Balance)
        self.entBalance.grid(row=1,column=3)

        #Define entry field for Account limit
        self.Limit=StringVar()
        self.entLimit=Entry(window,textvariable=self.Limit)
        self.entLimit.grid(row=2,column=3)

        #Listbox for displaying data
        self.listBox=Listbox(window,height=6,width=45)
        self.listBox.grid(row=3,column=0,rowspan=6,columnspan=2)

        #Scrollbar for listbox
        self.scrlBar=Scrollbar(window)
        self.scrlBar.grid(row=3,column=2,rowspan=6)

        #Bind scrollbar to listbox
        self.listBox.configure(yscrollcommand=self.scrlBar.set)
        self.scrlBar.configure(command=self.listBox.yview)

        #Get selected row
        self.listBox.bind('<<ListboxSelect>>',self.get_selected_row)

        #Button get users
        self.btnGetUsers=Button(window,command=self.get_all_command,width=12,text="Get accounts")
        self.btnGetUsers.grid(row=3,column=3)

        #Button add user
        self.btnAddUsers=Button(window,command=self.add_command,width=12,text="Add account")
        self.btnAddUsers.grid(row=4,column=3)

        #Button update users
        self.btnUpdateUsers=Button(window,command=self.update_command,width=12,text="Update account")
        self.btnUpdateUsers.grid(row=5,column=3)
       
        #Button delete users
        self.btnDeleteUsers=Button(window,command=self.delete_command,width=12,text="Delete account")
        self.btnDeleteUsers.grid(row=6,column=3)

        #Button search users
        self.btnSearchUsers=Button(window,command=self.search_command,width=12,text="Search account")
        self.btnSearchUsers.grid(row=7,column=3)

        #Button withdraw money
        self.btnWithdraw=Button(window,command=self.withdraw_command,width=12,text="Withdraw money")
        self.btnWithdraw.grid(row=8,column=3)

        #Button deposit money
        self.btnDeposit=Button(window,command=self.deposit_command,width=12,text="Deposit money")
        self.btnDeposit.grid(row=9,column=3)


    #Get selected row method
    def get_selected_row(self,event):
        index=self.listBox.curselection()
        if index!=():
            self.selectedRow=self.listBox.get(index)
            self.populate()

    #Populate entry with selection
    def populate(self):
        self.clear_fields()
        self.entName.insert(END,self.selectedRow[1])
        self.entSurname.insert(END,self.selectedRow[2])
        self.entAccNum.insert(END,self.selectedRow[3])
        self.entBalance.insert(END,self.selectedRow[4])
        self.entLimit.insert(END,self.selectedRow[5])
        
    #Get command
    def get_all_command(self):
        self.listBox.delete(0,'end')
        self.clear_fields()
        for rows in self.bankDb.get_users():
            self.listBox.insert(END,rows)
    
    #Add user
    def add_command(self):
        if len(self.entName.get())>0 and len(self.entSurname.get())>0 and len(self.entAccNum.get())>0:
            err=self.bankDb.add_user(self.entName.get(),self.entSurname.get(),self.entAccNum.get(),self.entBalance.get(),self.entLimit.get())
            if err:
                messagebox.showinfo("Warning",message="Account already in database!!!")
            self.clear_fields()
            self.get_all_command()

    #Update user
    def update_command(self):
        self.bankDb.update_user(self.entName.get(),self.entSurname.get(),self.entAccNum.get(),self.entBalance.get(),self.entLimit.get(),self.selectedRow[0])
        self.clear_fields()
        self.get_all_command()

    #Delete user
    def delete_command(self):
        self.bankDb.delete_user(self.entAccNum.get())
        self.clear_fields()
        self.get_all_command()

    #Search user
    def search_command(self):
        self.listBox.delete(0,'end')
        rows=self.bankDb.search_user(self.entName.get(),self.entSurname.get(),self.entAccNum.get())
        self.clear_fields()                   
        for el in rows:
            self.listBox.insert(END,el)

    #Withdraw money
    def withdraw_command(self):
        withdraw_val=simpledialog.askfloat(title="Request",prompt="Enter withdraw value:")
        current_balance=self.bankDb.search_user(NONE,NONE,self.entAccNum.get())
        for el in current_balance:
            current_balance=el[4]
            current_limit=el[5]
        if (current_balance + abs(current_limit)) <=withdraw_val:
            messagebox.showinfo("Warning",message="Limit reached. Your limit is "+self.entLimit.get())
        else:
            self.bankDb.update_user(self.entName.get(),self.entSurname.get(),self.entAccNum.get(),(current_balance-withdraw_val),self.entLimit.get(),self.selectedRow[0])
            self.clear_fields()
        self.get_all_command()

    #Deposit money
    def deposit_command(self):
        deposit_val=simpledialog.askfloat(title="Request",prompt="Enter deposit value:")
        current_balance=self.bankDb.search_user(NONE,NONE,self.entAccNum.get())
        for el in current_balance:
            current_balance=el[4]
        self.bankDb.update_user(self.entName.get(),self.entSurname.get(),self.entAccNum.get(),float(deposit_val+float(current_balance)),self.entLimit.get(),self.selectedRow[0])
        self.clear_fields()
        self.get_all_command()
    
    #Clear entry fields
    def clear_fields(self):
        self.entName.delete(0,'end')
        self.entSurname.delete(0,'end')
        self.entAccNum.delete(0,'end')
        self.entBalance.delete(0,'end')
        self.entLimit.delete(0,'end')

#Main programm
main_window=Tk()
Window(main_window)
main_window.mainloop()