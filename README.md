# NewsAlchemy

NewsAlchemy is a web application that aggregates news articles from various sources, allowing users to stay informed on topics of interest. Users can search for news articles, read summaries, and save their favorite articles for later reference. The application aims to simplify the process of staying up-to-date with global events by providing a centralized platform for news consumption. News is fetched from [NewsAPI](https://newsapi.org/).

## Why I Created This Application

In an era where information is abundant yet time is limited, staying informed about world events is both crucial and challenging. Access to diverse news sources enhances our understanding of global issues, promotes informed decision-making, and fosters critical thinking. However, navigating multiple platforms to find relevant news can be time-consuming.

I created NewsAlchemy to address this challenge by offering a streamlined solution for news consumption. The application aggregates articles from various reputable sources, allowing users to customize their news feed based on personal interests. By enabling users to save and organize their favorite articles, NewsAlchemy not only keeps them informed but also encourages continuous learning and engagement with current events.

## Table of Contents:
	•	Features
    •	Database Schema Design
    •	Live Demo
    •	Project Structure
	•	Installation
	•	Usage
	•	Technologies Used
    •	Testing The Application
    •	Running The Tests  
	•	Contributing
	•	License
	•	Acknowledgments




## Features

	•	News Aggregation: Fetches articles from multiple news sources using APIs.
	•	Search Functionality: Allows users to search for articles by keywords or topics.
	•	User Authentication: Secure login and registration with JWT tokens.
	•	Favorites Management: Users can save and organize favorite articles.
	•	Responsive Design: Optimized for both desktop and mobile devices.
	•	Category Filtering: Browse news by categories such as technology, health, sports, etc.

### Database Schema Design:

    +------------+          +-------------+
    |   User     |          |   Favorite  |
    +------------+          +-------------+
    | id         |<--+   +--| id          |
    | username   |   |   |  | title       |
    | email      |   |   |  | url         |
    | password   |   |   |  | user_id     |
    +------------+   |   |  +-------------+
                 |   |
                 |   |
                 +---+
                 One-to-Many

    User:
    •	id: Primary Key (Integer)
    •	username: String (Unique, Not Null)
    •	email: String (Unique, Not Null)
    •	password: String (Not Null)
    •	Relationship: One-to-Many with
    Favorite:
    •	Favorite:
    •	id: Primary Key (Integer)
    •	title: String (Not Null)
    •	url: String (Not Null)
    •	user_id: Foreign Key (Integer, Not Null, References User.id)

## Live Demo

Check out the live version of the application: https://news-alchemy.onrender.com

## Project Structure

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
    ├── tests/
    │   └── test_app.py
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

Follow these steps to set up the project locally:
1. Clone the repository:
    git clone https://github.com/Husky-4559/NewsAlchemy.git

2. Navigate to the project directory:
    cd NewsAlchemy

3. Install dependencies:
    npm install

4.	Set up environment variables
Create a .env file in the root directory with the following content:
    REACT_APP_NEWS_API_KEY=your_news_api_key
    REACT_APP_BASE_URL=http://localhost:3001
  		•	Replace your_news_api_key with your API key from a news API provider.
	    •	Ensure the REACT_APP_BASE_URL matches the URL where your backend server is running.

5. Start the application:
   npm start
   The application should now be running at http://localhost:3000.



## Usage
	•	Explore News Articles: Browse the latest news from various sources.
	•	Search and Filter: Use the search bar to find articles on specific topics.
	•	User Registration: Sign up to save favorite articles and customize your news feed.
	•	Manage Favorites: Save articles to your favorites for easy access later.
	•	Stay Informed: Regularly check the app to stay updated on topics that matter to you.

 ## Technologies Used
    •	Frontend: React.js, React Router, Axios
	•	Backend: PostgreSQL
	•	Authentication: JSON Web Tokens (JWT), bcrypt for password hashing
	•	APIs: News API for fetching news articles
	•	Styling: Bootstrap, CSS3
	•	Form Handling: Formik and Yup for form validation


## Testing The Application

    import unittest
    from app import create_app
    from config import TestConfig
    from models import db, User

    class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            user = User(username='testuser', email='test@example.com')
            user.set_password('Test1234')
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    class UserAuthTests(BaseTestCase):
    def test_registration(self):
        response = self.client.post('/auth/register', data=dict(
            username='newuser',
            email='new@example.com',
            password='Test1234',
            confirm_password='Test1234'
        ), follow_redirects=True)
        self.assertIn(b'Account created successfully!', response.data)

    def test_login(self):
        response = self.client.post('/auth/login', data=dict(
            username='testuser',
            password='Test1234'
        ), follow_redirects=True)
        self.assertIn(b'Login successful!', response.data)

    if __name__ == '__main__':
    unittest.main()

## Run The Tests

    python -m unittest discover

## Contributing

    1.	Fork the repository.
    2.	Create a new branch (git checkout -b feature-branch).
    3.	Make your changes.
    4.	Commit your changes (git commit -m 'Add some feature').
    5.	Push to the branch (git push origin feature-branch).
    6.	Open a pull request.

## License

This project is licensed under the MIT License.

## Acknowledgements
	•	News API: For providing access to news articles.
	•	React.js: For the powerful UI library.
	•	Bootstrap: For the responsive design framework.
	•	Springboard: For project inspiration and guidance.

