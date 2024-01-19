### Backend Submodule

## Installing package

Make sure to install all necessary packages before starting 

You should have python and pip installed
### `pip install fastapi uvicorn[standard] sqlalchemy python-multipart`

Make sure all the packages are installed
### `pip list`
You should be able to see starlette, SQLAlchemy, fastapi, etc...

Run the following command to start the app
### `uvicorn main:app --reload`
The server will be available at  http://127.0.0.1:8000 

 http://127.0.0.1:8000/docs to get the swagger interface