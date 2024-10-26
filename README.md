# Idea Voting App

This is a Python3 Flask project for an idea voting application. The app allows users to submit ideas, vote on them, and view the results in real-time. It is developed using Flask, Flask-SQLAlchemy, Flask-Migrate, and Flask-SocketIO.

## Features

- Submit new ideas with a title and optional description.
- Vote on existing ideas.
- Real-time updates using WebSockets.
- Admin interface to manage ideas.
- Persistent storage using SQLite.

## Requirements

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-SocketIO

## Developing locally

This is being developed using `uv` as a warpper around python.  
For development now, activate the following virtual env:
```bash
source qva/bin/activate
```

For development with Aider, you need to set the OpenAI API key.
```bash
export OPENAI_API_KEY=your-api-key-here
```

Before developing - run the tests locally.



## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Initialize the database:
   ```bash
   flask db upgrade
   ```

2. Run the application:
   ```bash
   python main.py
   ```

3. Open your web browser and go to `http://localhost:5000` to access the application.

## Development

To run the application in development mode with live reloading, use the following command:
```bash
FLASK_ENV=development python main.py
```

## License

This project is licensed under the MIT License.
