import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
import datetime

try:
    with open("Books.txt",'r'):
        pass
except FileNotFoundError:
    with open("Books.txt",'w'):
        pass

try:
    with open("Users.txt",'r'):
        pass
except FileNotFoundError:
    with open("Users.txt",'w') as user:
        AdminPasswordPage = ctk.CTk()
        AdminPasswordPage.geometry("250x250")
        AdminPasswordPage.title("Create Admin Account")
        loginPassEntry = ctk.CTkEntry(master=AdminPasswordPage, height = 30, placeholder_text="Admin Password", border_color="#1a1a1a", border_width=2, font=("Arial",12), show = "*")
        loginPassEntry.place(relx=0.5, rely=0.5, anchor="center")
        loginButton = ctk.CTkButton(master=AdminPasswordPage, corner_radius = 5, text="Create", fg_color="#595959", hover_color="#1a1a1a", border_color="#1a1a1a", border_width=2, command = lambda: [user.write(f"Admin;{hashlib.sha256(loginPassEntry.get().encode()).hexdigest()};0,0,0\n"),AdminPasswordPage.destroy()]) 
        loginButton.place(relx = 0.5, rely = 0.6, anchor = "center")
        AdminPasswordPage.mainloop()

def Destroy():
    for i in root.winfo_children():
        i.destroy()

CurrentUser = ""
root = ctk.CTk()
root.geometry("800x500")
root.configure(bg = "#000000")
root.title("Library Management System")

def login(userEntry, passwordEntry):
    global CurrentUser
    CurrentUser=""
    user = userEntry.get()
    password = passwordEntry.get()
    with open("Users.txt","r") as Users:
        for i in Users:
            il = i.rstrip("\n").split(";")
            if user == il[0]:
                if hashlib.sha256(password.encode()).hexdigest() == il[1]:
                    if user == 'Admin':
                        CurrentUser = user
                        adminPage()
                        return
                    CurrentUser = user
                    UserPage()
                    return
        passwordEntry.delete(0, ctk.END)
        loginFailLabel = ctk.CTkLabel(master=root, text="Username or Password is Wrong!", text_color="#ad0000", font=("Arial",12))
        loginFailLabel.place(relx = 0.5, rely = 0.55, anchor = "center")

def createAccount(userEntry,passwordEntry,repasswordEntry):
    user = userEntry.get()
    password = passwordEntry.get()
    repassword = repasswordEntry.get()
    with open("Users.txt","r") as Users:
        users = []
        for i in Users:
            users.append(i.rstrip("\n").split(";")[0])
    with open("Users.txt","a") as  Users:
        if len(user)<3:
            createAccFailLabel = ctk.CTkLabel(master=root, text="Username too Short!", width = 100, text_color="#ad0000", font=("Arial",10))
            createAccFailLabel.place(relx = 0.5, rely = 0.55, anchor = "center")
            passwordEntry.delete(0,ctk.END)
            repasswordEntry.delete(0,ctk.END)
            return
        if user in users: 
            createAccFailLabel = ctk.CTkLabel(master=root, text="User Already Exists!", text_color="#ad0000", font=("Arial",10))
            createAccFailLabel.place(relx = 0.5, rely = 0.55, anchor = "center")
            passwordEntry.delete(0,ctk.END)
            repasswordEntry.delete(0,ctk.END)
            return
        if len(password) < 8:
            createAccFailLabel = ctk.CTkLabel(master=root, text="Password too Short!", text_color="#ad0000", font=("Arial",10))
            createAccFailLabel.place(relx = 0.5, rely = 0.55, anchor = "center")
            passwordEntry.delete(0,ctk.END)
            repasswordEntry.delete(0,ctk.END)
            return
        if password == repassword:
            Users.write(f"{user};{hashlib.sha256(password.encode()).hexdigest()};0,0,0\n")
            LoadLoginPage()
        else:
            createAccFailLabel = ctk.CTkLabel(master=root, text="Password not matching!", text_color="#ad0000", font=("Arial",10))
            createAccFailLabel.place(relx = 0.5, rely = 0.55, anchor = "center")
            passwordEntry.delete(0,ctk.END)
            repasswordEntry.delete(0,ctk.END)

