# artworks-manager

This project is a submodules of [online_portfolio](https://github.com/AliciaFramboise/online-portfolio/tree/master)

Exposing endpoints to manage artwork.
You can upload artwork and specify its title and a description of it, update it and delete it

## Requirements
- [python](https://www.python.org/downloads/)
- pip 
- [sqlite3](https://dev.to/dendihandian/installing-sqlite3-in-windows-44eb) (or any other embedded database)

>pip should be installed along with python run `$pip --version` to make sure it's correctly installed

## Setup environment and installing packages

### Create a virtual environment 
Having a virtual environment is essential to maintain your independence 
as you will have few packages to install

Open a bash and go to the root of artworks-manager, run the following command to create you virtual environment :

`python -m venv [name_of_venv_folder]`

> Another option, if you're using Pycharm, is to create your virtual environment when adding your python interpreter

You should be able to see if you are in your virtual environment if your terminal shows '(venv)'

### Installing packages

Run the following command to install to dependencies packages :

`pip install fastapi 'uvicorn[standard]' sqlalchemy python-multipart 'passlib[bcrypt]' python-decouple 'python-jose[cryptography]' pytest`


Make sure all the packages are installed by running :

`pip list`

> You should be able to see `starlette`, `SQLAlchemy`, `fastapi`, `bcrypt`, `passlib` and `pydantic`

## Use the app

Run the following command to start the app :

`uvicorn main:app --reload`

The server will be available at  http://127.0.0.1:8000[^2]

You can access to the swagger endpoints in :

 http://127.0.0.1:8000/docs 

[^2]: Modify url and port app by using APP_URL and APP_PORT properties in you .env file
 
## Tips :+1: 

### Use environment variables

You can config your app using environment variable
The app will read a file called .env and extract the values of its properties
Run `cp template.env .env` to get a .env file template

Here's an example of what your .env file could look like (this uses the default values)
```
    DATABASE_NAME=portfolioapp.db
    DATABASE_URL= sqlite:///./
```
> Do not forget to uncomment (remove #) the variables you want to use from the template


### Access Database

If you're using sqlite you can access the db by running the following command : 
``` bash
    $ sqlite3 [db_name][^1]
    
    #example with default value
    $ sqlite3 portfolioapp.db
```
[^1]: You can change your database name by using DATABASE_NAME environment variable

You should enter to this terminal where you can execute sql command :
``` bash
    sqlite> ...
    
    #example to get all users in db
    sqlite> select * from artworks;
```