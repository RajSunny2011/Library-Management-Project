> # Library Management System
> 
> This project is a Library Management System designed for college first-year Python projects. It leverages several Python libraries to create a modern, user-friendly GUI for managing books and user accounts in a library setting.
> 
> ## Libraries Used
> 
> -   `tkinter`: Standard GUI library for Python.
> -   `customtkinter`: Provides customizable widgets for a more modern UI design.
> -   `hashlib`: Used for secure hashing of passwords.
> -   `datetime`: Utilized for managing date operations.
> 
> ## Features
> 
> ### File Management
> 
> -   **Persistent Storage**: Uses `Books.txt` and `Users.txt` to persistently store book and user data.
> -   **Initialization Check**: At startup, the system checks for the existence of these files and creates them if absent. An admin account setup is triggered if `Users.txt` is newly created.
> 
> ### User Interface Components
> 
> -   **Login and Account Creation**:
>     -   Enforces username and password requirements for new accounts.
>     -   Passwords are hashed using SHA256 before storage for security.
>     -   Login validation checks the hashed password against the stored hash.
> -   **Navigational Buttons**:
>     -   Buttons to navigate between login, account creation, user, and admin pages.
>     -   Functionalities like logout and returning to the login page for ease of navigation.
> 
> ### Book Management
> 
> -   **Admin Functionalities**:
>     -   Add new books with details like ID, name, and author.
>     -   Delete books with confirmation prompts to prevent accidental deletions.
>     -   Edit book details.
> -   **User Functionalities**:
>     -   Issue books, updating the book's status to 'Not Available' and recording the issuer.
>     -   Return books, updating their status to 'Available'.
> -   **Search Feature**:
>     -   Allows users to search for books by name, dynamically updating the displayed list of books based on the search query.
> 
> ### GUI Layout
> 
> -   **Main Window**:
>     -   Configured with `customtkinter` for a consistent look and feel.
>     -   Supports dynamic resizing and modern widget styling.
> -   **Tables for Books**:
>     -   Displayed using `Treeview` from `tkinter.ttk`, styled to match the customtkinter aesthetics.
>     -   Columns for book details like ID, name, author, status, issuer, and the last issue date.
> 
> ### Security Features
> 
> -   **Password Handling**:
>     -   Uses SHA256 hashing to securely store and verify passwords.
> -   **Data Validation**:
>     -   Ensures data integrity by checking for duplicate usernames or book IDs before adding to the system.
> 
> ## Setup and Deployment
> 
> -   **Initial Setup**:
>     -   Installation of Python and necessary libraries is required.
>     -   Run the script to automatically set up necessary files and directories.
> -   **Execution**:
>     -   Execute the Python script to launch the GUI and allow interaction with the system.