style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", background="#2a2d2e",foreground="white",rowheight=25,fieldbackground="#343638",bordercolor="#343638",borderwidth=0)
style.map('Treeview', background=[('selected', '#22559b')])
style.configure("Treeview.Heading",background="#565b5e",foreground="white",relief="flat")
style.map("Treeview.Heading",background=[('active', '#3484F0')])

def buildTable():
    columns=("ID","Name","Author","Status","Issuer","Date")
    Headers = ["Book ID","Book Name","Author name","Status","Current Issuer","Date Last Issued"]
    Table = ttk.Treeview(master=root, columns=columns, show="headings")
    for i in range(len(columns)):
        Table.heading(columns[i], text=Headers[i])
    Table.column("ID",width=50,stretch=False)
    Table.column("Status",width=82,stretch=False)
    Table.column("Date",width=95,stretch=False)
    with open("Books.txt", "r") as books:
        matches = []
        Status = lambda X : "Avaiable" if X == "1" else "Not Available"
        for book in books:
            BoookDetails = book.split(";")
            BoookDetails[-1] = BoookDetails[-1].rstrip("\n")
            BoookDetails[3] = Status(BoookDetails[3])
            matches.append(BoookDetails)
        ind = 0
        for i in matches:
            Table.insert(parent="",index=ind,values=i)
            ind+=1
    return Table

def UserPage():
    Destroy()
    SearchEntry = ctk.CTkEntry(master=root, height = 30, width=500, placeholder_text="Search", border_color="#1a1a1a", border_width=2, font=("Arial",12))
    SearchEntry.grid(row=0, column=0, sticky=(tk.W))
    SearchButton = ctk.CTkButton(master=root, corner_radius = 5, text="Search", fg_color="#595959", hover_color="#1a1a1a", border_color="#1a1a1a", border_width=2, command = lambda: search(Table, SearchEntry.get()))
    SearchButton.grid(row=0, column=1, sticky=(tk.W))
    LogoutButton = ctk.CTkButton(master=root, corner_radius = 50, text="Logout", fg_color="#595959", hover_color="#1a1a1a", border_color="#1a1a1a", border_width=2, command = lambda: LoadLoginPage())
    LogoutButton.grid(row=0, column=2, sticky=(tk.W))
    Table = buildTable()
    Table.grid(row=1, column=0, columnspan=3, sticky="nsew")
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(1, weight=1)
    runIssue = lambda x : issue(Table)
    deselect = lambda x : Table.selection_remove(*Table.selection())
    Table.bind('<Double-1>', runIssue)
    Table.bind('<Button-1>', deselect)

def adminPage():
    Destroy()
    SearchEntry = ctk.CTkEntry(master=root, height = 30, width=500,  placeholder_text="Search", border_color="#1a1a1a", border_width=2, font=("Arial",12))
    SearchEntry.grid(row=0, column=0, columnspan = 2, sticky=(tk.W))
    SearchButton = ctk.CTkButton(master=root, corner_radius = 5, text="Search", fg_color="#595959", hover_color="#1a1a1a", border_color="#1a1a1a", border_width=2, command = lambda: search(Table, SearchEntry.get()))
    SearchButton.grid(row=0, column=2, sticky="w")
    LogoutButton = ctk.CTkButton(master=root, corner_radius = 50, text="Logout", fg_color="#595959", hover_color="#1a1a1a", border_color="#1a1a1a", border_width=2, command = lambda: LoadLoginPage())
    LogoutButton.grid(row=0, column=3, sticky=(tk.W))
    DeleteButton = ctk.CTkButton(master=root, width = 100, corner_radius = 5, text="Delete Book", fg_color="#595959", hover_color="#1a1a1a", border_color="#1a1a1a", border_width=2, command  = lambda: DeleteBook(Table))
    EditButton = ctk.CTkButton(master=root, width = 100, corner_radius = 5, text="Edit Book", fg_color="#595959", hover_color="#1a1a1a", border_color="#1a1a1a", border_width=2, command = lambda: ModifyBookWindow(Table))
    AddButton = ctk.CTkButton(master=root, width = 100, corner_radius = 5, text="Add Book", fg_color="#595959", hover_color="#1a1a1a", border_color="#1a1a1a", border_width=2, command = lambda: AddBookWindow())
    Table = buildTable()
    Table.grid(row=1, column=0, columnspan=4, sticky="nsew")
    DeleteButton.grid(row=2, column=0)
    EditButton.grid(row=2, column=1, sticky="nsw")
    AddButton.grid(row=2, column=1, padx = 100, sticky="nsw")
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(1, weight=1)
    runReturnBook = lambda x : ReturnBook(Table)
    deselect = lambda x : Table.selection_remove(*Table.selection())
    Table.bind('<Double-1>', runReturnBook)
    Table.bind('<Button-1>', deselect)

