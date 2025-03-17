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


## Developing locally

This is being developed using `uv` as a warpper around python.  
For development now, activate the following virtual env:
```bash
source qva/bin/activate
```

For development with Aider, you need to set the OpenAI API key.
```bash
$ export OPENAI_API_KEY=your-api-key-here
```
Make sure that flask can recognise the local app

```bash
$ export FLASK_APP=main.py
```

Before developing - run the tests locally from the directory that conatins the tests directory.

```bash
$ pytest -s 
```


### Starting the app from scratch and Setting up the DB for the first time. 

### In Bash Shell:

```bash
export FLASK_APP=main 
flask db init
flask db migrate -m "Initial migration"
flask db upgrade 
python main.py
```

### In Fish Shell:

```fish
set -x FLASK_APP main
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
python main.py
```

## Running the Application

1. Initialize the database:
   ```bash
   export FLASK_APP=main 
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

## Installing on Glitch, or keeping Glitch updated.  

This app can run in Glitch (https://glitch.com), but I keep forgetting how to get it running, so here are some troubleshooting tips. 


#### Updating the Glitch Repo

Glitch can connect to your github repo. At the bottom of the glitch interface there is a row of features to help you manage your instance - STATUS, LOGS, TERMNIAL, TOOLS, PREVIEW. got into TOOLS and click on the "import/export" button, you can then import from Github and a modal pops up. For example for this app I put in `IanMulvany/question-voting-app` and it updates the local code with the latest commit from that repo. 

I have found it useful to do a `refresh` after. 

#### Essuring the DB is there. 

Through the course of creating this app I changed the DB name, but the old DB was still in glitch causing an error. You can get to a clean state by removing the `migrations` folder if it already esitst, and then in the `instance` folder you shoud have the correctly named db - in this case `ideas_prod.db`. 

To check if the right table is present you can do this

```bash 
cd instance/
sqlite3 ideas_prod.db
.tables
```

If the tables are missing, then to recreate them you can do the following

```bash
export FLASK_APP=main 
flask db init
flask db migrate -m "Initial migration"
flask db upgrade 
```

Rather than running the app from the terminal run this command instead:

```bash
refresh
```

That got it working for me. 
