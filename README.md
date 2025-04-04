# COMPSCI 235 Assignment 1 - 'SoundVault' Podcast Library
by azap501, hpra284, and bche 926!


This is our assignment 1 submission for a podcasts webapp project of CompSci 235 in Semester 2, 2024.

This repository contains a partial implementation of the domain model. It contains unit tests which can be run through pytest. 
It also contains a simple Flask application that renders content of a Podcast object instance from our domain model on our designed HTML page. 
We have expanded the domain model implementation, and modified the test cases as needed.

## Description

Dive into a world where captivating stories, insightful discussions, and endless entertainment come to life with SoundVault!
We have thousands of podcasts, diverse in many genres, categories, and tastes imaginable!

In the current state of our webapp, you must be able to: 
- access our homepage
- access our podcast page
- use pagination to browse our podcast page
- view the details of each podcast by clicking on it
- move back to the podcasts page using a back navigation button, after clicking a specific podcast

## Installation

**Installation via requirements.txt**

Please type the following commands in your terminal to ensure that you have all our requirements installed to run out webapp:

**Windows**
```shell
$ cd <project directory>
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

**MacOS**
```shell
$ cd <project directory>
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

When using PyCharm, set the virtual environment using 'File or PyCharm'->'Settings' and select your project from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add Interpreter'. Click the 'Existing environment' radio button to select the virtual environment. 


## Thank you! <3
We hope you enjoyed viewing our webapp. Thank you for marking!

**From azap501, hpra284, and bche926**


## Execution

**Running the application**

From the *project directory*, and within the activated virtual environment (see *venv\Scripts\activate* above):

````shell
$ flask run
```` 

## Testing

After you have configured pytest as the testing tool for PyCharm (File - Settings - Tools - Python Integrated Tools - Testing), you can then run tests from within PyCharm by right-clicking the tests folder and selecting "Run pytest in tests".

Alternatively, from a terminal in the root folder of the project, you can also call 'python -m pytest tests' to run all the tests. PyCharm also provides a built-in terminal, which uses the configured virtual environment. 

## Configuration

The *project directory/.env* file contains variable settings. They are set with appropriate values.

* `FLASK_APP`: Entry point of the application (should always be `wsgi.py`).
* `FLASK_ENV`: The environment in which to run the application (either `development` or `production`).
* `SECRET_KEY`: Secret key used to encrypt session data.
* `TESTING`: Set to False for running the application. Overridden and set to True automatically when testing the application.
* `WTF_CSRF_SECRET_KEY`: Secret key used by the WTForm library.
 
## Data sources

The data files are modified excerpts downloaded from:

https://www.kaggle.com/code/switkowski/building-a-podcast-recommendation-engine/input