def DeleteBook(Table):
    selected_items = Table.selection()
    if len(selected_items) == 0:
        messagebox.showerror(title="Not Selected", message="Book Not Selected.")
        return
    bookid = Table.item(selected_items[0])['values'][0]
    answer = messagebox.askyesno(title='confirmation', message='Are you sure that you want to Delete the selected Book?')
    global CurrentUser
    if answer:
        with open("Books.txt","r+") as File:
            Books = list(File)
            index = 0
            index = findIndex(bookid, Books)
            if index != -1:
                Books.pop(index)
                File.seek(0)
                File.truncate(0)
                File.writelines(Books)
        adminPage()

def ModifyBookWindow(Table):
    global CurrentUser
    selected_items = Table.selection()
    if len(selected_items) == 0:
        messagebox.showerror(title="Not Selected", message="Book Not Selected.")
        try:
            ModifyBookPopup.destroy()
        except:
            pass
        return
    bookid = Table.item(selected_items[0])['values'][0]
    answer = messagebox.askyesno(title='confirmation', message='Are you sure that you want to Edit the selected Book?')
    if answer:
        ModifyBookPopup = ctk.CTkToplevel()
        ModifyBookPopup.geometry('500x120')
        ModifyBookPopup.title('Add Book')
        ModifyBookPopup.attributes("-topmost","true")
        ModifyBookPopup.resizable(width=False, height=False)
        with open("Books.txt","r+") as File:
            Books = list(File)
            index = findIndex(bookid, Books)
            if index != -1:
                book = Books[index].split(";")
                NameEntry = ctk.CTkEntry(master=ModifyBookPopup, height = 30, width=500,  placeholder_text=f"Book's Name: {book[1]}", border_color="#1a1a1a", border_width=2, font=("Arial",12))
                NameEntry.grid(row = 0, column = 0)
                AuthorEntry = ctk.CTkEntry(master=ModifyBookPopup, height = 30, width=500,  placeholder_text=f"Author's Name: {book[2]}", border_color="#1a1a1a", border_width=2, font=("Arial",12))
                AuthorEntry.grid(row = 1, column = 0)
                ModifyButton = ctk.CTkButton(master=ModifyBookPopup, width = 100, corner_radius = 5, text="Modify Book", fg_color="#595959", hover_color="#1a1a1a", border_color="#1a1a1a", border_width=2, command = lambda: ModifyBook(NameEntry.get(),AuthorEntry.get(), index, ModifyBookPopup))
                ModifyButton.grid(row = 2, column = 0)
            else:
                messagebox.showerror(title="Not Found", message="Book Not Found.")
    else:
        try:
            ModifyBookPopup.destroy()
        except:
            pass
        return

