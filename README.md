# NewsAlchemy

NewsAlchemy is a web application designed to provide users with a personalized news experience. Users can register, log in, and save their favorite news articles. The application uses Flask for the backend and SQLAlchemy for database management. News is fetched from [NewsAPI](https://newsapi.org/).

## Features

- **User Authentication**: Register and log in to your account.
- **Personalized News**: Save and manage your favorite news articles.
- **Smooth Scrolling**: Enjoy a seamless browsing experience with smooth scrolling.

## Live Demo

Check out the live version of the application: https://news-alchemy.onrender.com

### Project Structure
    NewsAlchemy/
    │
    ├── instance/
    │
    ├── migrations/
    │
    ├── static/
    │   ├── js/
    │   │   └── index.js
    │   └── styles.css
    │
    ├── templates/
    │   ├── auth.html
    │   ├── base.html
    │   ├── entertainment.html
    │   ├── favorites.html
    │   ├── home.html
    │   ├── sports.html
    │   └── technology.html
    │
    ├── venv/
    │
    ├── .env
    ├── .gitignore
    ├── app.py
    ├── config.py
    ├── create_db.py
    ├── forms.py
    ├── models.py
    ├── README.md
    ├── requirements.txt
    └── routes.py

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL

### Clone the Repository

    ```sh
    git clone https://github.com/Husky-4559/NewsAlchemy.git
    cd NewsAlchemy

### Set Up Virtual Environment
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

### Install Dependencies
    pip install -r requirements.txt

### Configuration
    Create a .env file in the root directory and add the following environment variables:
    DATABASE_URL=postgresql://username:password@hostname:port/dbname
    SECRET_KEY=your_secret_key
    NEWS_API_KEY=your_news_api_key
    (Replace the placeholders with your actual database credentials, secret key, and News API key.)

### Initialize The Database
    python create_db.py

### Running The Application
    flask run
    The application should now be running on http://127.0.0.1:5000.

### Contributing

	1.	Fork the repository.
	2.	Create a new branch (git checkout -b feature-branch).
	3.	Make your changes.
	4.	Commit your changes (git commit -m 'Add some feature').
	5.	Push to the branch (git push origin feature-branch).
	6.	Open a pull request.

### License

This project is licensed under the MIT License.


