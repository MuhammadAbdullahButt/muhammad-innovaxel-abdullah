**Flask URL Shortening Service**

This is a URL shortening service built with Flask and SQLAlchemy. It allows users to create short URLs, retrieve the original URLs, update them, delete them, and check the stats for each shortened URL.

**Requirements**

- Python 3.x

- Flask

- Flask-SQLAlchemy

**Setup Instructions**

1. Clone the Repository

_git clone <repository_url>_

_cd <repository_folder>_

2. Install Dependencies

_pip install -r requirements.txt_

3. Set Up the Database
   
The app uses SQLite to store shortened URLs. The database file (database.db) will be automatically created when you run the app for the first time.

5. Run the Application
   
_python app.py_

This will start the app locally, and you can access it at http://127.0.0.1:5000/.

6. Database Structure
   
The database contains a single table ShortURL with the following fields:

_id - Primary key, auto-incremented._

_url - The original long URL._

_short_code - The shortened code used to access the URL._

_created_at - The timestamp when the short URL was created._

_updated_at - The timestamp when the short URL was last updated._

_access_count - Number of times the short URL has been accessed._

7. Utility Function
   
The generate_short_code() function (imported from utils.py) is used to create random short codes for URLs. It generates a random string of characters for the short URL.