def ModifyBook(name, author, index, window):
    with open('Books.txt','r') as Books:
        listBooks = list(Books)
    with open('Books.txt','w') as Books:
        book = listBooks[index].split(";")
        if name:
            book[1] = name
        if author:
            book[2] = author   
        listBooks[index] = ";".join(book)
        messagebox.showinfo(title="New Info", message="ID: {0}, Name: {1} Author: {2}".format(*book))
        Books.seek(0)
        Books.truncate(0)
        Books.writelines(listBooks)
    window.destroy()
    adminPage()

def AddBookWindow():
    AddBookPopup = ctk.CTkToplevel()
    AddBookPopup.geometry('500x120')
    AddBookPopup.title('Add Book')
    AddBookPopup.attributes("-topmost","true")
    AddBookPopup.resizable(width=False, height=False)
    BookIDEntry = ctk.CTkEntry(master=AddBookPopup, height = 30, width=500,  placeholder_text="Book's ID", border_color="#1a1a1a", border_width=2, font=("Arial",12))
    BookIDEntry.grid(row = 0, column = 0)
    NameEntry = ctk.CTkEntry(master=AddBookPopup, height = 30, width=500,  placeholder_text="Book's Name", border_color="#1a1a1a", border_width=2, font=("Arial",12))
    NameEntry.grid(row = 1, column = 0)
    AuthorEntry = ctk.CTkEntry(master=AddBookPopup, height = 30, width=500,  placeholder_text="Author's Name", border_color="#1a1a1a", border_width=2, font=("Arial",12))
    AuthorEntry.grid(row = 2, column = 0)
    AddButton = ctk.CTkButton(master=AddBookPopup, width = 100, corner_radius = 5, text="Add Book", fg_color="#595959", hover_color="#1a1a1a", border_color="#1a1a1a", border_width=2, command = lambda: AddBook(BookIDEntry.get(),NameEntry.get(),AuthorEntry.get(),AddBookPopup))
    AddButton.grid(row = 4, column = 0)

def AddBook(id, name, author, window):
    with open('Books.txt','r') as Books:
        listBooks = list(Books)
    with open('Books.txt','a') as Books:
        if findIndex(id, listBooks) == -1:
            Books.write(f"{id};{name};{author};1;;\n")
        else:
            messagebox.showerror(title="Already Exists", message="BookID Already Exists.")
    window.destroy()
    adminPage()

def ReturnBook(Table):
    selected_items = Table.selection()
    bookid = Table.item(selected_items[0])['values'][0]
    answer = messagebox.askyesno(title='confirmation', message='Are you sure that you want to Return the selected Book?')
    global CurrentUser
    if answer:
        with open("Books.txt","r+") as File:
            Books = list(File)
            index = findIndex(bookid, Books)
            if index != -1:
                book = Books[index].split(";")
                if book[3] == "0":
                    book[3] = "1"
                    book[4] = ""
                    Books[index] = ";".join(book)
                    messagebox.showinfo(title="Returned", message="ID: {0}, Name: {1} Returned.".format(*book))
                    File.seek(0)
                    File.truncate(0)
                    File.writelines(Books)
                else:
                    messagebox.showerror(title="Already issued", message="Book Not Issued.")
            else:
                messagebox.showerror(title="Not Found", message="Book Not Found.")
        adminPage()

def issue(Table):
    selected_items = Table.selection()
    bookid = Table.item(selected_items[0])['values'][0]
    answer = messagebox.askyesno(title='confirmation', message='Are you sure that you want to Issue the selected Book?')
    global CurrentUser
    if answer:
        with open("Books.txt","r+") as File:
            Books = list(File)
            index = findIndex(bookid, Books)
            if index != -1:
                book = Books[index].split(";")
                if book[3] == "1":
                    book[3] = "0"
                    book[4] = CurrentUser
                    x = datetime.date.today()
                    book[5] = x.strftime("%d-%m-%Y")+"\n"
                    Books[index] = ";".join(book)
                    messagebox.showinfo(title="Issued", message="ID: {0}, Name: {1} Issued to {4}.".format(*book))
                    File.seek(0)
                    File.truncate(0)
                    File.writelines(Books)
                else:
                    messagebox.showerror(title="Already issued", message="Book already issued.")
            else:
                messagebox.showerror(title="Not Found", message="Book Not Found.")
        UserPage()

