from tabulate import tabulate
import sqlite3

db = sqlite3.connect('ebookstore')  #create database
cursor = db.cursor()  #Get a cursor object

#create table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY, Title TEXT,
                   	Author TEXT, Qty INTEGER)''')
db.commit()

#create list to store data to be inserted in the data
#do this only if the table doesn't already exist
books_info = [(3001, 'A Tale of Two Cities', 'Charles Dickens',30),
              (3002, "Harry Potter and the Philosopher's Stone", 'J.K. Rowling', 40),
              (3003, "The Lion, the Witch and the Wardrobe", "C. S. Lewis", 25),
              (3004, "The Lord of the Rings", "J.R.R Tolkien", 37),
              (3005, "Alice in Wonderland", "Lewis Carroll", 12)]

cursor.executemany('INSERT OR IGNORE INTO books(id, Title, Author, Qty) VALUES (?, ?, ?, ?)', books_info)
db.commit()

#to see the data as a table using tabulate module
def see_table():
    cursor.execute('SELECT * FROM books')
    rows = cursor.fetchall()
    header = ['id', 'Title', 'Author', 'Qty']
    table = [row for row in rows]
    print(tabulate(table, headers=header, tablefmt='grid'))

print("The following books are in the database:")
see_table()

while True:
    menu = input('''What would you like to do?
Enter book - b
Update book - u
Delete book - d
Search books - s
view all books - v
exit - e
:''').lower()

    if menu == 'b':  #if user wants to enter a book then ask them for the following details and insert into books
        try:
            id = int(input("Enter book id: "))
            title = input("Enter book title: ").title()
            author = input("Enter author's name: ").title()
            qty = int(input("Enter no. of copies: "))
            cursor.execute('INSERT OR IGNORE INTO books(id, Title, Author, Qty) VALUES (?, ?, ?, ?)',
                       (id, title, author, qty))
            db.commit()
            see_table()
        except ValueError:
            print('Please make sure you enter an integer value for id and number of copies\n')

    elif menu == 'u':  #ask for books id and then ask what attribute of the book they would like to edit
         id = input("which book would you like to edit? Please enter its id: ")

         cursor.execute('SELECT id FROM books WHERE id = ?', (id,))
         if cursor.fetchone() is None:  #checking if id exists
             print('id not found. Please enter a valid id')
             continue

         option2 = input('''what would you like to edit about this book?  
Title - t
Author - a
Qty - q
:''').lower()
         if option2 == 't':
            new_title = input("Enter new title: ")
            cursor.execute('UPDATE books SET Title = ? where id = ?', (new_title, id))
            db.commit()
            print("Updated table:")
            see_table()

         elif option2 == 'a':
             new_author = input("Enter new author: ")
             cursor.execute('UPDATE books SET Author = ? where id = ?', (new_author, id))
             db.commit()
             print("Updated table:")
             see_table()

         elif option2 == 'q':
             new_quantity = input("Enter new quantity: ")
             cursor.execute('UPDATE books SET QTY = ? where id = ?', (new_quantity, id))
             db.commit()
             print("Updated table:")
             see_table()

         else:
             print('incorrect choice')


    elif menu == 'd':  #ask for id and check if it exists. If it does, then delete the row
        id = input("which book would you like to delete? Please enter its id: ")

        cursor.execute('SELECT id FROM books WHERE id = ?', (id,))
        if cursor.fetchone() is None:
            print('id not found. Please enter a valid id\n')

        else:
            cursor.execute('DELETE FROM books WHERE id = ? ', (id,))
            db.commit()
            print("Updated table:")
            see_table()

    elif menu == 'v':
         see_table()  #call function to display books


    elif menu == 's': #ask for book title or author and check if it is in the table
        choice = input('''Would you like to search by author or title of the book?
author - a
title - t
:''').lower()
        if choice == 't':
            search_title = input("Enter title of book to search for: ").lower()
            cursor.execute("SELECT * FROM books WHERE lower(Title) = ?" , (search_title,))
            rows = cursor.fetchall()

            if len(rows) == 0:
               print("No books found")  #not in table, no rows fetched

            else:
               header = ['id', 'Title', 'Author', 'Qty']   #display the book and it's info if it is in the table
               print(tabulate(rows, headers=header, tablefmt='grid'))

        elif choice == 'a':
            search_title = input("Enter author of book to search for: ").lower()
            cursor.execute("SELECT * FROM books WHERE lower(Author) = ?", (search_title,))
            rows = cursor.fetchall()

            if len(rows) == 0:
                print("No books found") #not in table, no rows fetched

            else:
                header = ['id', 'Title', 'Author', 'Qty']  # display the book and it's info if it is in the table
                print(tabulate(rows, headers=header, tablefmt='grid'))

        else:
            print('invalid option')

    elif menu == 'e':
        exit()

    else:
        print('invalid input\n')

db.close()






