# Library-Management-Project
College 1st year python project for Library Mangement, using CustomTkinter.
    Libraries:
        tkinter — Standard GUI library for Python.
        customtkinter — Customizable widgets for a more modern UI design.
        hashlib — For secure hashing of passwords.
        datetime — For managing date operations.

Features
File Management

Persistent Storage: Uses text files (Books.txt and Users.txt) to store user and book data persistently.
Initialization Check: On startup, the system checks for the existence of these files and creates them if they are not present. An admin account setup is triggered if Users.txt is newly created.

User Interface Components

Login and Account Creation:
    Users can create new accounts where username and password requirements are enforced.
    Passwords are hashed using SHA256 before storage to ensure security.
    Login validation checks the hashed password against the stored hash.
Navigational Buttons:
    Interactive buttons to navigate between login, account creation, user, and admin pages.
    Functionalities like logout and back to login are implemented for ease of navigation.

Book Management

Admin Functionalities:
    Add new books to the system with details such as ID, name, and author.
    Delete books from the system with confirmation prompts to prevent accidental deletions.
    Edit existing book details.
User Functionalities:
    Issue books which update the book's status to 'Not Available' and record the issuer.
    Return books and update their status to 'Available'.
Search Feature:
    Allows users to search for books by name, updating the displayed list of books in real-time based on the search query.

GUI Layout

Main Window:
    The root window configured with customtkinter for a consistent look and feel.
    Dynamic resizing and modern widget styling using customtkinter properties.
Tables for Books:
    Displayed using Treeview from tkinter.ttk, styled to match the customtkinter aesthetics.
    Columns for book details like ID, name, author, status, issuer, and the last issue date.

Security Features

Password Handling:
    Uses SHA256 hashing to securely store and verify passwords without storing the actual password.
Data Validation:
    Checks and validations at every step to ensure data integrity, such as checking for duplicate usernames or book IDs before adding to the system.

Setup and Deployment

Initial Setup:
    Requires installation of Python and necessary libraries.
    Run the script to automatically set up necessary files and directories.
Execution:
    Start the system by executing the Python script, which launches the GUI and allows interaction with the system.