def search(Table, entry):
    items = Table.get_children()
    for record in items:
        Table.delete(record)
    with open("Books.txt", "r") as books:
        matches = []
        Status = lambda X : "Avaiable" if X == "1" else "Not Available"
        for book in books:
            BoookDetails = book.split(";")
            BoookDetails[-1] = BoookDetails[-1].rstrip("\n")
            BoookDetails[3] = Status(BoookDetails[3])
            if BoookDetails[1].upper().find(entry.upper()) != -1:
                matches.append(BoookDetails)
        ind = 0
        for i in matches:
            Table.insert(parent="",index=ind,values=i)
            ind+=1

def findIndex(Bookid, Books):
    index = 0
    for entry in Books:
        if entry.split(";")[0] == str(Bookid):
            return index
        else:
            index+=1
    return -1

def LoadLoginPage():
    Destroy()
    # Login ID and Password Entry Fields
    loginIDEntry = ctk.CTkEntry(master=root, height = 30, placeholder_text="Username", border_color="#1a1a1a", border_width=2, font=("Arial",12))
    loginIDEntry.place(relx=0.5, rely=0.43, anchor="center")
    loginPassEntry = ctk.CTkEntry(master=root, height = 30, placeholder_text="Password", border_color="#1a1a1a", border_width=2, font=("Arial",12), show = "*")
    loginPassEntry.place(relx=0.5, rely=0.5, anchor="center")

    # Login Button: Runs Login function
    loginButton = ctk.CTkButton(master=root, corner_radius = 5, text="Login", fg_color="#595959", hover_color="#1a1a1a", border_color="#1a1a1a", border_width=2, command = lambda: login(loginIDEntry,loginPassEntry)) 
    loginButton.place(relx = 0.5, rely = 0.6, anchor = "center")

    # Create Account Button: Loads Create acount page
    createAccPageButton = ctk.CTkButton(master=root, corner_radius = 5, text="Create new account", fg_color="#595959", hover_color="#1a1a1a", border_color="#1a1a1a", border_width=2,  command = lambda: LoadCreateAccPage())
    createAccPageButton.place(relx = 0.5, rely = 0.66, anchor = "center")

# Create account button starts create account menu
def LoadCreateAccPage():
    Destroy()
    # Login ID and Password Entry Fields
    createAccIDEntry = ctk.CTkEntry(master=root, height = 30, placeholder_text="Username", border_color="#1a1a1a", border_width=2, font=("Arial",12))
    createAccIDEntry.place(relx=0.5, rely=0.33, anchor="center") 
    createAccPassEntry = ctk.CTkEntry(master=root, height = 30, placeholder_text="Password", border_color="#1a1a1a", border_width=2, font=("Arial",12), show = "*")
    createAccPassEntry.place(relx=0.5, rely=0.43, anchor="center") 
    createAccRePassEntry = ctk.CTkEntry(master=root, height = 30, placeholder_text="Re-enter Password", border_color="#1a1a1a", border_width=2, font=("Arial",12), show = "*")
    createAccRePassEntry.place(relx=0.5, rely=0.5, anchor="center")

    # Login Button: Runs Login function
    createAccButton = ctk.CTkButton(master=root, corner_radius = 5, text="Create account", fg_color="#595959", hover_color="#1a1a1a", border_color="#1a1a1a", border_width=2, command = lambda: createAccount(createAccIDEntry,createAccPassEntry,createAccRePassEntry)) 
    createAccButton.place(relx = 0.5, rely = 0.6, anchor = "center")

    # Create Account Button: Loads Create acount page
    loginPageButton = ctk.CTkButton(master=root, corner_radius = 5, text="Already have an account?", fg_color="#242424", hover_color="#292929",  command = lambda: LoadLoginPage())
    loginPageButton.place(relx = 0.5, rely = 0.66, anchor = "center")

LoadLoginPage()
root.mainloop()
