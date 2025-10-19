# Phase-3-Project-Book-Tracker-CLI

## Descrption 

Book Tracker is a command-line interface (CLI) application that helps users manage their personal reading collection. It allows book enthusiasts to track books they want to read, are currently reading, or have completed, while also providing features to rate books, add notes, and view reading statistics.
This application serves as a digital bookshelf where users can organize their reading journey, maintain reading habits, and get insights into their reading patterns through simple text-based commands.

## Features

- **Book Management**: Add, view, update, and delete books
- **Reading Status Tracking**: Track books as "Want to Read", "Currently Reading", or "Completed"
- **Review System**: Add reviews with 1-5 star ratings
- **Search & Filter**: Find books by title, author, or reading status
- **Statistics**: View reading progress and statistics
- **One-to-Many Relationships**: Books can have multiple reviews

## Technologies Used

- Python 3.9
- SQLite3 with custom ORM
- Command-line interface (CLI)

## Project Structure

 - lib/
 - cli.py      : Command-line interface
 - db/
 - models.py   : Book and Review models with custom ORM
 - seed.py     : Database seeding script
 - debug.py    : Debug utilities
 - helpers.py  : Helper functions
 - Pipfile     : Python dependencies
 - README.md   : Project documentation

 ## Getting Started

 1. **Clone the repository**
  
  ```bash
  git clone https://github.com/Oscar254-tech/Phase-3-Project-Book-Tracker.git

2. **Install dependencies**

  ```bash
  pipenv install

3. **Run the application**
   
  ```bash
  python lib/cli.py

## Author

**Oscar Ochanda**  
Email: [oscarochanda@gmail.com]

## License

**MIT License**  
MIT
