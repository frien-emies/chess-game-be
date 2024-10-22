# Chess Game Backend API

## Overview
Welcome to the Chess Game Backend API Service. This is a Python Flask API application allows a client to make API calls to endpoints that:
* return a games current state
* save a games current state 

Further details about the applications JSON response, endpoints, dependencies, and other general configuration information can be found below. 

## Cloning Repository and Creating Python Virtual Environment
To clone the repository click on the green button on the GitHub repository that says `clone` and select the `SHH` key option. Then run the following command from the command line once you have selected
the desired directory to create the repository in `git clone your_shh_key`.

Following this you need to create the Python Virtual Environment since Python is a interpreted language. If you are trying to reactivate or deactivate the virtual environment there are instructions for 
that as well. 

### Creating a New Virtual Environment
1. Install `virtualenv` (if not already installed). `virtualenv` is a tool to create isolated Python environments which we will use for setting up this repository.
To install run `pip3 install virtualenv`.

2. Run the following command to create a virtual environment in the root directory of the project (`/chess-game-be`): `python3 -m venv venv`
Note that if you are on a Mac or Linux os the command `python3` must be followed by a three, so that it looks like `python3`. 
This will create a directory called venv in your project folder, which contains the isolated Python environment.

3. Run the following command to activate the virtual environment on your operating system:
- For Mac and Linux: `source venv/bin/activate`
- Windows (cmd): `venv\Scripts\activate`
- Windows (PowerShell): `.\venv\Scripts\Activate`
Once activated, your terminal prompt should change, and you'll see (venv) at the beginning of the command line, indicating that you're working inside the virtual environment.

4. Now we must install all project requirements from the `requirements.txt` file. 
To install run `pip3 install -r requirements.txt`. Make sure you install the versions specifically listed in the `requirements.txt` file, otherwise the dependencies and
versioning of the libraries listed in the .txt file will not merge correctly and will cause your application to crash. 
We can check we installed all our requirements by running `pip3 list` and this will show all packages within the virtual environment. 

### Deactivating Existing Environment
1. To deactivate the virtual environment simply run `deactivate`. This will return you to the global Python environment. 

### Activating Existing Environment
1. To re-activate your virtual environment run the following command to activate the virtual environment on your operating system:
- For Mac and Linux: `source venv/bin/activate`
- Windows (cmd): `venv\Scripts\activate`
- Windows (PowerShell): `.\venv\Scripts\Activate`
You can then follow steps 3-4 for setting up the virtual environment if you need to do additional configuration. 

### Installing and Creating the requirements.txt file
Run the following command to create the requirements.txt file: `pip3 install -r requirements.txt`.

## Using the Flask Command Shell
To use the Flask Command Shell run `flask shell` from the command line. This will allow you to manipulate various elements of the application as detailed below.

### Manipulating the Database with the Flask Command Shell
The Flask Command Shell has numerous commands for manipulating the applications database. To do so you must first open the command shell from the command line by running `flask shell`.
Following this you must import the database tables you wish to manipulate. The syntax for doing so follows conventional Python syntax for importing files. For instance, to import the database
you would run the following line in the Flask Command Shell: `from app import Game`.

After importing the database, you will need to import your models to access the database tables. In this application the command to do so will look like this: `from app import Game`. This will import
the applications Game model by specifying the Model class.

You can exit the Flask Command Shell at any time by clicking the CMD + D keys at the same time. 

### Dropping the Entire Database
To drop all the tables in the database you can run the following command from the the Flask Command Shell: `db.drop_all()`. 

### Creating the Entire Database
To create all the tables in the database you can run the following command from the the Flask Command Shell: `db.create_all()`. This will create al lthe tables based on what models you have present in 
your application. 

### Deleting All Records from A Table
To delete all the records for a specific tablein the database, run the following commands: `db.session.query(table_name).delete()`. In this case table_name is the name of the class model `Game`. 

After running the above command commit the changes to the database: `db.session.commit()`. 

### Seeding the database for testing
To seed the database with sample game data, run python seed.py from the project root directory.

## Endpoints and JSON Contract
The Chess Game Backend API has the following endpoints. 

### `Return a Games Current State by ID`
To have a specific games state returned you must hit the following API endpoint `/api/v1/games/:game_id` where the id corresponds to a particular games id. 

Here is a sample response for hitting the following endpoint:
`/api/v1/games/1`

![Screenshot 2024-10-20 at 11 20 01 AM](https://github.com/user-attachments/assets/d1d6f76e-3b32-4a99-b15b-991fbd0cfca1)

## Other Information: 

### Versioning 

#### Versioning for Python Libraries 
This versioning information is also found in the `requirements.txt` file:

- alembic==1.13.3
- bidict==0.23.1
- blinker==1.8.2
- certifi==2024.8.30
- charset-normalizer==2.0.12
- click==8.1.7
- Flask==2.1.2
- Flask-Migrate==4.0.7
- Flask-SocketIO==5.1.1
- Flask-SQLAlchemy==2.5.1
- h11==0.14.0
- idna==3.10
- itsdangerous==2.2.0
- Jinja2==3.1.4
- Mako==1.3.5
- MarkupSafe==3.0.1
- python-engineio==4.10.1
- python-socketio==5.11.4
- requests==2.26.0
- simple-websocket==1.1.0
- SQLAlchemy==1.4.39
- typing_extensions==4.12.2
- urllib3==1.26.20
- Werkzeug==2.0.3
- wsproto==1.2.0
- Flask-Cors==5.0.0

#### API Version: V1 

#### Python Version: Python 3.13

#### Flask Version: Flask 2.1.2

### Deployment

#### Deployed Site: [Vercel Application](https://chess-game-ybezrcbs2-jcl461437s-projects.vercel.app)


