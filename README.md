# NewsAlchemy

NewsAlchemy is a web application that provides users with the latest news articles in various categories like general, sports, entertainment, and technology. The application requires users to log in or register to access the news articles. It is built using Flask, SQLAlchemy, and Bootstrap.

## Features

- User registration and login
- Fetch and display news articles from the NewsAPI
- Categories include General, Sports, Entertainment, and Technology
- Responsive design with Bootstrap
- User sessions stored using Flask-Session

## Installation

### Prerequisites

- Python 3.7+
- Virtual Environment (recommended)

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/news-alchemy.git
   cd news-alchemy

2.	Create and activate a virtual environment:

3.	Install the dependencies:
    pip install -r requirements.txt

4.	Configure the application:
    Create a .env file in the root directory and add your configuration details. An example .env file:
  	SECRET_KEY=your_secret_key
    SQLALCHEMY_DATABASE_URI=postgresql://newsalchemyuser:yourpassword@localhost/news_alchemy_users
    NEWS_API_KEY=your_news_api_key

5.	Initialize the database:

6.	Run the application:

Folder Structure:

news-alchemy/
│
├── app.py              # Main application file
├── config.py           # Configuration file
├── models.py           # Database models
├── forms.py            # Forms for registration and login
├── requirements.txt    # Python dependencies
│
├── templates/          # HTML templates
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── sports.html
│   ├── entertainment.html
│   └── technology.html
│
├── static/             # Static files
│   ├── styles.css
│   └── index.js
│
└── migrations/         # Database migrations


Usage

	•	Visit the home page and either log in or register for an account.
	•	Once logged in, browse through different news categories using the navigation bar.
	•	Search for specific news articles using the search bar.

Contributing

	1.	Fork the repository.
	2.	Create a new branch (git checkout -b feature-branch).
	3.	Make your changes.
	4.	Commit your changes (git commit -am 'Add new feature').
	5.	Push to the branch (git push origin feature-branch).
	6.	Create a new Pull Request.

License

This project is licensed under the MIT License.

