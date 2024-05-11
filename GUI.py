import customtkinter as ctk
from tkinter import ttk, messagebox
import hashlib
import datetime

class LibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System")
        self.geometry("800x500")
        self.configure(bg="#000000")
        self.current_user = ""
        self.initialize_files()
        self.login_page()

    def initialize_files(self):
        try:
            with open("Books.txt", 'r'):
                pass
        except FileNotFoundError:
            with open("Books.txt", 'w'):
                pass

        try:
            with open("Users.txt", 'r'):
                pass
        except FileNotFoundError:
            with open("Users.txt", 'w') as user_file:
                self.create_admin_account(user_file)

    # Popup to ask password for admin on first initialization
    def create_admin_account(self, user_file):
        admin_password_page = ctk.CTk()
        admin_password_page.geometry("250x250")
        admin_password_page.title("Create Admin Account")
        password_entry = ctk.CTkEntry(master=admin_password_page, placeholder_text="Admin Password", show="*")
        password_entry.pack(pady=20)
        submit_button = ctk.CTkButton(master=admin_password_page, text="Create", command=lambda: [self.submit_admin_password(password_entry.get(), user_file), admin_password_page.destroy()])
        submit_button.pack()
        admin_password_page.mainloop()

    def submit_admin_password(self, password, user_file):
        hashed = hashlib.sha256(password.encode()).hexdigest()
        user_file.write(f"Admin;{hashed};0,0,0\n")

    def login_page(self):
        self.clear_screen()
        user_entry = ctk.CTkEntry(self, placeholder_text="Username")
        user_entry.place(relx=0.5, rely=0.43, anchor="center")
        password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        password_entry.place(relx=0.5, rely=0.5, anchor="center")

        login_button = ctk.CTkButton(self, text="Login", command=lambda: self.login(user_entry.get(), password_entry.get()))
        login_button.place(relx=0.5, rely=0.6, anchor="center")

        create_acc_button = ctk.CTkButton(self, text="Create new account", command=self.create_account_page)
        create_acc_button.place(relx=0.5, rely=0.66, anchor="center")

    def login(self, username, password):
        with open("Users.txt", "r") as file:
            for line in file:
                user, hashed_pass, _ = line.strip().split(";")
                if username == user and hashlib.sha256(password.encode()).hexdigest() == hashed_pass:
                    self.current_user = user
                    self.admin_page() if user == 'Admin' else self.user_page()
                    return
        messagebox.showerror("Login Failed", "Incorrect username or password")

    def create_account_page(self):
        self.clear_screen()
        # Username Entry
        username_entry = ctk.CTkEntry(self, placeholder_text="Username", border_color="#1a1a1a", border_width=2, font=("Arial", 12))
        username_entry.place(relx=0.5, rely=0.33, anchor="center")

        # Password Entry
        password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*", border_color="#1a1a1a", border_width=2, font=("Arial", 12))
        password_entry.place(relx=0.5, rely=0.43, anchor="center")

        # Re-enter Password Entry
        re_password_entry = ctk.CTkEntry(self, placeholder_text="Re-enter Password", show="*", border_color="#1a1a1a", border_width=2, font=("Arial", 12))
        re_password_entry.place(relx=0.5, rely=0.5, anchor="center")

        # Create Account Button
        create_button = ctk.CTkButton(self, text="Create Account", fg_color="#595959", hover_color="#1a1a1a", border_color="#1a1a1a", border_width=2, command=lambda: self.create_account(username_entry.get(), password_entry.get(), re_password_entry.get()))
        create_button.place(relx=0.5, rely=0.6, anchor="center")

        # Back to Login Page Button
        back_button = ctk.CTkButton(self, text="Back to Login", fg_color="#242424", hover_color="#292929", command=self.login_page)
        back_button.place(relx=0.5, rely=0.6, anchor="center")

    def create_account(self, username, password, re_password):
        if password != re_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return
        if len(username) < 3:
            messagebox.showerror("Error", "Username too short.")
            return
        if len(password) < 8:
            messagebox.showerror("Error", "Password too short.")
            return
        with open("Users.txt", "r") as file:
            for line in file:
                user = line.strip().split(";")[0]
                if username == user:
                    messagebox.showerror("Error", "Username already exists.")
                    return
        with open("Users.txt", "a") as file:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            file.write(f"{username};{hashed_password};0,0,0\n")
        messagebox.showinfo("Success", "Account created successfully.")
        self.login_page()

    def build_table(self):
        # Styling ttk to look like rest of the widgets
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#2a2d2e",foreground="white",rowheight=25,fieldbackground="#343638",bordercolor="#343638",borderwidth=0)
        style.map('Treeview', background=[('selected', '#22559b')])
        style.configure("Treeview.Heading",background="#565b5e",foreground="white",relief="flat")
        style.map("Treeview.Heading",background=[('active', '#3484F0')])

        # Define the table columns and headers
        columns = ("ID", "Name", "Author", "Status", "Issuer", "Date")
        headers = ["Book ID", "Book Name", "Author Name", "Status", "Current Issuer", "Date Last Issued"]

        # Create the Treeview widget
        Table = ttk.Treeview(self, columns=columns, show="headings")
        for col, header in zip(columns, headers):
            Table.heading(col, text=header)
        Table.column("ID",width=50,stretch=False)
        Table.column("Status",width=82,stretch=False)
        Table.column("Date",width=95,stretch=False)

        # Load books from file and populate the table
        self.populate_table(Table)
        return Table

    def populate_table(self, Table, key = ''):
        # Deleting all elements before populating
        items = Table.get_children()
        for record in items:
            Table.delete(record)
        status = lambda x: "Available" if x == "1" else "Not Available"
        with open("Books.txt", "r") as books:
            matches = []
            for book in books:
                BookDetails = book.split(";")
                BookDetails[-1] = BookDetails[-1].rstrip("\n")
                BookDetails[3] = status(BookDetails[3])
                if BookDetails[1].upper().find(key.upper()) != -1:
                    matches.append(BookDetails)
        for index, details in enumerate(matches):
            Table.insert("", index, values=details)

    def user_page(self):
        self.clear_screen()

        # Build and display the table of books
        table = self.build_table()
        table.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Search Entry
        search_entry = ctk.CTkEntry(self, height=30, width=500, placeholder_text="Search", border_color="#1a1a1a", border_width=2, font=("Arial", 12))
        search_entry.grid(row=0, column=0, sticky="w")

        # Search Button
        search_button = ctk.CTkButton(self, corner_radius=5, text="Search", fg_color="#595959", hover_color="#1a1a1a", border_color="#1a1a1a", border_width=2,
                                        command=lambda: self.populate_table(table, search_entry.get())) 
        search_button.grid(row=0, column=1, sticky="w")

        # Logout Button
        logout_button = ctk.CTkButton(self, corner_radius=50, text="Logout", fg_color="#595959", hover_color="#1a1a1a", border_color="#1a1a1a", border_width=2, command=self.login_page)
        logout_button.grid(row=0, column=2, sticky="w")

        # Bind table actions
        table.bind('<Double-1>', lambda x: self.issue_book(table))
        table.bind('<Button-1>', lambda x: table.selection_remove(*table.selection()))

    def issue_book(self, table):
        selected_items = table.selection()
        if not selected_items:
            messagebox.showerror("Not Selected", "No book selected.")
            return
        book_id = table.item(selected_items[0])['values'][0]

        if messagebox.askyesno('Confirmation', 'Are you sure you want to issue the selected book?'):
            with open("Books.txt", "r+") as file:
                books = list(file)
                index = self.find_index(book_id, books)
                if index == -1:
                    messagebox.showerror("Not Found", "Book not found.")
                    return
                book = books[index].split(";")
                if book[3] == "1":
                    book[3] = "0"
                    book[4] = self.current_user
                    book[5] = datetime.date.today().strftime("%d-%m-%Y") + "\n"
                    books[index] = ";".join(book)
                    file.seek(0)
                    file.truncate(0)
                    file.writelines(books)
                    messagebox.showinfo("Issued", f"Book ID: {book_id}, '{book[1]}' issued to {self.current_user}.")
                else:
                    messagebox.showerror("Already Issued", "This book is already issued.")
            self.populate_table(table)
            

    def admin_page(self):
        self.clear_screen()

        # Build and display the table of books
        table = self.build_table()
        table.grid(row=1, column=0, columnspan=5, sticky="nsew")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Search Entry
        search_entry = ctk.CTkEntry(self, height=30, width=500, placeholder_text="Search", border_color="#1a1a1a", border_width=2, font=("Arial", 12))
        search_entry.grid(row=0, column=0, columnspan=3, sticky="w")

        # Search Button
        search_button = ctk.CTkButton(self, corner_radius=5, text="Search", fg_color="#595959", hover_color="#1a1a1a", border_color="#1a1a1a", border_width=2,
                                    command=lambda: self.populate_table(table, search_entry.get()))
        search_button.grid(row=0, column=2, sticky="w")

        # Logout Button
        logout_button = ctk.CTkButton(self, corner_radius=50, text="Logout", fg_color="#595959", hover_color="#1a1a1a", border_color="#1a1a1a", border_width=2,
                                    command=self.login_page)
        logout_button.grid(row=0, column=3, sticky="w")

        # Delete Book Button
        delete_button = ctk.CTkButton(self, text="Delete Book", fg_color="#595959", hover_color="#1a1a1a", border_color="#1a1a1a", border_width=2,
                                    command=lambda: self.delete_book(table))
        delete_button.grid(row=2, column=0)

        # Edit Book Button
        edit_button = ctk.CTkButton(self, text="Edit Book", fg_color="#595959", hover_color="#1a1a1a", border_color="#1a1a1a", border_width=2,
                                    command=lambda: self.modify_book_window(table))
        edit_button.grid(row=2, column=1, sticky="nsw")

        # Add Book Button
        add_button = ctk.CTkButton(self, text="Add Book", fg_color="#595959", hover_color="#1a1a1a", border_color="#1a1a1a", border_width=2,
                                command=self.add_book_window)
        add_button.grid(row=3, column=0, sticky="nsw")

        table.bind('<Double-1>', lambda x: self.return_book(table))
        table.bind('<Button-1>', lambda x: table.selection_remove(*table.selection()))

    def delete_book(self, table):
        selected_items = table.selection()
        if not selected_items:
            messagebox.showerror("Not Selected", "Book Not Selected.")
            return
        book_id = table.item(selected_items[0])['values'][0]
        if messagebox.askyesno('Confirmation', 'Are you sure that you want to delete the selected book?'):
            with open("Books.txt", "r+") as file:
                books = file.readlines()
                index = self.find_index(book_id, books)
                if index != -1:
                    books.pop(index)
                    file.seek(0)
                    file.truncate()
                    file.writelines(books)
            self.populate_table(table) # Refresh the admin page

    def modify_book_window(self, table):
        selected_items = table.selection()
        if not selected_items:
            messagebox.showerror("Not Selected", "Book Not Selected.")
            return
        book_id = table.item(selected_items[0])['values'][0]
        if messagebox.askyesno('Confirmation', 'Are you sure that you want to edit the selected book?'):
            self.create_modify_book_popup(book_id)

    def create_modify_book_popup(self, book_id):
        with open("Books.txt", "r") as file:
            books = file.readlines()
            index = self.find_index(book_id, books)
            if index == -1:
                messagebox.showerror("Not Found", "Book Not Found.")
                return
            book_details = books[index].strip().split(";")

        modify_book_popup = ctk.CTkToplevel()
        modify_book_popup.geometry('500x120')
        modify_book_popup.title('Modify Book')
        modify_book_popup.attributes("-topmost", True)
        modify_book_popup.resizable(width=False, height=False)

        name_entry = ctk.CTkEntry(master=modify_book_popup, height=30, width=500, placeholder_text=f"Book's Name: {book_details[1]}", border_color="#1a1a1a", border_width=2, font=("Arial", 12))
        name_entry.grid(row=0, column=0)
        author_entry = ctk.CTkEntry(master=modify_book_popup, height=30, width=500, placeholder_text=f"Author's Name: {book_details[2]}", border_color="#1a1a1a", border_width=2, font=("Arial", 12))
        author_entry.grid(row=1, column=0)
        
        modify_button = ctk.CTkButton(master=modify_book_popup, text="Modify Book", command=lambda: self.modify_book(name_entry.get(), author_entry.get(), index, books, modify_book_popup))
        modify_button.grid(row=2, column=0)

    def modify_book(self, name, author, index, books, window):
        if name:
            books[index] = books[index].split(';')
            books[index][1] = name
            books[index][2] = author
            books[index] = ';'.join(books[index])
            with open('Books.txt', 'w') as file:
                file.writelines(books)
            messagebox.showinfo("Success", "Book modified successfully.")
        window.destroy()
        self.admin_page()

    def add_book_window(self):
        add_book_popup = ctk.CTkToplevel()
        add_book_popup.geometry('500x120')
        add_book_popup.title('Add Book')
        add_book_popup.attributes("-topmost", True)
        add_book_popup.resizable(width=False, height=False)

        book_id_entry = ctk.CTkEntry(master=add_book_popup, height=30, width=500, placeholder_text="Book's ID", border_color="#1a1a1a", border_width=2, font=("Arial", 12))
        book_id_entry.grid(row=0, column=0)
        name_entry = ctk.CTkEntry(master=add_book_popup, height=30, width=500, placeholder_text="Book's Name", border_color="#1a1a1a", border_width=2, font=("Arial", 12))
        name_entry.grid(row=1, column=0)
        author_entry = ctk.CTkEntry(master=add_book_popup, height=30, width=500, placeholder_text="Author's Name", border_color="#1a1a1a", border_width=2, font=("Arial", 12))
        author_entry.grid(row=2, column=0)
        
        add_button = ctk.CTkButton(master=add_book_popup, text="Add Book", command=lambda: self.add_book(book_id_entry.get(), name_entry.get(), author_entry.get(), add_book_popup))
        add_button.grid(row=3, column=0)

    def add_book(self, id, name, author, window):
        with open('Books.txt', 'r+') as file:
            books = file.readlines()
            if self.find_index(id, books) == -1:
                file.write(f"{id};{name};{author};1;;\n")
                messagebox.showinfo("Success", "Book added successfully.")
            else:
                messagebox.showerror("Already Exists", "Book ID already exists.")
        window.destroy()
        self.admin_page()

    def return_book(self, table):
        selected_items = table.selection()
        if not selected_items:
            messagebox.showerror("Not Selected", "No book selected.")
            return
        book_id = table.item(selected_items[0])['values'][0]
        if messagebox.askyesno('Confirmation', 'Are you sure you want to return this book?'):
            with open("Books.txt", "r+") as file:
                books = file.readlines()
                index = self.find_index(book_id, books)
                if index != -1:
                    books[index] = books[index].split(';')
                    if books[index][3] == "0":  # Currently issued
                        books[index][3] = "1"  # Make it available
                        books[index][4] = ""  # Clear the issuer
                        books[index] = ';'.join(books[index])
                        file.seek(0)
                        file.truncate(0)
                        file.writelines(books)
                        messagebox.showinfo("Returned", "Book returned successfully.")
                    else:
                        messagebox.showerror("Not Issued", "Book is not issued.")
            self.admin_page()

    def find_index(self, book_id, books):
        for index, entry in enumerate(books):
            if entry.split(";")[0] == str(book_id):
                return index
        return -1

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

app = LibraryApp()
app.mainloop()
