from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Initially, we don't have any books in the library, so we use an empty list
books = []

@app.route('/')
def index():
    # Render the home page and pass the current list of books to display
    return render_template('index.html', books=books)

@app.route('/add', methods=['POST'])
def add_book():
    # Get data entered by the user to add a new book to the library
    title = request.form['title']
    author = request.form['author']
    year = int(request.form['year'])
    genre = request.form['genre']
    # Set the read status based on the user's input ('yes' means read, 'no' means unread)
    read = True if request.form['read'] == 'yes' else False

    # Add the new book as a dictionary in the books list
    books.append({'title': title, 'author': author, 'year': year, 'genre': genre, 'read': read})
    return redirect(url_for('index'))  # After adding the book, redirect to the home page

@app.route('/remove', methods=['POST'])
def remove_book():
    # Get the title of the book the user wants to remove
    title = request.form['title']
    global books
    # Remove the book by comparing the title (case-insensitive match)
    books = [book for book in books if book['title'].lower() != title.lower()]
    return redirect(url_for('index'))  # Redirect to home page after removing the book

@app.route('/search', methods=['POST'])
def search_books():
    # Get the search query and search type (either title or author)
    query = request.form['query']
    search_by = request.form['search_by']
    result_books = []
    # Search based on title or author
    if search_by == 'title':
        result_books = [book for book in books if query.lower() in book['title'].lower()]
    elif search_by == 'author':
        result_books = [book for book in books if query.lower() in book['author'].lower()]
    else:
        print("Invalid choice")
    # Render the result page with the matching books
    return render_template('index.html', books=result_books)

@app.route('/statistics')
def statistics():
    # Calculate the total number of books
    total_books = len(books)
    # Calculate how many books have been read
    read_books = sum(1 for book in books if book['read'])
    # Calculate the percentage of books that have been read
    read_percentage = (read_books / total_books) * 100 if total_books > 0 else 0
    # Render the statistics page
    return render_template('statistics.html', total_books=total_books, read_percentage=read_percentage)

# Function to handle menu choices and actions
def library_manager():
    while True:
        # Show menu options to the user
        print("\nMenu")
        print("Welcome to your Personal Library Manager!")
        print("1. Add a book")
        print("2. Remove a book")
        print("3. Search for a book")
        print("4. Display all books")
        print("5. Display statistics")
        print("6. Exit")

        try:
            # Get the user's choice
            choice = int(input("Enter your choice: "))
            if choice == 1:
                add_book()  # Call the function to add a book
            elif choice == 2:
                remove_book()  # Call the function to remove a book
            elif choice == 3:
                search_books()  # Call the function to search for a book
            elif choice == 4:
                display_books()  # Call the function to display all books
            elif choice == 5:
                display_statistics()  # Call the function to display statistics
            elif choice == 6:
                print("Exiting the program.")  # Exit the program
                break
            else:
                print("Invalid option! Please choose a number between 1 and 6.")  # Handle invalid options
        except ValueError:
            print("Invalid input! Please enter a valid number.")  # Handle invalid input if user enters a non-number

def add_book():
    # Prompt the user to enter details for the new book
    title = input("Enter the book title: ")
    author = input("Enter the author: ")
    year = int(input("Enter the publication year: "))
    genre = input("Enter the genre: ")
    read_status = input("Have you read this book? (yes/no): ").lower()
    # Convert the read status to a boolean value
    read = True if read_status == 'yes' else False

    # Add the new book as a dictionary to the books list
    books.append({
        'title': title,
        'author': author,
        'year': year,
        'genre': genre,
        'read': read
    })
    print("Book added successfully!")

def remove_book():
    # Ask the user to provide the title of the book to remove
    title_to_remove = input("Enter the title of the book to remove: ")
    # Search for the book by title
    for book in books:
        if book['title'].lower() == title_to_remove.lower():
            books.remove(book)  # Remove the book if found
            print("Book removed successfully!")
            return
    print("Book not found.")  # If book is not found, show this message

def search_books():
    # Give the user options for searching by title or author
    print("Search by:")
    print("1. Title")
    print("2. Author")
    search_choice = int(input("Enter your choice: "))
    # Perform the search based on the user's choice
    if search_choice == 1:
        title = input("Enter the title: ")
        matches = [book for book in books if title.lower() in book['title'].lower()]
    elif search_choice == 2:
        author = input("Enter the author: ")
        matches = [book for book in books if author.lower() in book['author'].lower()]
    else:
        print("Invalid choice.")  # Handle invalid search option
        return

    # If matching books are found, display them
    if matches:
        print("Matching Books:")
        for index, book in enumerate(matches, start=1):
            read_status = 'Read' if book['read'] else 'Unread'
            print(f"{index}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")
    else:
        print("No matching books found.")  # Show if no matching books are found

def display_books():
    # Display all the books in the library
    if books:
        print("Your Library:")
        for index, book in enumerate(books, start=1):
            read_status = 'Read' if book['read'] else 'Unread'
            print(f"{index}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")
    else:
        print("Your library is empty.")  # Show message if no books are in the library

def display_statistics():
    # Calculate the total number of books
    total_books = len(books)
    # If there are books, calculate how many have been read and the percentage
    if total_books > 0:
        read_books = sum(1 for book in books if book['read'])
        read_percentage = (read_books / total_books) * 100
        print(f"Total books: {total_books}")
        print(f"Percentage read: {read_percentage:.1f}%")
    else:
        print("No books in the library.")  # Show message if no books are in the library

if __name__ == '__main__':
    # Start the library manager when the program is run
    library_manager()
