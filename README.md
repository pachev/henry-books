# Henry-Books database using Flask

## Installation

### Python Virtual Environment

This project is best ran in a virtual environment. You can use [pyvenv][2],
which comes with python 3 and greater. The virtual enviroment lets you run
different versions of python and packages from other projects.

#### Installation (Unix)

First install python3+ on your machine and then download and install [pip][1].
Then from the root of the project run:

1. `pyvenv env` - Create a virtual environment in the venv folder
2. `source venv/bin/activate` - Load the environment
3. `pip install -r requirements.txt` - Install dependencies
4. `deactivate` - Unloads the environment


#### Installation (Windows)
Note - Most documentation is for unix systems. Differences between windows and unix are: `env\Scripts\` instead of `env/bin/` and libraries go in `env\Lib\` rather than `env/lib/`)

First install python3+ on your machine and then download and install [pip][1].
Then from the root of the project run:

1. `pip install virtualenv` - Install virtualenv if not already done soCreate a virtual environment in the venv folder
2. `virtualenv venv` - This creates will create a series of directories and scripts
3. `venv/Scripts/activate` - Load the enviroment (There should be a (venv) before the current directory path name
4. `pip install -r requirements.txt` - Install dependencies
5. `deactivate` - Unloads the environment



### Running Application

After the dependencies have been installed issue the command `export FLASK_APP=app.py && flask run`. The app will be running on your localhost

An alternative to this is to run `python app.py` which will also run the app on your localhost. 


As a last resort, a remote version of the application is hosted at [henry.pachevjoseph.com](http://henry.pachevjoseph.com)


[1]: https://pip.pypa.io/en/latest/installing/
[2]: https://docs.python.org/3/using/scripts.html
