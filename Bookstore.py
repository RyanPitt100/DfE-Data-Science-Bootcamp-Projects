import sqlite3
import os


def build_db(id, title, author, qty):
    check_exist = os.path.exists('./Bookstore_db')
    db = sqlite3.connect('./Bookstore_db')
    db.commit()

    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Bookstore_db (id INTEGER PRIMARY KEY, title TEXT NOT NULL, author TEXT NOT NULL, qty INTEGER NOT NULL)
    ''')
    db.commit()
    if check_exist == False:
        for n in range(0, len(id)):
            cursor.execute(''' INSERT INTO Bookstore_db(id, title, author, qty) VALUES(?,?,?,?)
            ''', (id[n], title[n], author[n], qty[n]))
        db.commit()
    return db


def enter_book(db, lastid):
    print("You have chosen to add a new book listing to the database.")
    id = lastid[0] + 1
    title = input("Please enter the book title: ")
    author = input("Please enter Author's name: ")
    qty = input("Please enter stock quantity: ")
    # we have collected the data on the book, now we can add it to the database.
    cursor = db.cursor()
    cursor.execute('''
    INSERT INTO Bookstore_db(id, title, author, qty)
                   VALUES(?, ?, ?, ?)''', (id, title, author, qty))
    db.commit()
    print("Book successfully added! Returning to menu...")
    return


def update_book(db):
    print("You have selected to update the information on one of the books in the database.")
    book_id = int(input("Please enter the id of the book to be changed."))
    column = input(
        "Please enter which piece of information you'd like to change.\n*e.g. title, author, qty").lower()
    # id is automatically generated and guaranteed to be unique so we dont need to update this.
    cursor = db.cursor()
    cursor.execute('''
    SELECT ? FROM Bookstore WHERE id = ?
    ''', (column, book_id))
    current_data = cursor.fetchone()
    new_data = input(
        f"The current value for {column} is {current_data}. What would you like to change it to?")
    if column == 'qty':
        new_data = int(new_data)
    cursor.execute('''
    UPDATE Bookstore_db SET ? = ? WHERE id = ?
    ''', (column, new_data, book_id))

    db.commit()
    print("Book successfully updated! Returning to menu...")


def delete_book(db):
    print("You have selected to delete the entry for one of the books in the database.")
    book_id = int(input("Please enter the id of the book to be removed: "))
    cursor = db.cursor()
    cursor.execute('''DELETE FROM Bookstore_db WHERE id = ?''', (book_id,))
    db.commit()
    print("Book successfully removed! Returning to menu...")


def search_book(db):
    cursor = db.cursor()
    print("You have chosen to search for a book in the database.")
    title = input(
        "Please enter the title or id of the book you wish to search for: ")
    if title.isnumeric():
        id = int(title)
        cursor.execute('''
        SELECT * FROM Bookstore_db WHERE id = ?''', (id,))
    else:
        cursor.execute('''
        SELECT * FROM Bookstore_db WHERE title = ?
        ''', (title,))
    book = cursor.fetchone()
    print('--------------------')
    print('Results:')
    print(
        f"id: {book[0]}\nTitle: {book[1]}\nAuthor: {book[2]}\nQuantity in stock: {book[3]}.")
    print('-------------------')


def print_database(db):
    cursor = db.cursor()
    print("Connected to Bookstore")
    cursor.execute('''SELECT * from Bookstore_db''')
    records = cursor.fetchall()
    print(f"There are currently {len(records)} books in the database.\n")
    print("Printing book information")
    for row in records:
        print("id: ", row[0])
        print("Title: ", row[1])
        print("Author: ", row[2])
        print("Qty: ", row[3])
        print('\n')

    print("Printing complete.")


def main():
    # Leaving this data here for initial calling, if table already exists it shouldnt be used and should not reset the table.

    id = [3001, 3002, 3003, 3004, 3005]
    title = ['A Tale of Two Cities', 'Harry Potter and the Philosopher\'s Stone',
             'The Lion, The Witch, and The Wardrobe', 'The Lord of the Rings', 'Alice in Wonderland']
    author = ['Charles Dickens', 'J.K. Rowling',
              'C.S. Lewis', 'J.R.R. Tolkien', 'Lewis Carroll']
    qty = [30, 40, 25, 37, 12]

    db = build_db(id, title, author, qty)
    print_database(db)

    while True:
        # this will contain our menu with available options for updating database.
        # ask user what to do.
        print("-------------------------------")
        menu = int(input('''Select one of the following options (enter 1,2,3,4 or 0):
        1. Enter Book
        2. Update Book
        3. Delete Book
        4. Search Book
        0. Exit\n\t :'''))
        if menu == 1:
            enter_book(db, lastid)
        elif menu == 2:
            update_book(db)
        elif menu == 3:
            delete_book(db)
        elif menu == 4:
            search_book(db)
        elif menu == 0:
            print("Exiting...")
            break
    cursor.close()
    db.close()
    return 0


if __name__ == "__main__":
    main()
